"""MCP server for prompt saving and retrieval."""

import asyncio
import logging
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from prompt_saver_mcp.config import config
from prompt_saver_mcp.tools.get_prompt_details import (
    get_get_prompt_details_tool,
    handle_get_prompt_details,
)
from prompt_saver_mcp.tools.improve_prompt_from_feedback import (
    get_improve_prompt_from_feedback_tool,
    handle_improve_prompt_from_feedback,
)
from prompt_saver_mcp.tools.save_prompt import get_save_prompt_tool, handle_save_prompt
from prompt_saver_mcp.tools.search_prompts import (
    get_search_prompts_tool,
    handle_search_prompts,
)
from prompt_saver_mcp.tools.search_prompts_by_use_case import (
    get_search_prompts_by_use_case_tool,
    handle_search_prompts_by_use_case,
)
from prompt_saver_mcp.tools.update_prompt import (
    get_update_prompt_tool,
    handle_update_prompt,
)
from prompt_saver_mcp.tools.preview_prompt import (
    get_preview_prompt_tool,
    handle_preview_prompt,
)
from prompt_saver_mcp.tools.save_approved_prompt import (
    get_save_approved_prompt_tool,
    handle_save_approved_prompt,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("prompt-saver-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        get_save_prompt_tool(),
        get_preview_prompt_tool(),
        get_save_approved_prompt_tool(),
        get_search_prompts_tool(),
        get_search_prompts_by_use_case_tool(),
        get_update_prompt_tool(),
        get_get_prompt_details_tool(),
        get_improve_prompt_from_feedback_tool(),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[dict]:
    """Handle tool calls."""
    try:
        if name == "save_prompt":
            result = await handle_save_prompt(
                conversation_messages=arguments.get("conversation_messages", ""),
                task_description=arguments.get("task_description"),
                context_info=arguments.get("context_info"),
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "search_prompts":
            result = await handle_search_prompts(
                query=arguments.get("query", ""),
                limit=arguments.get("limit", 5),
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "search_prompts_by_use_case":
            result = await handle_search_prompts_by_use_case(
                use_case=arguments.get("use_case", ""),
                limit=arguments.get("limit", 10),
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "update_prompt":
            result = await handle_update_prompt(
                prompt_id=arguments.get("prompt_id", ""),
                change_description=arguments.get("change_description", ""),
                prompt_template=arguments.get("prompt_template"),
                summary=arguments.get("summary"),
                use_case=arguments.get("use_case"),
                history=arguments.get("history"),
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "get_prompt_details":
            result = await handle_get_prompt_details(
                prompt_id=arguments.get("prompt_id", "")
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "improve_prompt_from_feedback":
            result = await handle_improve_prompt_from_feedback(
                prompt_id=arguments.get("prompt_id", ""),
                feedback=arguments.get("feedback", ""),
                conversation_context=arguments.get("conversation_context"),
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "preview_prompt":
            result = await handle_preview_prompt(
                conversation_messages=arguments.get("conversation_messages", ""),
                task_description=arguments.get("task_description"),
            )
            return [{"type": "text", "text": result[0].text}]

        elif name == "save_approved_prompt":
            result = await handle_save_approved_prompt(
                use_case=arguments.get("use_case", ""),
                summary=arguments.get("summary", ""),
                prompt_template=arguments.get("prompt_template", ""),
                history=arguments.get("history", ""),
                context_info=arguments.get("context_info"),
            )
            return [{"type": "text", "text": result[0].text}]

        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [{"type": "text", "text": f"Error: {str(e)}"}]


async def main():
    """Main entry point for the MCP server."""
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated successfully")

        # Run the server with stdio transport
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

