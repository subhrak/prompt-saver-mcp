#!/usr/bin/env python3
"""
Helper script for using prompt saver in Cursor.
Provides easy-to-use functions for searching, saving, and managing prompts.
"""

import sys
import os
import json
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path so we can import prompt_saver_mcp
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_saver_mcp.tools.search_prompts import handle_search_prompts
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt
from prompt_saver_mcp.tools.get_prompt_details import handle_get_prompt_details
from prompt_saver_mcp.tools.update_prompt import handle_update_prompt
from prompt_saver_mcp.tools.search_prompts_by_use_case import handle_search_prompts_by_use_case
from prompt_saver_mcp.tools.improve_prompt_from_feedback import handle_improve_prompt_from_feedback


async def search(query: str, limit: int = 5):
    """Search for prompts."""
    print(f"Searching for: '{query}'...")
    result = await handle_search_prompts(query, limit)
    print("\n" + "="*60)
    print(result[0].text)
    print("="*60)


async def save(conversation_file: str = None, conversation_json: str = None, 
               task_description: str = None, context_info: str = None):
    """Save a conversation as a prompt."""
    if conversation_file:
        with open(conversation_file, 'r') as f:
            conversation_json = f.read()
    elif not conversation_json:
        print("Enter conversation JSON (or 'file:<path>' to read from file):")
        print("Format: [{\"role\": \"user\", \"content\": \"...\"}, ...]")
        user_input = input().strip()
        if user_input.startswith("file:"):
            file_path = user_input[5:].strip()
            with open(file_path, 'r') as f:
                conversation_json = f.read()
        else:
            conversation_json = user_input
    
    if not task_description:
        task_description = input("Task description (optional): ").strip() or None
    
    if not context_info:
        context_info = input("Context info (optional): ").strip() or None
    
    print("\nSaving prompt...")
    result = await handle_save_prompt(conversation_json, task_description, context_info)
    print("\n" + "="*60)
    print(result[0].text)
    print("="*60)


async def get_details(prompt_id: str):
    """Get full details of a prompt."""
    print(f"Retrieving prompt: {prompt_id}...")
    result = await handle_get_prompt_details(prompt_id)
    print("\n" + "="*60)
    print(result[0].text)
    print("="*60)


async def search_by_use_case(use_case: str, limit: int = 10):
    """Search prompts by use case."""
    print(f"Searching for {use_case} prompts...")
    result = await handle_search_prompts_by_use_case(use_case, limit)
    print("\n" + "="*60)
    print(result[0].text)
    print("="*60)


async def update(prompt_id: str, change_description: str, **kwargs):
    """Update a prompt."""
    print(f"Updating prompt: {prompt_id}...")
    result = await handle_update_prompt(prompt_id, change_description, **kwargs)
    print("\n" + "="*60)
    print(result[0].text)
    print("="*60)


async def improve(prompt_id: str, feedback: str, conversation_context: str = None):
    """Improve a prompt based on feedback."""
    print(f"Improving prompt: {prompt_id}...")
    result = await handle_improve_prompt_from_feedback(prompt_id, feedback, conversation_context)
    print("\n" + "="*60)
    print(result[0].text)
    print("="*60)


def main():
    parser = argparse.ArgumentParser(description="Prompt Saver Helper for Cursor")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for prompts")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Maximum results (default: 5)")
    
    # Save command
    save_parser = subparsers.add_parser("save", help="Save a conversation as a prompt")
    save_parser.add_argument("--file", help="Path to JSON file with conversation")
    save_parser.add_argument("--json", help="Conversation JSON string")
    save_parser.add_argument("--task", help="Task description")
    save_parser.add_argument("--context", help="Context information")
    
    # Get details command
    details_parser = subparsers.add_parser("details", help="Get prompt details")
    details_parser.add_argument("prompt_id", help="Prompt ID")
    
    # Search by use case
    use_case_parser = subparsers.add_parser("use-case", help="Search by use case")
    use_case_parser.add_argument("use_case", choices=["code-gen", "text-gen", "data-analysis", "creative", "general"],
                                help="Use case category")
    use_case_parser.add_argument("--limit", type=int, default=10, help="Maximum results (default: 10)")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a prompt")
    update_parser.add_argument("prompt_id", help="Prompt ID")
    update_parser.add_argument("--change", required=True, help="Change description")
    update_parser.add_argument("--template", help="New prompt template")
    update_parser.add_argument("--summary", help="New summary")
    update_parser.add_argument("--use-case", help="New use case")
    update_parser.add_argument("--history", help="Updated history")
    
    # Improve command
    improve_parser = subparsers.add_parser("improve", help="Improve a prompt")
    improve_parser.add_argument("prompt_id", help="Prompt ID")
    improve_parser.add_argument("--feedback", required=True, help="Feedback about the prompt")
    improve_parser.add_argument("--context", help="Conversation context")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "search":
            asyncio.run(search(args.query, args.limit))
        elif args.command == "save":
            asyncio.run(save(args.file, args.json, args.task, args.context))
        elif args.command == "details":
            asyncio.run(get_details(args.prompt_id))
        elif args.command == "use-case":
            asyncio.run(search_by_use_case(args.use_case, args.limit))
        elif args.command == "update":
            kwargs = {}
            if args.template:
                kwargs["prompt_template"] = args.template
            if args.summary:
                kwargs["summary"] = args.summary
            if args.use_case:
                kwargs["use_case"] = args.use_case
            if args.history:
                kwargs["history"] = args.history
            asyncio.run(update(args.prompt_id, args.change, **kwargs))
        elif args.command == "improve":
            asyncio.run(improve(args.prompt_id, args.feedback, args.context))
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

