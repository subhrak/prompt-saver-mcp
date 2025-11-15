# Natural Language Workflow for Cursor

This guide shows you how to use the prompt saver with natural language commands in Cursor - no code required!

## Setup

### Step 1: Add Cursor Rules

Copy the contents of `.cursorrules` file to your Cursor settings:

1. Open Cursor Settings
2. Go to "Rules for AI" or ".cursorrules"
3. Paste the rules from `.cursorrules` file
4. Save

Alternatively, if your project has a `.cursorrules` file, the rules are already there.

### Step 2: Verify Script is Accessible

Make sure the script is executable:
```bash
chmod +x scripts/cursor_prompt_helper.py
```

## Usage Examples

### Example 1: Simple Save

**You:** "Generate a prompt preview from our conversation"

**Cursor:**
- Formats conversation as JSON
- Runs preview command
- Shows you:

```
📋 PROMPT PREVIEW

📁 Category: code-gen

📝 Summary:
Creating a Python REST API client with error handling...

📄 Prompt Template:
[Full template shown]

---
💡 To save: Say "save it" or "allow" in Cursor chat
```

**You:** "Save it"

**Cursor:**
```
✅ Successfully saved prompt!

**Prompt ID:** 67890abcdef1234567890123
**Use Case:** code-gen
```

---

### Example 2: Edit Before Saving

**You:** "Create a prompt preview from our conversation about the database migration"

**Cursor:** [Shows preview]

**You:** "Make it more specific about Alembic and rollback handling"

**Cursor:**
```
📋 UPDATED PREVIEW

[Shows updated template with Alembic details]

---
💡 Say "save it" to save, or ask for more edits
```

**You:** "Save it"

**Cursor:** "✅ Prompt saved!"

---

### Example 3: With Context

**You:** "Generate a prompt preview. We're on branch feature/user-auth, PR #456"

**Cursor:** [Shows preview with context noted]

**You:** "Save it"

**Cursor:** "✅ Prompt saved with context: Branch: feature/user-auth, PR: #456"

---

### Example 4: Multiple Edits

**You:** "Generate prompt preview"

**Cursor:** [Shows preview]

**You:** "Change category to data-analysis"

**Cursor:** [Shows updated preview with new category]

**You:** "Add more details about data validation"

**Cursor:** [Shows updated preview with validation details]

**You:** "Perfect, save it"

**Cursor:** "✅ Prompt saved!"

---

## Natural Language Commands

### Generate Preview
- "Generate a prompt preview"
- "Create a prompt from our conversation"
- "Preview this conversation as a prompt"
- "Make a prompt template from what we did"
- "Generate prompt preview from our chat"

### Save Prompt
- "Save it"
- "Save"
- "Allow"
- "Approve"
- "Yes, save it"
- "Go ahead and save"
- "Save the prompt"

### Edit Preview
- "Make it more specific about [topic]"
- "Add details about [something]"
- "Change category to [category]"
- "Update the summary to mention [thing]"
- "Make the template include [requirement]"
- "Regenerate with [feedback]"

### Cancel
- "Don't save"
- "Cancel"
- "Skip it"
- "Not this time"

---

## How It Works

1. **You speak naturally** - No code, just conversation
2. **Cursor formats** - Cursor converts conversation to JSON
3. **Preview generated** - Script creates prompt template
4. **You review** - See human-readable preview
5. **You edit** - Tell Cursor what to change (natural language)
6. **You approve** - Say "save it"
7. **Saved** - Prompt goes to database

---

## Tips

1. **Be specific when editing**: "Make it more specific about error handling" works better than "make it better"

2. **Include context**: Mention branch/PR when generating preview or saving

3. **Review before saving**: Always check the preview - you can edit multiple times before saving

4. **Use clear commands**: "Save it" is clearer than "yeah go ahead"

---

## Troubleshooting

### "No preview found"
- Generate a preview first by saying "generate prompt preview"

### Preview looks wrong
- Tell Cursor what to change: "Make it more specific about [topic]"
- Cursor will regenerate with your feedback

### Can't save
- Make sure you've generated a preview first
- Check that the script path is correct in Cursor rules

---

## Advanced Usage

### Save with Custom Context

**You:** "Generate prompt preview. This is for our authentication feature on branch feature/auth"

**Cursor:** [Shows preview]

**You:** "Save it with context: Authentication feature, merged to main on 2024-11-15"

**Cursor:** Saves with that context

### Regenerate Multiple Times

You can ask for multiple edits:
- "Make it more specific about X"
- "Also add details about Y"
- "Change category to Z"
- "Save it"

Each time Cursor regenerates and shows updated preview.

---

Enjoy your natural language prompt saving workflow! 🎉

