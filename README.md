# Prompt Saver MCP Server

MCP server that converts successful conversation threads into reusable prompts that can be used for future tasks. Based on the principle that the most important artifact of your LLM interactions is what you did to produce the results, not the results themselves.

## Features

- **Save Conversations as Prompts**: Convert conversation threads into reusable markdown-formatted prompt templates
- **Semantic Search**: Find relevant prompts using vector search powered by Voyage AI embeddings
- **Prompt Management**: Update, retrieve, and improve prompts based on feedback
- **Use Case Categorization**: Automatically categorize prompts (code-gen, text-gen, data-analysis, creative, general)
- **AI-Powered Improvements**: Use GPT-4o-mini to automatically improve prompts based on user feedback

## Tools

### `save_prompt`

Summarizes, categorizes, and converts conversation history into a markdown formatted prompt template.

**Parameters:**
- `conversation_messages` (string, required): JSON string containing the conversation history
- `task_description` (string, optional): Description of the task being performed
- `context_info` (string, optional): Additional context about the conversation

### `search_prompts`

Retrieves prompts from the database using semantic search.

**Parameters:**
- `query` (string, required): Search query to find relevant prompts
- `limit` (integer, optional): Maximum number of results (default: 5)

### `search_prompts_by_use_case`

Retrieves prompts filtered by use case category.

**Parameters:**
- `use_case` (string, required): Use case category (code-gen, text-gen, data-analysis, creative, general)
- `limit` (integer, optional): Maximum number of results (default: 10)

### `update_prompt`

Updates an existing prompt with new information.

**Parameters:**
- `prompt_id` (string, required): The ID of the prompt to update
- `change_description` (string, required): Description of what changed
- `prompt_template` (string, optional): New prompt template
- `summary` (string, optional): New summary (triggers embedding regeneration)
- `use_case` (string, optional): New use case category
- `history` (string, optional): Updated history

### `get_prompt_details`

Retrieves the complete details of a specific prompt.

**Parameters:**
- `prompt_id` (string, required): The ID of the prompt to retrieve

### `improve_prompt_from_feedback`

Uses AI to automatically improve a prompt based on user feedback.

**Parameters:**
- `prompt_id` (string, required): The ID of the prompt to improve
- `feedback` (string, required): User feedback about the prompt
- `conversation_context` (string, optional): Context about how the prompt was used

## Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md) - Step-by-step setup
- [Cursor Usage](docs/CURSOR_USAGE.md) - Using in Cursor with Python imports
- [Natural Language Workflow](docs/CURSOR_NATURAL_LANGUAGE.md) - Natural language commands
- [Quick Start](QUICK_START.md) - Quick reference checklist

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd prompt-saver-mcp
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   # or with uv:
   uv sync
   ```

3. **Set up MongoDB Atlas:**
   - Create a MongoDB Atlas cluster (free tier available)
   - Create a database named `prompt_saver`
   - Create a vector search index on the `embedding` field:
     - Index name: `vector_index`
     - Dimensions: `2048`
     - Similarity: `dotProduct`
     - Path: `embedding`

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and MongoDB Atlas URI
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URI` | MongoDB Atlas connection string | - | Yes |
| `MONGODB_DATABASE` | Database name | `prompt_saver` | No |
| `MONGODB_COLLECTION` | Collection name | `prompts` | No |
| `VOYAGE_AI_API_KEY` | Voyage AI API key | - | Yes |
| `VOYAGE_AI_EMBEDDING_MODEL` | Embedding model | `voyage-3-large` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `OPENAI_MODEL` | Model for analysis | `gpt-4o-mini` | No |

## Using in Cursor

This package is designed to be used directly in Cursor by importing the modules. No MCP client setup required!

### Quick Start

```python
import asyncio
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

# Search for prompts
result = await handle_search_prompts("Python API client", limit=5)
print(result[0].text)

# Save a conversation
conversation_json = json.dumps([
    {"role": "user", "content": "Help me create..."},
    {"role": "assistant", "content": "Here's how..."}
])
result = await handle_save_prompt(conversation_json, "Creating API client")
```

### Helper Scripts

