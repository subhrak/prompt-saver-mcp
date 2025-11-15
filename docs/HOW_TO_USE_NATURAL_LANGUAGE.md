# How to Use Natural Language Workflow - Step by Step

## Prerequisites

Before starting, make sure you've completed:
- [ ] MongoDB Atlas setup ✅
- [ ] API keys configured (Voyage AI, OpenAI) ✅
- [ ] `.env` file configured ✅
- [ ] Installed dependencies: `pip install -e .` ✅
- [ ] Vector search index created (1024 dimensions) ✅

---

## Step-by-Step Guide

### Step 1: Verify Setup

Test that everything works:

```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"

# Test the helper script
python scripts/cursor_prompt_helper.py --help
```

Expected: Help text showing available commands (preview, save, show, regenerate).

---

### Step 2: Test Manual Workflow (Before Using with Cursor)

Let's test the workflow manually first to understand how it works.

**Create a test conversation file:** `test_conversation.json`

```json
[
  {
    "role": "user",
    "content": "Help me create a Python function to validate email addresses"
  },
  {
    "role": "assistant",
    "content": "I'll help you create an email validation function. Here's a solution using regex:\n\n```python\nimport re\n\ndef validate_email(email):\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return re.match(pattern, email) is not None\n```"
  }
]
```

**Run preview command:**

```bash
python scripts/cursor_prompt_helper.py preview --file test_conversation.json --task "Creating email validation function"
```

**Expected output:**
```
📋 PROMPT PREVIEW

📁 Category: code-gen

📝 Summary:
[Shows summary about email validation]

📜 What We Did:
[Shows what happened in conversation]

📄 Prompt Template:
------------------------------------------------------------
[Shows reusable template]
------------------------------------------------------------

---
💡 To save: Say "save it" or "allow" in Cursor chat
```

---

### Step 3: Test Save Command

After previewing, test saving:

```bash
python scripts/cursor_prompt_helper.py save --context "Test save"
```

**Expected output:**
```
✅ Successfully saved prompt!

**Prompt ID:** [some ID]
**Use Case:** code-gen
**Summary:** [summary]
```

**Verify in MongoDB:**
- Go to MongoDB Atlas
- Browse Collections → prompt_saver → prompts
- You should see the saved prompt

---

### Step 4: Test Show Command

Check if there's a preview:

```bash
python scripts/cursor_prompt_helper.py show
```

If you just saved, it'll say "No preview found" (correct - preview is cleared after save).

Generate a new preview, then run `show` again to see it.

---

### Step 5: Test Regenerate Command

Generate a preview, then regenerate with feedback:

```bash
# Generate preview
python scripts/cursor_prompt_helper.py preview --file test_conversation.json --task "Test"

# Regenerate with feedback
python scripts/cursor_prompt_helper.py regenerate --feedback "Make it more specific about regex patterns"
```

---

### Step 6: Use with Cursor Chat (Natural Language)

Now that manual testing works, use it with Cursor!

**Open Cursor and start a conversation about any coding task.**

After completing your task, say:

```
"Generate a prompt preview from our conversation"
```

**What should happen:**
1. Cursor formats your conversation as JSON
2. Cursor runs: `python scripts/cursor_prompt_helper.py preview ...`
3. You see a preview
4. Cursor says: "Review the preview above. Say 'save it' to save, or tell me what to change."

**Then you can:**
- Say "Save it" → Saves to database
- Say "Make it more specific about X" → Regenerates with feedback
- Say "Don't save" → Cancels

---

## Complete Example Workflow

### Scenario: Creating an API Client

**1. Work in Cursor (normal conversation)**

```
You: "Help me create a REST API client with error handling"
Cursor: [Provides code and guidance]
You: "Add retry logic"
Cursor: [Adds retry logic]
You: "Perfect, this works!"
```

**2. Generate Preview**

```
You: "Generate a prompt preview from our conversation"
```

**Cursor responds:**
```
Formatting conversation and generating preview...

[Runs: python scripts/cursor_prompt_helper.py preview ...]

📋 PROMPT PREVIEW

📁 Category: code-gen

📝 Summary:
Creating a Python REST API client with error handling and retry logic...

📄 Prompt Template:
------------------------------------------------------------
# Task: Create a REST API Client

## Requirements
- Error handling for network failures
- Retry logic with exponential backoff
...
------------------------------------------------------------

Review the preview above. Say 'save it' to save, or tell me what to change.
```

**3. Edit (Optional)**

```
You: "Make it more specific about the exponential backoff parameters"
```

**Cursor:**
```
Regenerating with your feedback...

[Runs: python scripts/cursor_prompt_helper.py regenerate --feedback "..."]

📋 UPDATED PREVIEW
[Shows updated template with more specifics]

Updated! Review the changes. Say 'save it' when ready.
```

**4. Save**

```
You: "Save it"
```

**Cursor:**
```
[Runs: python scripts/cursor_prompt_helper.py save]

✅ Successfully saved prompt!

**Prompt ID:** 69182f2534cde2cadefbf600
**Use Case:** code-gen
```

Done! ✅

---

## Verification Checklist

Before using with Cursor, verify:

- [ ] Script runs: `python scripts/cursor_prompt_helper.py --help` ✅
- [ ] Preview works: `python scripts/cursor_prompt_helper.py preview --file test_conversation.json` ✅
- [ ] Save works: `python scripts/cursor_prompt_helper.py save` ✅
- [ ] Show works: `python scripts/cursor_prompt_helper.py show` ✅
- [ ] Can see saved prompts in MongoDB Atlas ✅

---

## Files Required for Natural Language Workflow

All these files should exist:

```bash
# Check files exist
ls -la .cursorrules                           # Cursor instructions ✅
ls -la scripts/cursor_prompt_helper.py         # Helper script ✅
ls -la docs/CURSOR_NATURAL_LANGUAGE.md         # Usage guide ✅
ls -la docs/SETUP_NATURAL_LANGUAGE.md          # Setup guide ✅
ls -la docs/USAGE_EXAMPLE.md                   # Example ✅
```

---

## Troubleshooting

### "No preview found"
- Generate preview first: `python scripts/cursor_prompt_helper.py preview --file [file]`

### Cursor doesn't recognize commands
- Check `.cursorrules` exists in project root
- Restart Cursor
- Ask Cursor: "What are my rules?" to verify it loaded them

### Script errors
- Check `.env` file has all required keys
- Verify MongoDB connection works
- Test script manually first

### Permission denied for .env
- Check file permissions: `ls -la .env`
- Make sure .env is readable: `chmod 644 .env`

---

## Quick Test Command

Run this to test the entire workflow:

```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"

# Test preview
echo '[{"role":"user","content":"test"},{"role":"assistant","content":"response"}]' | python scripts/cursor_prompt_helper.py preview --task "Test"

# Test save (after preview above)
python scripts/cursor_prompt_helper.py save --context "Test"
```

If both commands work, you're ready to use with Cursor!

---

## Now Try in Cursor

Open Cursor and say:

```
"Generate a prompt preview from this test conversation: 
[{\"role\": \"user\", \"content\": \"How do I sort a list?\"}, 
 {\"role\": \"assistant\", \"content\": \"Use the sort() method\"}]"
```

If Cursor runs the command and shows a preview, you're all set! 🎉

---

## Next Steps

1. Use naturally in Cursor conversations
2. Build your prompt library
3. Search before starting similar tasks
4. Share with your team

