# Complete Usage Example - Natural Language Workflow

## Scenario: You Just Finished Creating an API Client

### Step 1: Generate Preview

**You (in Cursor chat):**
```
I just finished creating a REST API client with error handling. Generate a prompt preview from our conversation so I can review it.
```

**What Cursor Does:**
1. Formats your conversation as JSON
2. Extracts task description: "Creating REST API client with error handling"
3. Runs: `python scripts/cursor_prompt_helper.py preview --conversation '[JSON]' --task 'Creating REST API client'`
4. Shows you:

```
📋 PROMPT PREVIEW

📁 Category: code-gen

📝 Summary:
Creating a Python REST API client with comprehensive error handling, retry logic, and rate limit management. The conversation covered implementing HTTP requests, handling various error scenarios, and adding exponential backoff for failed requests.

📜 What We Did:
Started with basic requests library usage, then added error handling for network failures (timeouts, connection errors), implemented retry logic with exponential backoff, added rate limit detection and handling, and included proper logging for debugging.

📄 Prompt Template:
------------------------------------------------------------
# Task: Create a REST API Client

## Context
You need to create a Python REST API client that [DESCRIBE PURPOSE]

## Requirements
- Handle HTTP errors gracefully (4xx, 5xx status codes)
- Implement retry logic with exponential backoff
- Detect and handle rate limiting (429 responses)
- Include proper error messages and logging
- Support timeout configuration

## Steps
1. Set up HTTP client with session management
2. Add error handling for network failures (timeouts, connection errors)
3. Implement retry logic with exponential backoff
4. Add rate limit detection (check for 429 status)
5. Include logging for debugging
6. Add timeout configuration
7. Test error scenarios

## Error Handling Pattern
- Network errors: Retry with exponential backoff
- 4xx errors: Log and raise appropriate exception
- 5xx errors: Retry with backoff
- Rate limits: Wait and retry
------------------------------------------------------------

---
💡 To save: Say "save it" or "allow" in Cursor chat
💡 To edit: Tell Cursor what to change, then regenerate
```

**Cursor says:**
```
Preview generated! Review it above. You can say 'save it' to save, or tell me what to change.
```

---

### Step 2: Review and Edit (Optional)

**You:**
```
Make it more specific about the exponential backoff implementation - mention the initial delay and max retries
```

**What Cursor Does:**
1. Extracts feedback: "more specific about exponential backoff - mention initial delay and max retries"
2. Runs: `python scripts/cursor_prompt_helper.py regenerate --feedback 'more specific about exponential backoff - mention initial delay and max retries'`
3. Shows updated preview:

```
📋 UPDATED PREVIEW

📁 Category: code-gen

📝 Summary:
[Same summary]

📜 What We Did:
[Same history]

📄 Updated Prompt Template:
------------------------------------------------------------
# Task: Create a REST API Client

## Context
You need to create a Python REST API client that [DESCRIBE PURPOSE]

## Requirements
- Handle HTTP errors gracefully (4xx, 5xx status codes)
- Implement retry logic with exponential backoff
  - Initial delay: 1 second
  - Maximum retries: 3-5 attempts
  - Backoff multiplier: 2x (doubles each retry)
- Detect and handle rate limiting (429 responses)
- Include proper error messages and logging
- Support timeout configuration

## Steps
1. Set up HTTP client with session management
2. Add error handling for network failures
3. Implement retry logic:
   - Start with initial delay (e.g., 1 second)
   - Double delay on each retry (exponential backoff)
   - Set maximum retry attempts (e.g., 3-5)
   - Handle different error types appropriately
4. Add rate limit detection
5. Include logging
6. Add timeout configuration
7. Test error scenarios

[Rest of template...]
------------------------------------------------------------

---
💡 Say "save it" to save, or ask for more edits
```

**Cursor says:**
```
Updated! Review the changes. Say 'save it' when ready, or tell me what else to change.
```

---

### Step 3: Save

**You:**
```
Save it
```

**What Cursor Does:**
1. Runs: `python scripts/cursor_prompt_helper.py save`
2. Shows confirmation:

```
✅ Successfully saved prompt!

**Prompt ID:** 69182f2534cde2cadefbf600
**Use Case:** code-gen
**Summary:** Creating a Python REST API client with comprehensive error handling...

The prompt has been saved and can be retrieved using the prompt ID or searched using semantic search.
```

**Cursor says:**
```
✅ Prompt saved! ID: 69182f2534cde2cadefbf600

You can now search for it later using: "search prompts for API client"
```

---

## Alternative: Quick Save (No Edits)

**You:**
```
This conversation worked great! Generate a prompt preview and save it.
```

**Cursor:**
- Generates preview
- Shows it to you
- Asks: "Preview generated! Should I save it? Say 'save it' to confirm."

**You:**
```
Yes, save it
```

**Cursor:**
```
✅ Prompt saved! ID: [id]
```

---

## With Context Information

**You:**
```
Generate a prompt preview from our conversation. We're working on branch feature/api-client, PR #123
```

**Cursor:**
- Generates preview
- Notes the context
- Shows preview

**You:**
```
Save it
```

**Cursor:**
- Saves with context: "Branch: feature/api-client, PR: #123"
- Confirms: "✅ Prompt saved with context!"

---

## Multiple Edits Example

**You:** "Generate prompt preview"

**Cursor:** [Shows preview]

**You:** "Change category to data-analysis"

**Cursor:** [Shows updated preview with new category]

**You:** "Also add more details about data validation steps"

**Cursor:** [Shows updated preview with validation details]

**You:** "Perfect, save it"

**Cursor:** "✅ Prompt saved!"

---

## Key Points

1. **No code needed** - Just talk to Cursor naturally
2. **Preview first** - Always see what you're saving
3. **Edit easily** - Tell Cursor what to change
4. **Simple save** - Just say "save it"
5. **Context aware** - Mention branch/PR and it's included

That's the complete natural language workflow! 🎉

