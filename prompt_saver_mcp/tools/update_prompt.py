"""Tool for updating existing prompts."""

import logging
from typing import Optional

from mcp.types import Tool, TextContent

from prompt_saver_mcp.database.mongodb_client import mongodb_client
from prompt_saver_mcp.database.models import PromptUpdate
from prompt_saver_mcp.embeddings.voyage_client import voyage_client

logger = logging.getLogger(__name__)


def get_update_prompt_tool() -> Tool:
    """Get the update_prompt tool definition."""
    return Tool(
        name="update_prompt",
        description="Updates an existing prompt with new information. Regenerates embedding if summary changes. Tracks changes in changelog.",
        inputSchema={
            "type": "object",
            "properties": {
                "prompt_id": {
                    "type": "string",
                    "description": "The ID of the prompt to update",
                },
                "change_description": {
                    "type": "string",
                    "description": "Description of what changed (will be added to changelog)",
                },
                "prompt_template": {
                    "type": "string",
                    "description": "Optional new prompt template. If not provided, existing template is kept.",
                },
                "summary": {
                    "type": "string",
                    "description": "Optional new summary. If provided, embedding will be regenerated.",
                },
                "use_case": {
                    "type": "string",
                    "description": "Optional new use case category",
                },
                "history": {
                    "type": "string",
                    "description": "Optional updated history",
                },
            },
            "required": ["prompt_id", "change_description"],
        },
    )


async def handle_update_prompt(
    prompt_id: str,
    change_description: str,
    prompt_template: Optional[str] = None,
    summary: Optional[str] = None,
    use_case: Optional[str] = None,
    history: Optional[str] = None,
) -> list[TextContent]:
    """
    Handle update_prompt tool execution.

    Args:
        prompt_id: ID of the prompt to update
        change_description: Description of changes
        prompt_template: Optional new prompt template
        summary: Optional new summary (triggers embedding regeneration)
        use_case: Optional new use case
        history: Optional updated history

    Returns:
        List of text content with result message
    """
    try:
        # Get existing prompt to check if summary changed
        existing_prompt = mongodb_client.get_prompt(prompt_id)
        if not existing_prompt:
            return [
                TextContent(
                    type="text", text=f"Error: Prompt with ID {prompt_id} not found."
                )
            ]

        # Regenerate embedding if summary changed
        embedding = None
        if summary and summary != existing_prompt.summary:
            logger.info("Summary changed, regenerating embedding...")
            embedding = voyage_client.generate_embedding(summary)

        # Prepare update data
        update_data = PromptUpdate(
            prompt_template=prompt_template,
            summary=summary,
            use_case=use_case,
            history=history,
            embedding=embedding,
            changelog_entry=change_description,
        )

        # Update prompt
        logger.info(f"Updating prompt {prompt_id}...")
        success = mongodb_client.update_prompt(prompt_id, update_data)

        if success:
            result_message = f"""Successfully updated prompt {prompt_id}!

**Change Description:** {change_description}
"""
            if summary:
                result_message += f"**New Summary:** {summary}\n"
            if prompt_template:
                result_message += f"**Template Updated:** Yes\n"
            if embedding:
                result_message += f"**Embedding Regenerated:** Yes\n"

            result_message += "\nThe prompt has been updated and the change has been logged."
            return [TextContent(type="text", text=result_message)]
        else:
            return [
                TextContent(
                    type="text", text=f"Error: Failed to update prompt {prompt_id}."
                )
            ]
    except Exception as e:
        error_message = f"Failed to update prompt: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

