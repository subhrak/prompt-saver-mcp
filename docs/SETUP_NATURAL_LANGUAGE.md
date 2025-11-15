# Setup Natural Language Workflow

## Quick Setup (2 minutes)

### Step 1: Add Cursor Rules

The `.cursorrules` file is already in your project. Cursor should automatically read it, but to be sure:

1. **Check if Cursor picked it up:**
   - Open Cursor
   - Start a chat
   - Say: "What are my rules?"
   - If it mentions prompt saver rules, you're good!

2. **If not automatically loaded:**
   - Open Cursor Settings (Cmd/Ctrl + ,)
   - Search for "Rules" or ".cursorrules"
   - Copy content from `.cursorrules` file
   - Paste into Cursor's Rules section
   - Save

### Step 2: Test It Works

Try this in Cursor chat:

```
"Generate a prompt preview from this conversation: [{'role': 'user', 'content': 'test'}, {'role': 'assistant', 'content': 'test response'}]"
```

If Cursor runs the script and shows a preview, it's working!

---

## How to Use

### Basic Workflow

1. **You:** "Generate a prompt preview from our conversation"
2. **Cursor:** Shows preview
3. **You:** "Save it" (or "Make it more specific about X" then "Save it")
4. **Done!**

### Natural Language Commands

**Generate Preview:**
- "Generate a prompt preview"
- "Create a prompt from our conversation"
- "Preview this conversation"

**Save:**
- "Save it"
- "Save"
- "Allow"
- "Approve"

**Edit:**
- "Make it more specific about [topic]"
- "Add details about [something]"
- "Change category to [category]"

---

## Files Created

1. **`scripts/cursor_prompt_helper.py`** - The helper script Cursor calls
2. **`.cursorrules`** - Instructions for Cursor on how to handle your commands
3. **`CURSOR_NATURAL_LANGUAGE.md`** - Detailed usage guide
4. **`USAGE_EXAMPLE.md`** - Complete example conversation
5. **`NATURAL_LANGUAGE_QUICKSTART.md`** - Quick reference

---

## How It Works

```
You (Natural Language)
  ↓
Cursor (Interprets your command)
  ↓
Cursor (Formats conversation as JSON)
  ↓
Cursor (Runs: python scripts/cursor_prompt_helper.py preview ...)
  ↓
Script (Generates preview, saves to ~/.cursor_prompt_preview.json)
  ↓
Cursor (Shows you preview)
  ↓
You: "Save it"
  ↓
Cursor (Runs: python scripts/cursor_prompt_helper.py save)
  ↓
Script (Saves to MongoDB, clears preview file)
  ↓
Cursor (Shows confirmation)
```

---

## Troubleshooting

### Cursor doesn't recognize commands
- Check that `.cursorrules` is in your project root
- Verify Cursor has read the rules (ask: "What are my rules?")
- Try restarting Cursor

### Script not found
- Make sure you're in the prompt-saver-mcp directory, OR
- Update `.cursorrules` to use absolute path (already included as fallback)

### Preview not showing
- Check that the script ran successfully
- Look for error messages in Cursor's output
- Try running the script manually: `python scripts/cursor_prompt_helper.py --help`

---

## Next Steps

1. Try it: Say "Generate a prompt preview" in Cursor
2. Review the preview
3. Say "Save it" when ready
4. Enjoy your natural language workflow! 🎉

