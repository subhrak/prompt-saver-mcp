#!/usr/bin/env python3
"""
Save prompt from current GitHub branch before merging.
Usage: python save_branch_prompt.py [branch-name] [pr-number] [conversation-file]
"""

import sys
import os
import json
import asyncio
import subprocess
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompt_saver_mcp.tools.save_prompt import handle_save_prompt


def get_current_branch():
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_branch_info(branch_name):
    """Get branch commit info."""
    try:
        result = subprocess.run(
            ["git", "log", f"origin/main..{branch_name}", "--oneline"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(
                ["git", "log", f"main..{branch_name}", "--oneline"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "Unable to get branch info"


async def save_branch_prompt(branch_name=None, pr_number=None, conversation_file=None, 
                             conversation_json=None, task_description=None):
    """
    Save prompt for a branch.
    
    Args:
        branch_name: Branch name (auto-detected if None)
        pr_number: PR number for context
        conversation_file: Path to JSON file with conversation
        conversation_json: JSON string of conversation
        task_description: Task description (auto-generated if None)
    """
    if not branch_name:
        branch_name = get_current_branch()
        if not branch_name:
            print("Error: Could not detect git branch. Please specify branch name.")
            return
    
    # Load conversation
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
    
    # Get branch info
    branch_info = get_branch_info(branch_name)
    
    # Build task description
    if not task_description:
        task_description = f"Branch: {branch_name}"
        if pr_number:
            task_description += f", PR: #{pr_number}"
    
    # Build context info
    context_info = f"""Branch: {branch_name}
PR: {pr_number or 'N/A'}
Branch commits:
{branch_info}
"""
    
    print(f"\nSaving prompt for branch: {branch_name}")
    if pr_number:
        print(f"PR: #{pr_number}")
    print("="*60)
    
    try:
        result = await handle_save_prompt(
            conversation_messages=conversation_json,
            task_description=task_description,
            context_info=context_info
        )
        
        print("\n" + "="*60)
        print("✅ PROMPT SAVED SUCCESSFULLY!")
        print("="*60)
        print(result[0].text)
        print(f"\nBranch: {branch_name}")
        if pr_number:
            print(f"PR: #{pr_number}")
        print("\nYou can now safely merge!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error saving prompt: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Save prompt from GitHub branch before merging"
    )
    parser.add_argument("branch", nargs="?", help="Branch name (auto-detected if not provided)")
    parser.add_argument("--pr", type=int, help="PR number")
    parser.add_argument("--file", help="Path to JSON file with conversation")
    parser.add_argument("--json", help="Conversation JSON string")
    parser.add_argument("--task", help="Task description")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(save_branch_prompt(
            branch_name=args.branch,
            pr_number=args.pr,
            conversation_file=args.file,
            conversation_json=args.json,
            task_description=args.task
        ))
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

