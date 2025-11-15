"""Tool for searching prompts by use case category."""

import logging
from typing import Optional

from mcp.types import Tool, TextContent

from prompt_saver_mcp.database.mongodb_client import mongodb_client

logger = logging.getLogger(__name__)

USE_CASES = ["code-gen", "text-gen", "data-analysis", "creative", "general"]


def get_search_prompts_by_use_case_tool() -> Tool:
    """Get the search_prompts_by_use_case tool definition."""
    return Tool(
        name="search_prompts_by_use_case",
        description="Retrieves prompts filtered by use case category. Use cases: code-gen, text-gen, data-analysis, creative, general.",
        inputSchema={
            "type": "object",
            "properties": {
                "use_case": {
                    "type": "string",
                    "description": "Use case category: code-gen, text-gen, data-analysis, creative, or general",
                    "enum": USE_CASES,
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 10)",
                    "default": 10,
                },
            },
            "required": ["use_case"],
        },
    )


async def handle_search_prompts_by_use_case(
    use_case: str, limit: Optional[int] = 10
) -> list[TextContent]:
    """
    Handle search_prompts_by_use_case tool execution.

    Args:
        use_case: Use case category to filter by
        limit: Maximum number of results

    Returns:
        List of text content with search results
    """
    try:
        if use_case not in USE_CASES:
            return [
                TextContent(
                    type="text",
                    text=f"Invalid use case. Must be one of: {', '.join(USE_CASES)}",
                )
            ]

        if limit is None:
            limit = 10

        # Search by use case
        logger.info(f"Searching prompts for use case: {use_case}")
        results = mongodb_client.search_by_use_case(use_case, limit=limit)

        if not results:
            return [
                TextContent(
                    type="text",
                    text=f"No prompts found for use case '{use_case}'. Try saving a prompt with this use case first.",
                )
            ]

        # Format results
        result_lines = [f"Found {len(results)} prompt(s) for use case '{use_case}':\n"]
        for i, result in enumerate(results, 1):
            prompt_id = result.get("_id", "unknown")
            summary = result.get("summary", "No summary")
            last_updated = result.get("last_updated", "")

            result_lines.append(
                f"{i}. **Prompt ID:** {prompt_id}\n"
                f"   **Summary:** {summary}\n"
                f"   **Last Updated:** {last_updated}\n"
            )

        result_lines.append(
            "\nUse `get_prompt_details` with a prompt ID to view the full prompt template."
        )

        return [TextContent(type="text", text="\n".join(result_lines))]
    except Exception as e:
        error_message = f"Failed to search prompts by use case: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

