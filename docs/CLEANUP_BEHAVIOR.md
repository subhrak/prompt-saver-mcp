# Cleanup Behavior

## Automatic Cleanup

The prompt saver system automatically cleans up temporary files after use to keep your workspace clean.

## What Gets Cleaned Up

### 1. Preview Files

After you save a prompt, the preview file is automatically deleted:

```
~/.cursor_prompt_preview.json → Deleted after successful save
```

**Why:** Preview is only needed temporarily. Once saved to MongoDB, you don't need the preview file.

### 2. Conversation JSON Files (Optional)

You can manually delete conversation JSON files after saving prompts, or add them to `.gitignore` to avoid committing them.

**Pattern ignored:** `*conversation*.json`

Examples:
- `our_conversation.json`
- `test_conversation.json`
- `my_conversation_123.json`
- Any file with "conversation" in the name

## What's Kept

### In MongoDB Database
- ✅ Full prompt template
- ✅ Summary
- ✅ Use case category
- ✅ History
- ✅ Embedding (for search)
- ✅ Metadata (timestamps, updates)
- ✅ Context information

### In Your Workspace
- ✅ Code you created
- ✅ Documentation
- ✅ Scripts
- ✅ Configuration files

## Manual Cleanup

If you want to clean up old conversation files:

```bash
# Remove all conversation JSON files
rm *conversation*.json

# Or be more specific
rm my_old_conversation.json
```

## Why This Design?

1. **Database is permanent**: Your prompts are safely stored in MongoDB
2. **Workspace stays clean**: No clutter from temporary conversation files
3. **Easy to recreate**: You can always export conversations again if needed
4. **Git-friendly**: Won't accidentally commit conversation files

## Retrieving Saved Prompts

You don't need the conversation JSON after saving. To get your prompt back:

```bash
# Search for it
python scripts/prompt_helper.py search "your topic"

# Get full details
python scripts/prompt_helper.py details <prompt_id>
```

Or in Cursor:
```
"Search my prompts for [topic]"
```

## Summary

- Preview files: Auto-deleted after save ✅
- Conversation JSONs: Add to .gitignore (already configured) ✅
- Prompts in database: Permanent, searchable, retrievable ✅
- Workspace: Stays clean ✅

