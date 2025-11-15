# Using Prompt Saver in Cursor

This guide shows you how to use the Prompt Saver directly in Cursor without needing Claude Desktop.

## Quick Start

### Option 1: Using Helper Scripts (Easiest)

The helper scripts make it super easy to use the prompt saver:

```bash
# Search for prompts
python scripts/prompt_helper.py search "Python API client"

# Save a conversation (will prompt for input)
python scripts/prompt_helper.py save

# Get details of a specific prompt
python scripts/prompt_helper.py details <prompt_id>

# Search by use case
python scripts/prompt_helper.py use-case code-gen
```

### Option 2: Import Directly in Cursor

You can import and use the modules directly in Cursor's chat or Python scripts:

```python
import asyncio
import json
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

# Search for prompts
async def search():
    result = await handle_search_prompts("Python API client", limit=5)
    print(result[0].text)

asyncio.run(search())
```

## Common Workflows

### 1. Before Starting a Task: Search for Relevant Prompts

**In Cursor Chat:**
```
"Search my prompt library for anything about creating REST API clients"
```

**Then run:**
```bash
python scripts/prompt_helper.py search "REST API client"
```

**Or in Python:**
```python
import asyncio
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts

result = await handle_search_prompts("REST API client", limit=3)
print(result[0].text)
```

### 2. After Completing a Task: Save the Conversation

**Step 1:** Copy your conversation from Cursor chat and format as JSON:

```json
[
  {"role": "user", "content": "Help me create an API client..."},
  {"role": "assistant", "content": "Here's how to create..."},
  {"role": "user", "content": "Can you add error handling?"},
  {"role": "assistant", "content": "Sure, here's the updated version..."}
]
```

**Step 2:** Save it:

```bash
# Option A: Save from file
python scripts/prompt_helper.py save --file conversation.json --task "Creating API client"

# Option B: Interactive (will prompt for input)
python scripts/prompt_helper.py save
```

**Or in Python:**
```python
import asyncio
import json
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

conversation = [
    {"role": "user", "content": "Help me create..."},
    {"role": "assistant", "content": "Here's how..."}
]

result = await handle_save_prompt(
    conversation_messages=json.dumps(conversation),
    task_description="Creating API client",
    context_info="Successfully created with error handling"
)
print(result[0].text)
```

### 3. Before Merging a Branch: Save Branch Prompt

```bash
# Auto-detect branch and save
python scripts/save_branch_prompt.py --file conversation.json --pr 123

# Or specify branch
python scripts/save_branch_prompt.py feature/api-client --pr 123 --file conversation.json
```

### 4. Get Full Prompt Details

After searching, you'll get prompt IDs. Get full details:

```bash
python scripts/prompt_helper.py details <prompt_id>
```

**Or in Python:**
```python
from prompt_saver_mcp.tools.get_prompt_details import handle_get_prompt_details

result = await handle_get_prompt_details("prompt_id_here")
print(result[0].text)
```

### 5. Improve a Prompt Based on Feedback

```bash
python scripts/prompt_helper.py improve <prompt_id> \
  --feedback "Worked well but needs more error handling examples" \
  --context "Used for debugging API integration"
```

**Or in Python:**
```python
from prompt_saver_mcp.tools.improve_prompt_from_feedback import handle_improve_prompt_from_feedback

result = await handle_improve_prompt_from_feedback(
    prompt_id="prompt_id_here",
    feedback="Worked well but needs more error handling examples",
    conversation_context="Used for debugging API integration"
)
print(result[0].text)
```

## Using in Cursor Chat

### Example 1: Search Before Starting

**You:** "I need to create a database migration script. Search my prompt library for anything related."

**Then in terminal or Python:**
```python
import asyncio
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts

result = await handle_search_prompts("database migration script", limit=3)
print(result[0].text)
```

### Example 2: Save After Success

**You:** "This conversation worked great! Save it as a prompt."

**Then:**
1. Copy the conversation from Cursor chat
2. Format as JSON
3. Run: `python scripts/prompt_helper.py save`

### Example 3: Use Found Prompt

**You:** "I found a relevant prompt. Show me the full template and help me adapt it for my current task."

**Then:**
```python
from prompt_saver_mcp.tools.get_prompt_details import handle_get_prompt_details

# Get the prompt details
result = await handle_get_prompt_details("prompt_id_from_search")
print(result[0].text)

# Then use the template in your conversation with Cursor
```

## Integration with Your Development Workflow

### Pre-commit Hook (Optional)

Create a script that reminds you to save prompts:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Did you save any useful prompts from this branch? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Run: python scripts/save_branch_prompt.py"
fi
```

### Branch Workflow

```bash
# 1. Work on feature branch
git checkout -b feature/new-api-client

# 2. Do your work with Cursor
# ... code, chat, iterate ...

# 3. Before merging, save the prompt
python scripts/save_branch_prompt.py feature/new-api-client --pr 123 --file conversation.json

# 4. Merge
git checkout main
git merge feature/new-api-client
```

## Tips

1. **Search before starting**: Always search your prompt library before beginning similar tasks
2. **Save successful patterns**: If a conversation worked well, save it immediately
3. **Use descriptive task descriptions**: Makes searching easier later
4. **Add context**: Include branch names, PR numbers, or other context when saving
5. **Improve over time**: Use the improve function to refine prompts based on experience

## Troubleshooting

### Import Errors

If you get import errors:

```python
import sys
import os
sys.path.insert(0, '/path/to/prompt-saver-mcp')
```

Or make sure you've installed the package:
```bash
pip install -e .
```

### Environment Variables Not Loading

Make sure your `.env` file is in the `prompt-saver-mcp` directory and contains all required variables.

### Async Functions

Remember to use `asyncio.run()` or `await` when calling the functions:

```python
# Correct
asyncio.run(handle_search_prompts("query"))

# Or in async context
result = await handle_search_prompts("query")
```

## Next Steps

- Check out the helper scripts in `scripts/` directory
- See [README.md](../README.md) for full API documentation
- See [GETTING_STARTED.md](GETTING_STARTED.md) for setup instructions

