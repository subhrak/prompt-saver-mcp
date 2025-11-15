"""OpenAI client for prompt analysis and generation."""

import json
import logging
from typing import Dict, List, Optional

from openai import OpenAI

from prompt_saver_mcp.config import config

logger = logging.getLogger(__name__)

USE_CASES = ["code-gen", "text-gen", "data-analysis", "creative", "general"]


class OpenAIClient:
    """OpenAI client for analyzing conversations and generating prompts."""

    def __init__(self):
        """Initialize OpenAI client."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL

    def analyze_conversation(
        self, conversation_messages: List[Dict], task_description: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Analyze a conversation thread and extract key information.

        Args:
            conversation_messages: List of conversation messages
            task_description: Optional description of the task

        Returns:
            Dictionary with use_case, summary, and prompt_template
        """
        try:
            # Format conversation for analysis
            conversation_text = self._format_conversation(conversation_messages)

            system_prompt = """You are an expert at analyzing conversation threads and extracting reusable prompt patterns.

Your task is to:
1. Categorize the conversation into one of these use cases: code-gen, text-gen, data-analysis, creative, general
2. Create a concise summary of what the conversation accomplished
3. Generate a universal, reusable prompt template in markdown format that captures the key patterns and steps

The prompt template should be:
- Universal and reusable (not specific to the exact conversation)
- Well-structured with clear sections
- Include placeholders for variable inputs
- Capture the essential problem-solving approach

Return your response as a JSON object with these keys:
- use_case: one of the use case categories
- summary: a brief summary (2-3 sentences)
- prompt_template: the markdown-formatted prompt template
- history: a summary of the steps taken and end result (2-3 sentences)
"""

            user_prompt = f"""Analyze this conversation thread:

{conversation_text}

{f'Task description: {task_description}' if task_description else ''}

Extract the reusable prompt pattern and return as JSON."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            result_text = response.choices[0].message.content
            if not result_text:
                raise ValueError("Empty response from OpenAI")

            result = json.loads(result_text)

            # Validate use_case
            if result.get("use_case") not in USE_CASES:
                logger.warning(f"Invalid use_case {result.get('use_case')}, defaulting to 'general'")
                result["use_case"] = "general"

            return {
                "use_case": result.get("use_case", "general"),
                "summary": result.get("summary", ""),
                "prompt_template": result.get("prompt_template", ""),
                "history": result.get("history", ""),
            }
        except Exception as e:
            logger.error(f"Failed to analyze conversation: {e}")
            raise

    def improve_prompt_from_feedback(
        self, current_prompt: str, feedback: str, conversation_context: Optional[str] = None
    ) -> str:
        """
        Improve a prompt based on user feedback.

        Args:
            current_prompt: The current prompt template
            feedback: User feedback on the prompt
            conversation_context: Optional context about how the prompt was used

        Returns:
            Improved prompt template
        """
        try:
            system_prompt = """You are an expert at improving prompts based on feedback.

Your task is to take the current prompt and user feedback, then generate an improved version that:
- Addresses the feedback points
- Maintains the core structure and approach
- Enhances clarity and effectiveness
- Remains universal and reusable

Return only the improved prompt template in markdown format, without any additional commentary."""

            user_prompt = f"""Current prompt template:

{current_prompt}

User feedback:
{feedback}

{f'Context: {conversation_context}' if conversation_context else ''}

Generate an improved version of this prompt."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )

            improved_prompt = response.choices[0].message.content
            if not improved_prompt:
                raise ValueError("Empty response from OpenAI")

            return improved_prompt.strip()
        except Exception as e:
            logger.error(f"Failed to improve prompt: {e}")
            raise

    def _format_conversation(self, messages: List[Dict]) -> str:
        """
        Format conversation messages into a readable string.

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted conversation string
        """
        formatted = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            formatted.append(f"{role.upper()}: {content}")
        return "\n\n".join(formatted)


# Global OpenAI client instance (lazy initialization)
_openai_client: Optional[OpenAIClient] = None


def get_openai_client() -> OpenAIClient:
    """Get or create the global OpenAI client instance."""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAIClient()
    return _openai_client


# Create a simple object that delegates to get_openai_client()
class OpenAIClientProxy:
    """Proxy for lazy-loaded OpenAI client."""

    def __getattr__(self, name):
        return getattr(get_openai_client(), name)


openai_client = OpenAIClientProxy()

