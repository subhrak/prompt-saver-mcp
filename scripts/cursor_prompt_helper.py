#!/usr/bin/env python3
"""
Natural language prompt helper for Cursor.
Cursor can call this script with simple commands for preview and save workflow.
"""
import sys
import json
import asyncio
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_saver_mcp.llm.openai_client import get_openai_client
from prompt_saver_mcp.utils.prompt_formatter import parse_conversation_json, format_prompt_template
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

# Store preview in a temp file in user's home directory
PREVIEW_FILE = Path.home() / ".cursor_prompt_preview.json"


async def generate_preview(conversation_json: str, task_description: str = None):
    """Generate and save preview."""
    try:
        messages = parse_conversation_json(conversation_json)
        openai_client = get_openai_client()
        analysis_result = openai_client.analyze_conversation(messages, task_description)
        prompt_template = format_prompt_template(messages, analysis_result)
        
        preview = {
            "use_case": analysis_result["use_case"],
            "summary": analysis_result["summary"],
            "prompt_template": prompt_template,
            "history": analysis_result["history"],
            "conversation_json": conversation_json,
            "task_description": task_description,
        }
        
        # Save preview to file
        with open(PREVIEW_FILE, 'w') as f:
            json.dump(preview, f, indent=2)
        
        # Return human-readable format
        return f"""📋 PROMPT PREVIEW

📁 Category: {preview['use_case']}

📝 Summary:
{preview['summary']}

📜 What We Did:
{preview['history']}

📄 Prompt Template:
{'-' * 60}
{preview['prompt_template']}
{'-' * 60}

---
💡 To save: Say "save it" or "allow" in Cursor chat
💡 To edit: Tell Cursor what to change, then regenerate
"""
    except Exception as e:
        return f"❌ Error generating preview: {str(e)}"


async def save_preview(context_info: str = None):
    """Save the previewed prompt."""
    if not PREVIEW_FILE.exists():
        return "❌ No preview found. Generate a preview first by saying 'generate prompt preview'."
    
    try:
        with open(PREVIEW_FILE, 'r') as f:
            preview = json.load(f)
        
        result = await handle_save_prompt(
            conversation_messages=preview['conversation_json'],
            task_description=preview['task_description'],
            context_info=context_info
        )
        
        # Clean up preview file after successful save
        PREVIEW_FILE.unlink()
        
        return result[0].text + "\n\n💡 Tip: Conversation JSON files are automatically cleaned up. Your prompt is safely stored in the database."
    except Exception as e:
        return f"❌ Error saving prompt: {str(e)}"


def show_preview():
    """Show the current preview."""
    if not PREVIEW_FILE.exists():
        return "❌ No preview found. Generate a preview first by saying 'generate prompt preview'."
    
    try:
        with open(PREVIEW_FILE, 'r') as f:
            preview = json.load(f)
        
        return f"""📋 CURRENT PREVIEW

📁 Category: {preview['use_case']}

📝 Summary:
{preview['summary']}

📜 What We Did:
{preview['history']}

📄 Prompt Template:
{'-' * 60}
{preview['prompt_template']}
{'-' * 60}

---
💡 Say "save it" to save, or ask for edits
"""
    except Exception as e:
        return f"❌ Error reading preview: {str(e)}"


async def regenerate_with_feedback(feedback: str):
    """Regenerate preview with user feedback."""
    if not PREVIEW_FILE.exists():
        return "❌ No preview found. Generate a preview first."
    
    try:
        with open(PREVIEW_FILE, 'r') as f:
            old_preview = json.load(f)
        
        # Use OpenAI to improve the prompt based on feedback
        from prompt_saver_mcp.llm.openai_client import get_openai_client
        openai_client = get_openai_client()
        
        # Regenerate with feedback
        improved_template = openai_client.improve_prompt_from_feedback(
            old_preview['prompt_template'],
            feedback,
            old_preview['history']
        )
        
        # Update preview
        old_preview['prompt_template'] = improved_template
        
        # Save updated preview
        with open(PREVIEW_FILE, 'w') as f:
            json.dump(old_preview, f, indent=2)
        
        return f"""📋 UPDATED PREVIEW

📁 Category: {old_preview['use_case']}

📝 Summary:
{old_preview['summary']}

📜 What We Did:
{old_preview['history']}

📄 Updated Prompt Template:
{'-' * 60}
{improved_template}
{'-' * 60}

---
💡 Say "save it" to save, or ask for more edits
"""
    except Exception as e:
        return f"❌ Error regenerating: {str(e)}"


async def main():
    parser = argparse.ArgumentParser(description="Cursor Prompt Helper - Natural Language Workflow")
    parser.add_argument(
        "command",
        choices=["preview", "save", "show", "regenerate"],
        help="Command: preview (generate), save (save to DB), show (show current), regenerate (update with feedback)"
    )
    parser.add_argument("--conversation", help="Conversation JSON string (for preview)")
    parser.add_argument("--file", help="Path to file containing conversation JSON (for preview)")
    parser.add_argument("--task", help="Task description (for preview)")
    parser.add_argument("--context", help="Context info like branch/PR (for save)")
    parser.add_argument("--feedback", help="Feedback for regeneration")
    
    args = parser.parse_args()
    
    try:
        if args.command == "preview":
            if args.file:
                with open(args.file, 'r') as f:
                    conversation_json = f.read()
            elif args.conversation:
                conversation_json = args.conversation
            else:
                # Read from stdin
                conversation_json = sys.stdin.read()
            
            result = await generate_preview(conversation_json, args.task)
            print(result)
        
        elif args.command == "save":
            result = await save_preview(args.context)
            print(result)
        
        elif args.command == "show":
            result = show_preview()
            print(result)
        
        elif args.command == "regenerate":
            if not args.feedback:
                print("❌ Error: --feedback is required for regenerate command")
                sys.exit(1)
            result = await regenerate_with_feedback(args.feedback)
            print(result)
    
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

