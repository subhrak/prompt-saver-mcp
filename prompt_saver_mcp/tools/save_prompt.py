"""Tool for saving conversation threads as prompts."""

import logging
from typing import Optional

from mcp.types import Tool, TextContent

from prompt_saver_mcp.database.mongodb_client import mongodb_client
from prompt_saver_mcp.database.models import PromptCreate
from prompt_saver_mcp.embeddings.voyage_client import voyage_client
from prompt_saver_mcp.llm.openai_client import openai_client
from prompt_saver_mcp.utils.prompt_formatter import format_prompt_template, parse_conversation_json

logger = logging.getLogger(__name__)


def get_save_prompt_tool() -> Tool:
    """Get the save_prompt tool definition."""
    return Tool(
        name="save_prompt",
        description="Summarizes, categorizes, and converts conversation history into a markdown formatted prompt template. Run upon completion of a successful complex task to build your prompt library.",
        inputSchema={
            "type": "object",
            "properties": {
                "conversation_messages": {
                    "type": "string",
                    "description": "JSON string containing the conversation history as a list of messages with 'role' and 'content' keys",
                },
                "task_description": {
                    "type": "string",
                    "description": "Optional description of the task being performed",
                },
                "context_info": {
                    "type": "string",
                    "description": "Additional context about the conversation",
                },
            },
            "required": ["conversation_messages"],
        },
    )


async def handle_save_prompt(
    conversation_messages: str,
    task_description: Optional[str] = None,
    context_info: Optional[str] = None,
) -> list[TextContent]:
    """
    Handle save_prompt tool execution.

    Args:
        conversation_messages: JSON string containing conversation history
        task_description: Optional task description
        context_info: Optional context information

    Returns:
        List of text content with result message
    """
    try:
        # Parse conversation JSON
        messages = parse_conversation_json(conversation_messages)

        # Analyze conversation with OpenAI
        logger.info("Analyzing conversation with OpenAI...")
        analysis_result = openai_client.analyze_conversation(messages, task_description)

        # Format prompt template
        prompt_template = format_prompt_template(messages, analysis_result)

        # Generate embedding
        logger.info("Generating embedding...")
        embedding = voyage_client.generate_embedding(analysis_result["summary"])

        # Create prompt data
        prompt_data = PromptCreate(
            use_case=analysis_result["use_case"],
            summary=analysis_result["summary"],
            prompt_template=prompt_template,
            history=analysis_result["history"],
            embedding=embedding,
            created_by=None,  # Can be extended to include user identification
        )

        # Save to MongoDB
        logger.info("Saving prompt to database...")
        prompt_id = mongodb_client.create_prompt(prompt_data)

        result_message = f"""Successfully saved prompt!

**Prompt ID:** {prompt_id}
**Use Case:** {analysis_result['use_case']}
**Summary:** {analysis_result['summary']}

The prompt has been saved and can be retrieved using the prompt ID or searched using semantic search."""
        if context_info:
            result_message += f"\n\n**Context:** {context_info}"

        return [TextContent(type="text", text=result_message)]
    except ValueError as e:
        error_message = f"Invalid input: {str(e)}"
        logger.error(error_message)
        return [TextContent(type="text", text=f"Error: {error_message}")]
    except Exception as e:
        error_message = f"Failed to save prompt: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