We've included helper scripts in the `scripts/` directory for easier usage:
- `prompt_helper.py` - Main helper with search, save, and other functions
- `save_branch_prompt.py` - Save prompts from GitHub branches

See [CURSOR_USAGE.md](docs/CURSOR_USAGE.md) for detailed examples and workflows.

## Usage Examples

### Saving a Prompt

After completing a complex task in Cursor, save the conversation as a reusable prompt:

```python
import asyncio
import json
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

# Example conversation messages (JSON format)
conversation = [
    {"role": "user", "content": "Help me create a Python function to parse CSV files"},
    {"role": "assistant", "content": "I'll help you create a robust CSV parser..."},
    # ... more conversation
]

# Save the prompt
async def save():
    result = await handle_save_prompt(
        conversation_messages=json.dumps(conversation),
        task_description="Creating a CSV parser function",
        context_info="Successfully created a parser with error handling"
    )
    print(result[0].text)

asyncio.run(save())
```

### Searching for Prompts

Search for relevant prompts when starting a new task:

```python
import asyncio
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts

async def search():
    result = await handle_search_prompts("I need help with data processing in Python", limit=5)
    print(result[0].text)

asyncio.run(search())
```

### Getting Prompt Details

Retrieve full details of a specific prompt:

```python
import asyncio
from prompt_saver_mcp.tools.get_prompt_details import handle_get_prompt_details

async def get_details():
    result = await handle_get_prompt_details("prompt_id_here")
    print(result[0].text)

asyncio.run(get_details())
```

### Updating a Prompt

After using a prompt, update it based on your experience:

```python
import asyncio
from prompt_saver_mcp.tools.update_prompt import handle_update_prompt

async def update():
    result = await handle_update_prompt(
        prompt_id="prompt_id_here",
        change_description="Added error handling examples",
        prompt_template="Updated template with better error handling..."
    )
    print(result[0].text)

asyncio.run(update())
```

### Improving a Prompt with Feedback

Use AI to automatically improve a prompt:

```python
import asyncio
from prompt_saver_mcp.tools.improve_prompt_from_feedback import handle_improve_prompt_from_feedback

async def improve():
    result = await handle_improve_prompt_from_feedback(
        prompt_id="prompt_id_here",
        feedback="The prompt worked well but could use more specific examples for edge cases",
        conversation_context="Used for debugging a complex API integration issue"
    )
    print(result[0].text)

asyncio.run(improve())
```

### Using Helper Scripts

For easier usage, use the helper scripts:

```bash
# Search prompts
python scripts/prompt_helper.py search "Python API client"

# Save a prompt (will prompt for conversation JSON)
python scripts/prompt_helper.py save
```

## Database Schema

Each prompt is stored with the following structure:

```json
{
    "_id": ObjectId,
    "use_case": "code-gen" | "text-gen" | "data-analysis" | "creative" | "general",
    "summary": "Summary of the prompt and its use case",
    "prompt_template": "Universal problem-solving prompt template (markdown)",
    "history": "Summary of steps taken and end result",
    "embedding": [0.1, 0.2, ...],  // 2048 dimensions
    "last_updated": ISODate,
    "num_updates": 0,
    "changelog": ["Change 1", "Change 2", ...],
    "created_by": "user123"  // Optional, for team sharing
}
```

## MongoDB Atlas Vector Search Setup

1. Go to your MongoDB Atlas cluster
2. Navigate to the "Search" tab
3. Click "Create Search Index"
4. Choose "JSON Editor"
5. Use the following configuration:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 2048,
      "similarity": "dotProduct"
    }
  ]
}
```

6. Name the index `vector_index`
7. Select the `prompts` collection

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black prompt_saver_mcp/
ruff check prompt_saver_mcp/
```

## License

MIT License - see LICENSE file for details.

## Notes

- Using `gpt-4o-mini` model for cost efficiency (much cheaper than gpt-4o while still capable)
- MongoDB Atlas free tier includes 512MB storage and shared cluster, sufficient for personal use
- Voyage AI offers free tier with limited requests per month
- Vector search index needs to be created manually in MongoDB Atlas UI (one-time setup)

