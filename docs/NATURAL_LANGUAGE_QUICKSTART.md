# Natural Language Quick Start

## Setup (One Time)

### Step 1: Add Cursor Rules

**Option A: Using .cursorrules file (Recommended)**
- The `.cursorrules` file is already in your project
- Cursor should automatically pick it up
- If not, go to Cursor Settings → Rules for AI → Add rules from `.cursorrules`

**Option B: Manual Setup**
1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "Rules" or ".cursorrules"
3. Copy the content from `.cursorrules` file
4. Paste it into Cursor's rules
5. Save

### Step 2: Verify Script Works

```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"
python scripts/cursor_prompt_helper.py --help
```

You should see help text. If not, check that Python can find the script.

---

## Usage (Natural Language)

### Basic Workflow

**1. Generate Preview:**
```
You: "Generate a prompt preview from our conversation"
```

**2. Review:**
Cursor shows you a readable preview with category, summary, and template.

**3. Edit (Optional):**
```
You: "Make it more specific about error handling"
```

**4. Save:**
```
You: "Save it"
```

Done! ✅

---

## Real Example

**You:** "I just finished creating an API client. Generate a prompt preview from our conversation."

**Cursor:**
```
Formatting conversation and generating preview...

📋 PROMPT PREVIEW

📁 Category: code-gen

📝 Summary:
Creating a Python REST API client with error handling and retry logic...

📄 Prompt Template:
[Shows full template]

---
💡 To save: Say "save it" or "allow" in Cursor chat
```

**You:** "Make the summary mention exponential backoff specifically"

**Cursor:**
```
Regenerating with your feedback...

📋 UPDATED PREVIEW

📁 Category: code-gen

📝 Summary:
Creating a Python REST API client with error handling, retry logic using exponential backoff...

📄 Updated Prompt Template:
[Shows updated template]

---
💡 Say "save it" to save, or ask for more edits
```

**You:** "Save it"

**Cursor:**
```
✅ Successfully saved prompt!

**Prompt ID:** 67890abcdef1234567890123
**Use Case:** code-gen
**Summary:** Creating a Python REST API client...

The prompt has been saved and can be retrieved using the prompt ID or searched using semantic search.
```

---

## Common Phrases

### To Generate Preview:
- "Generate a prompt preview"
- "Create a prompt from our conversation"
- "Preview this conversation"
- "Make a prompt template"

### To Save:
- "Save it"
- "Save"
- "Allow"
- "Approve"
- "Yes, save"

### To Edit:
- "Make it more specific about [topic]"
- "Add details about [something]"
- "Change category to [category]"
- "Update the summary"

### To Cancel:
- "Don't save"
- "Cancel"
- "Skip it"

---

## Tips

1. **Be specific**: "Make it more specific about error handling" is better than "make it better"

2. **Include context**: "Generate preview. We're on branch feature/auth, PR #123"

3. **Review carefully**: Check the preview before saving - you can edit multiple times

4. **Use natural language**: Just talk to Cursor normally, no code needed!

---

## Troubleshooting

**"No preview found"**
- Generate a preview first: "Generate prompt preview"

**Preview looks wrong**
- Tell Cursor what to change: "Make it more specific about X"
- Cursor will regenerate

**Script not found**
- Make sure you're in the prompt-saver-mcp directory
- Or use full path: `python /path/to/prompt-saver-mcp/scripts/cursor_prompt_helper.py`

---

That's it! Just talk to Cursor naturally and it handles the rest. 🎉

