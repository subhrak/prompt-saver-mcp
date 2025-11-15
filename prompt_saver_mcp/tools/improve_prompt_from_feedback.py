"""Tool for improving prompts based on feedback."""

import logging
from typing import Optional

from mcp.types import Tool, TextContent

from prompt_saver_mcp.database.mongodb_client import mongodb_client
from prompt_saver_mcp.database.models import PromptUpdate
from prompt_saver_mcp.embeddings.voyage_client import voyage_client
from prompt_saver_mcp.llm.openai_client import openai_client

logger = logging.getLogger(__name__)


def get_improve_prompt_from_feedback_tool() -> Tool:
    """Get the improve_prompt_from_feedback tool definition."""
    return Tool(
        name="improve_prompt_from_feedback",
        description="Uses AI to automatically improve a prompt based on user feedback. Analyzes feedback and suggests improvements to the prompt template.",
        inputSchema={
            "type": "object",
            "properties": {
                "prompt_id": {
                    "type": "string",
                    "description": "The ID of the prompt to improve",
                },
                "feedback": {
                    "type": "string",
                    "description": "User feedback about the prompt (what worked, what didn't, suggestions)",
                },
                "conversation_context": {
                    "type": "string",
                    "description": "Optional context about how the prompt was used",
                },
            },
            "required": ["prompt_id", "feedback"],
        },
    )


async def handle_improve_prompt_from_feedback(
    prompt_id: str, feedback: str, conversation_context: Optional[str] = None
) -> list[TextContent]:
    """
    Handle improve_prompt_from_feedback tool execution.

    Args:
        prompt_id: ID of the prompt to improve
        feedback: User feedback
        conversation_context: Optional context about usage

    Returns:
        List of text content with improved prompt
    """
    try:
        # Get existing prompt
        existing_prompt = mongodb_client.get_prompt(prompt_id)
        if not existing_prompt:
            return [
                TextContent(
                    type="text", text=f"Error: Prompt with ID {prompt_id} not found."
                )
            ]

        # Use OpenAI to improve the prompt
        logger.info(f"Improving prompt {prompt_id} based on feedback...")
        improved_template = openai_client.improve_prompt_from_feedback(
            existing_prompt.prompt_template, feedback, conversation_context
        )

        # Regenerate embedding since template changed
        logger.info("Regenerating embedding for improved prompt...")
        new_embedding = voyage_client.generate_embedding(existing_prompt.summary)

        # Update prompt with improved template
        update_data = PromptUpdate(
            prompt_template=improved_template,
            embedding=new_embedding,
            changelog_entry=f"Improved prompt based on feedback: {feedback}",
        )

        success = mongodb_client.update_prompt(prompt_id, update_data)

        if success:
            result_message = f"""Successfully improved prompt {prompt_id}!

**Feedback:** {feedback}
"""
            if conversation_context:
                result_message += f"**Context:** {conversation_context}\n"

            result_message += f"\n## Improved Prompt Template\n\n{improved_template}"

            result_message += "\n\nThe prompt has been updated with the improvements."
            return [TextContent(type="text", text=result_message)]
        else:
            return [
                TextContent(
                    type="text", text=f"Error: Failed to update prompt {prompt_id}."
                )
            ]
    except Exception as e:
        error_message = f"Failed to improve prompt: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

