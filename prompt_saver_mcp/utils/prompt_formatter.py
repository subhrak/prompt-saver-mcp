"""Utility functions for formatting conversations into prompts."""

import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def parse_conversation_json(conversation_json: str) -> List[Dict]:
    """
    Parse conversation JSON string into a list of message dictionaries.

    Args:
        conversation_json: JSON string containing conversation messages

    Returns:
        List of message dictionaries with 'role' and 'content' keys
    """
    try:
        messages = json.loads(conversation_json)
        if not isinstance(messages, list):
            raise ValueError("Conversation JSON must be a list of messages")

        # Validate message structure
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dictionary")
            if "role" not in msg or "content" not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")

        return messages
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse conversation JSON: {e}")
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        logger.error(f"Failed to parse conversation: {e}")
        raise


def format_prompt_template(
    conversation_messages: List[Dict], analysis_result: Dict[str, str]
) -> str:
    """
    Format the prompt template with proper markdown structure.

    Args:
        conversation_messages: Original conversation messages
        analysis_result: Analysis result from OpenAI

    Returns:
        Formatted markdown prompt template
    """
    template = analysis_result.get("prompt_template", "")

    # Ensure template has proper markdown formatting
    if not template.strip().startswith("#"):
        template = f"# Prompt Template\n\n{template}"

    return template


def extract_key_patterns(conversation_messages: List[Dict]) -> List[str]:
    """
    Extract key patterns from conversation messages.

    Args:
        conversation_messages: List of conversation messages

    Returns:
        List of key patterns identified
    """
    patterns = []
    # Simple pattern extraction - can be enhanced with more sophisticated analysis
    user_messages = [msg for msg in conversation_messages if msg.get("role") == "user"]
    assistant_messages = [
        msg for msg in conversation_messages if msg.get("role") == "assistant"
    ]

    if len(user_messages) > 1:
        patterns.append("Multi-step problem solving")
    if len(assistant_messages) > 0:
        patterns.append("Iterative refinement")

    return patterns

