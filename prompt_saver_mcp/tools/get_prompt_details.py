"""Tool for retrieving full prompt details."""

import logging

from mcp.types import Tool, TextContent

from prompt_saver_mcp.database.mongodb_client import mongodb_client

logger = logging.getLogger(__name__)


def get_get_prompt_details_tool() -> Tool:
    """Get the get_prompt_details tool definition."""
    return Tool(
        name="get_prompt_details",
        description="Retrieves the complete details of a specific prompt including the full template, history, and metadata.",
        inputSchema={
            "type": "object",
            "properties": {
                "prompt_id": {
                    "type": "string",
                    "description": "The ID of the prompt to retrieve",
                },
            },
            "required": ["prompt_id"],
        },
    )


async def handle_get_prompt_details(prompt_id: str) -> list[TextContent]:
    """
    Handle get_prompt_details tool execution.

    Args:
        prompt_id: ID of the prompt to retrieve

    Returns:
        List of text content with prompt details
    """
    try:
        prompt = mongodb_client.get_prompt(prompt_id)
        if not prompt:
            return [
                TextContent(
                    type="text", text=f"Error: Prompt with ID {prompt_id} not found."
                )
            ]

        # Format prompt details
        details = [
            f"# Prompt Details\n",
            f"**Prompt ID:** {prompt_id}",
            f"**Use Case:** {prompt.use_case}",
            f"**Summary:** {prompt.summary}",
            f"**Last Updated:** {prompt.last_updated}",
            f"**Number of Updates:** {prompt.num_updates}",
        ]

        if prompt.created_by:
            details.append(f"**Created By:** {prompt.created_by}")

        if prompt.changelog:
            details.append(f"\n## Changelog")
            for i, change in enumerate(prompt.changelog, 1):
                details.append(f"{i}. {change}")

        details.append(f"\n## History\n{prompt.history}")

        details.append(f"\n## Prompt Template\n\n{prompt.prompt_template}")

        return [TextContent(type="text", text="\n".join(details))]
    except Exception as e:
        error_message = f"Failed to get prompt details: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

