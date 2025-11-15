#!/usr/bin/env python3
"""Test script to search for prompts in the database."""
import asyncio
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts

async def test_search():
    print("="*60)
    print("TESTING PROMPT SEARCH")
    print("="*60)
    
    query = "fibonacci Python function"
    print(f"\nSearching for: '{query}'")
    print()
    
    try:
        result = await handle_search_prompts(query, limit=5)
        
        print("="*60)
        print("SEARCH RESULTS:")
        print("="*60)
        print(result[0].text)
        print("="*60)
        
        if "No prompts found" in result[0].text:
            print("\n⚠️  No prompts found. This is normal if you haven't saved any yet.")
            print("   Try running: python test_save_prompt.py")
        else:
            print("\n✅ Search completed successfully!")
        
        return result
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your .env file has VOYAGE_AI_API_KEY")
        print("  2. Verify MongoDB connection")
        print("  3. Make sure vector search index is created and active")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_search())

