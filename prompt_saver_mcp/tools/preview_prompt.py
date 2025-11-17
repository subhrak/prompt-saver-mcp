"""Tool for previewing prompt before saving."""

import logging
from typing import Optional

from mcp.types import Tool, TextContent

from prompt_saver_mcp.llm.openai_client import openai_client
from prompt_saver_mcp.utils.prompt_formatter import format_prompt_template, parse_conversation_json

logger = logging.getLogger(__name__)


def get_preview_prompt_tool() -> Tool:
    """Get the preview_prompt tool definition."""
    return Tool(
        name="preview_prompt",
        description="Generate a preview of what the prompt template will look like before saving. Shows category, summary, history, and full template for review.",
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
            },
            "required": ["conversation_messages"],
        },
    )


async def handle_preview_prompt(
    conversation_messages: str,
    task_description: Optional[str] = None,
) -> list[TextContent]:
    """
    Handle preview_prompt tool execution.

    Args:
        conversation_messages: JSON string containing conversation history
        task_description: Optional task description

    Returns:
        List of text content with preview message
    """
    try:
        # Parse conversation JSON
        messages = parse_conversation_json(conversation_messages)

        # Analyze conversation with OpenAI
        logger.info("Analyzing conversation with OpenAI for preview...")
        analysis_result = openai_client.analyze_conversation(messages, task_description)

        # Format prompt template
        prompt_template = format_prompt_template(messages, analysis_result)

        # Store preview data in a special format for later saving
        # We'll return it in a structured way for Cursor to display
        preview_message = f"""📋 PROMPT PREVIEW

📁 **Category:** {analysis_result['use_case']}

📝 **Summary:**
{analysis_result['summary']}

📜 **What We Did:**
{analysis_result['history']}

📄 **Prompt Template:**
{'-' * 60}
{prompt_template}
{'-' * 60}

---

💡 **To save this prompt:** Use the `save_approved_prompt` tool with this preview data.

**Preview Data (for saving):**
```json
{{
  "use_case": "{analysis_result['use_case']}",
  "summary": "{analysis_result['summary']}",
  "prompt_template": {prompt_template.__repr__()},
  "history": "{analysis_result['history']}",
  "conversation_messages": {conversation_messages.__repr__()},
  "task_description": "{task_description}"
}}
```

**Note:** You can ask me to regenerate with specific feedback before saving, or proceed to save this version.
"""

        return [TextContent(type="text", text=preview_message)]
    except ValueError as e:
        error_message = f"Invalid input: {str(e)}"
        logger.error(error_message)
        return [TextContent(type="text", text=f"Error: {error_message}")]
    except Exception as e:
        error_message = f"Failed to generate preview: {str(e)}"
        logger.error(error_message, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_message}")]

