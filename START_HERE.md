# 🚀 START HERE - Natural Language Workflow

## ✅ All Files Are Ready

Your natural language workflow is fully set up! Here's how to use it.

---

## Step-by-Step: First Time Usage

### Step 1: Test It Works (30 seconds)

Open terminal and run:

```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"

# Test the workflow
python scripts/cursor_prompt_helper.py preview --file test_conversation.json --task "Email validation"
```

You should see a preview with category, summary, and template. ✅

### Step 2: Test Saving

```bash
python scripts/cursor_prompt_helper.py save --context "First test"
```

You should see "✅ Successfully saved prompt!" ✅

### Step 3: Verify in MongoDB

Go to MongoDB Atlas → Browse Collections → `prompt_saver` → `prompts`

You should see 2-3 saved prompts (including your test). ✅

---

## Using in Cursor (Natural Language)

### Open Cursor and Try This:

**1. Start a conversation** (any coding task)

Example:
```
You: "Help me create a Python function to read CSV files"
Cursor: [Helps you create the function]
You: "Can you add error handling?"
Cursor: [Adds error handling]
```

**2. Generate preview**

```
You: "Generate a prompt preview from our conversation"
```

**What Cursor Will Do:**
- Format conversation as JSON
- Run preview command
- Show you the preview

**3. Review and save**

```
You: "Save it"
```

Done! Your prompt is saved to the database.

---

## Natural Language Commands

### Generate Preview
Just say any of these:
- "Generate a prompt preview"
- "Create a prompt from our conversation"
- "Preview this conversation"

### Save
Just say:
- "Save it"
- "Allow"
- "Approve"

### Edit Before Saving
Say:
- "Make it more specific about [topic]"
- "Add details about [something]"
- "Change category to [category]"

### Cancel
Say:
- "Don't save"
- "Cancel"

---

## Complete Example

```
You: "Help me create a database migration script"
Cursor: [Helps you create it]

You: "Generate a prompt preview"
Cursor: [Shows preview]

You: "Make it mention that we're using Alembic"
Cursor: [Shows updated preview]

You: "Perfect, save it"
Cursor: ✅ Prompt saved!
```

---

## Files You Need to Know About

### For Usage
- `.cursorrules` - Teaches Cursor the commands (already configured)
- `scripts/cursor_prompt_helper.py` - The script Cursor calls (working)
- `test_conversation.json` - Sample for testing (created)

### For Documentation
- `docs/HOW_TO_USE_NATURAL_LANGUAGE.md` - Detailed guide
- `docs/CURSOR_NATURAL_LANGUAGE.md` - Full documentation
- `docs/USAGE_EXAMPLE.md` - Complete example

---

## Quick Verification

Run these commands to verify everything is ready:

```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"

# 1. Check helper script works
python scripts/cursor_prompt_helper.py --help
# Should show help text ✅

# 2. Check .cursorrules exists
cat .cursorrules | head -5
# Should show Cursor rules ✅

# 3. Test preview
python scripts/cursor_prompt_helper.py preview --file test_conversation.json
# Should show preview ✅

# 4. Test save
python scripts/cursor_prompt_helper.py save
# Should save successfully ✅
```

---

## You're Ready!

All files are properly set up:
- ✅ Helper script works
- ✅ Cursor rules configured
- ✅ Documentation complete
- ✅ Test files created
- ✅ MongoDB connected
- ✅ API keys working

**Next:** Open Cursor and say "Generate a prompt preview from our conversation"

Enjoy your natural language workflow! 🎉

---

## Need Help?

- Detailed guide: `docs/HOW_TO_USE_NATURAL_LANGUAGE.md`
- Example: `docs/USAGE_EXAMPLE.md`
- Troubleshooting: `docs/SETUP_NATURAL_LANGUAGE.md`

