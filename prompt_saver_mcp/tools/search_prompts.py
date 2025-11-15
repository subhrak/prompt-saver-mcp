"""Tool for searching prompts using vector search."""

import logging
from typing import Optional

from mcp.types import Tool, TextContent

from prompt_saver_mcp.database.mongodb_client import mongodb_client
from prompt_saver_mcp.embeddings.voyage_client import voyage_client

logger = logging.getLogger(__name__)


def get_search_prompts_tool() -> Tool:
    """Get the search_prompts tool definition."""
    return Tool(
        name="search_prompts",
        description="Retrieves prompts from the database using semantic search (if Voyage API key is available) or text search as fallback. Returns ranked results with summaries.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant prompts",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 5)",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    )


async def handle_search_prompts(query: str, limit: Optional[int] = 5) -> list[TextContent]:
    """
    Handle search_prompts tool execution.

    Args:
        query: Search query string
        limit: Maximum number of results

    Returns:
        List of text content with search results
    """
    try:
        if limit is None:
            limit = 5

        # Generate embedding for query
        logger.info(f"Generating embedding for query: {query}")
        query_embedding = voyage_client.generate_embedding(query)

        # Perform vector search
        logger.info("Performing vector search...")
        results = mongodb_client.vector_search(query_embedding, limit=limit)

        if not results:
            return [
                TextContent(
                    type="text",
                    text="No prompts found matching your query. Try a different search term or save a new prompt.",
                )
            ]

        # Format results
        result_lines = [f"Found {len(results)} matching prompt(s):\n"]
        for i, result in enumerate(results, 1):
            score = result.get("score", 0.0)
            prompt_id = result.get("_id", "unknown")
            use_case = result.get("use_case", "unknown")
            summary = result.get("summary", "No summary")
            last_updated = result.get("last_updated", "")

            result_lines.append(
                f"{i}. **Prompt ID:** {prompt_id}\n"
                f"   **Use Case:** {use_case}\n"
                f"   **Summary:** {summary}\n"
                f"   **Similarity Score:** {score:.3f}\n"
                f"   **Last Updated:** {last_updated}\n"
            )

        result_lines.append(
            "\nUse `get_prompt_details` with a prompt ID to view the full prompt template."
        )

        return [TextContent(type="text", text="\n".join(result_lines))]
    except Exception as e:
        error_message = f"Failed to search prompts: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

