# How to Use - Complete Guide

## ✅ Setup Verified

Your natural language workflow is ready! All files are properly configured.

---

## Quick Start (3 Steps)

### 1. Test It Manually

```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"

# Generate preview
python scripts/cursor_prompt_helper.py preview --file test_conversation.json --task "Email validation"

# Save it
python scripts/cursor_prompt_helper.py save --context "Test"
```

### 2. Use in Cursor

Open Cursor and say:
```
"Generate a prompt preview from our conversation"
```

### 3. Save After Review

```
"Save it"
```

Done! ✅

---

## Complete Natural Language Workflow

### The Flow

```
1. You work normally in Cursor → Complete your task
                                     ↓
2. You: "Generate prompt preview" → Cursor formats conversation
                                     ↓
3. Cursor shows preview → You review use case, summary, template
                                     ↓
4. Optional: "Make it more specific" → Cursor regenerates
                                     ↓
5. You: "Save it" → Cursor saves to database
                                     ↓
6. ✅ Done! Prompt saved and searchable
```

---

## Example Conversation

### Full Example: Creating an API Client

**You start working:**
```
You: "Help me create a REST API client for the GitHub API"
Cursor: [Provides code]

You: "Add error handling"
Cursor: [Adds error handling]

You: "Add retry logic with exponential backoff"
Cursor: [Adds retry logic]

You: "Perfect! This works great."
```

**Generate preview:**
```
You: "Generate a prompt preview from our conversation"

Cursor: 
Formatting conversation and generating preview...

📋 PROMPT PREVIEW

📁 Category: code-gen

📝 Summary:
Creating a Python REST API client for GitHub with comprehensive error 
handling and retry logic using exponential backoff.

📜 What We Did:
Started with basic API client, added error handling for network failures,
implemented retry logic with exponential backoff for rate limits.

📄 Prompt Template:
------------------------------------------------------------
# Task: Create a REST API Client

## Context
You need to create a Python REST API client for [API NAME]

## Requirements
- HTTP request handling
- Error handling for network failures
- Retry logic with exponential backoff
- Rate limit detection

## Implementation Steps
1. Set up HTTP client with session management
2. Add error handling (timeouts, connection errors)
3. Implement retry logic with exponential backoff
4. Add rate limit detection (429 responses)
5. Include logging for debugging

## Error Handling Pattern
- Network errors: Retry with exponential backoff
- 4xx errors: Log and raise exception
- 5xx errors: Retry with backoff
- Rate limits: Wait and retry
------------------------------------------------------------

Review the preview above. Say 'save it' to save, or tell me what to change.
```

**Review and edit (optional):**
```
You: "Make it more specific about the backoff parameters - initial delay and max retries"

Cursor:
Regenerating with your feedback...

📋 UPDATED PREVIEW

[Shows updated template with specific backoff parameters:
- Initial delay: 1 second
- Max retries: 3-5
- Backoff multiplier: 2x]

Updated! Review the changes. Say 'save it' when ready.
```

**Save:**
```
You: "Save it"

Cursor:
✅ Successfully saved prompt!

**Prompt ID:** 69183b932538aa5448125d4e
**Use Case:** code-gen

The prompt has been saved to your library.
```

---

## Using Saved Prompts

### Search Before Starting New Tasks

```
You: "I need to create an API client for Slack. Do we have any prompts about API clients?"

Cursor: 
[Runs search command]

Found 2 matching prompts:

1. **Prompt ID:** 69183b932538aa5448125d4e
   **Use Case:** code-gen
   **Summary:** Creating a REST API client with error handling...
   **Similarity Score:** 0.850

2. [Another prompt...]

Would you like to see the full template for any of these?
```

```
You: "Show me the full template for the first one"

Cursor:
[Runs get details command and shows full template]

Here's the template. Should I adapt it for your Slack API client?
```

---

## Commands Reference

### Generate Preview
- "Generate a prompt preview"
- "Create a prompt from our conversation"
- "Preview this conversation as a prompt"
- "Make a prompt template"

### Save
- "Save it"
- "Save"
- "Allow"
- "Approve"
- "Yes, save"

### Edit
- "Make it more specific about [X]"
- "Add details about [Y]"
- "Change category to [Z]"
- "Update the summary"

### Search (use regular prompt_helper.py)
```bash
python scripts/prompt_helper.py search "your query"
```

Or in Cursor: "Search my prompts for [topic]" and then run the command

---

## Troubleshooting

### Cursor doesn't respond to commands

**Check 1: Rules loaded?**
Ask Cursor: "What are my rules?"
- If it mentions prompt saver rules → ✅ Loaded
- If not → Restart Cursor or add rules manually

**Check 2: Script accessible?**
```bash
python scripts/cursor_prompt_helper.py --help
```
Should show help. If error, check paths in `.cursorrules`

### "No preview found" when saving

Generate preview first: "Generate a prompt preview"

### Script errors

Run verification:
```bash
./VERIFY_SETUP.sh
```

All checks should pass.

---

## What's Happening Behind the Scenes

When you say "Generate prompt preview":

1. Cursor formats your conversation as JSON
2. Cursor runs: `python scripts/cursor_prompt_helper.py preview ...`
3. Script:
   - Sends conversation to OpenAI (GPT-4o-mini)
   - Gets back: use_case, summary, template, history
   - Saves preview to `~/.cursor_prompt_preview.json`
   - Returns formatted preview
4. Cursor shows you the preview

When you say "Save it":

1. Cursor runs: `python scripts/cursor_prompt_helper.py save`
2. Script:
   - Reads preview from `~/.cursor_prompt_preview.json`
   - Generates embedding (Voyage AI)
   - Saves to MongoDB
   - Clears preview file
3. Cursor shows confirmation

---

## You're All Set!

Everything is ready. Just open Cursor and try:

```
"Generate a prompt preview from our conversation"
```

Then:

```
"Save it"
```

That's it! No code, no complexity, just natural language. 🎉

---

## Next Steps

1. Use in your daily workflow
2. Build your prompt library
3. Search before starting similar tasks
4. Share with your team (they follow same setup)

