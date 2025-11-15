#!/usr/bin/env python3
"""Test script to save a prompt to the database."""
import asyncio
import json
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

# Sample conversation for testing
conversation = [
    {
        "role": "user",
        "content": "Help me create a Python function to calculate fibonacci numbers"
    },
    {
        "role": "assistant",
        "content": "I'll help you create a Python function to calculate Fibonacci numbers. Here's a clean implementation:\n\n```python\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n```\n\nThis recursive function calculates the nth Fibonacci number."
    },
    {
        "role": "user",
        "content": "Can you add memoization to make it faster?"
    },
    {
        "role": "assistant",
        "content": "Sure! Here's an optimized version with memoization:\n\n```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n```\n\nThis uses Python's built-in `lru_cache` decorator to cache results, making it much faster for repeated calls."
    }
]

async def test_save():
    print("="*60)
    print("TESTING PROMPT SAVE")
    print("="*60)
    print("\nSaving conversation as prompt...")
    print("Conversation summary:")
    print(f"  - User asked about Fibonacci function")
    print(f"  - Assistant provided recursive solution")
    print(f"  - User requested memoization")
    print(f"  - Assistant provided optimized version")
    print()
    
    try:
        result = await handle_save_prompt(
            conversation_messages=json.dumps(conversation),
            task_description="Creating Fibonacci function with memoization",
            context_info="Test save from native Python script - verifying database connection"
        )
        
        print("="*60)
        print("RESULT:")
        print("="*60)
        print(result[0].text)
        print("="*60)
        print("\n✅ SUCCESS! Prompt saved to database.")
        print("\nYou can now:")
        print("  1. Search for it: python scripts/prompt_helper.py search 'fibonacci'")
        print("  2. View it in MongoDB Atlas: Browse Collections → prompt_saver → prompts")
        
        return result
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your .env file has all required keys")
        print("  2. Verify MongoDB connection string is correct")
        print("  3. Check that MongoDB Atlas cluster is running")
        print("  4. Verify network access is allowed")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_save())

