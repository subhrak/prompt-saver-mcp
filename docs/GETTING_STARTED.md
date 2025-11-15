# Getting Started Guide

This guide will walk you through setting up and using the Prompt Saver MCP Server step by step.

## Prerequisites

Before you begin, make sure you have:
- Python 3.10 or higher installed
- A MongoDB Atlas account (free tier is fine)
- A Voyage AI API key (free tier available)
- An OpenAI API key (you'll get free credits when you sign up)

---

## Step 1: Set Up MongoDB Atlas

### 1.1 Create a MongoDB Atlas Account
1. Go to [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Create a new cluster (choose the free M0 tier)

### 1.2 Create Database User
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and password (save these!)
5. Set privileges to "Atlas admin" or "Read and write to any database"
6. Click "Add User"

### 1.3 Configure Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (or add your specific IP)
4. Click "Confirm"

### 1.4 Get Your Connection String
1. Go to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (it looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
5. Replace `<password>` with your database user password
6. Replace `<username>` with your database username
7. Save this connection string - you'll need it in Step 3

### 1.5 Create the Vector Search Index
1. In MongoDB Atlas, go to your cluster
2. Click "Browse Collections"
3. Create a database named `prompt_saver` (if it doesn't exist)
4. Create a collection named `prompts` (if it doesn't exist)
5. Go to the "Search" tab (next to "Collections")
6. Click "Create Search Index"
7. Choose "JSON Editor"
8. Paste this configuration:

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

9. Name the index: `vector_index`
10. Select the database: `prompt_saver`
11. Select the collection: `prompts`
12. Click "Next" and then "Create Search Index"
13. Wait for the index to finish building (this may take a few minutes)

---

## Step 2: Get API Keys

### 2.1 Voyage AI API Key
1. Go to [https://www.voyageai.com/](https://www.voyageai.com/)
2. Sign up for a free account
3. Go to your dashboard/API keys section
4. Copy your API key
5. Save it - you'll need it in Step 3

### 2.2 OpenAI API Key
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign up for an account (you'll get free credits)
3. Go to API Keys section: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key immediately (you won't see it again!)
6. Save it - you'll need it in Step 3

---

## Step 3: Install and Configure the MCP Server

### 3.1 Navigate to the Project Directory
```bash
cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"
```

### 3.2 Install Python Dependencies
```bash
# Option 1: Using pip
pip install -e .

# Option 2: Using uv (if you have it installed)
uv sync
```

### 3.3 Create Environment File
```bash
# Copy the example file
cp .env.example .env
```

### 3.4 Edit the .env File
Open `.env` in a text editor and fill in your values:

```bash
# MongoDB Configuration
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/
MONGODB_DATABASE=prompt_saver
MONGODB_COLLECTION=prompts

# Voyage AI Configuration
VOYAGE_AI_API_KEY=your_voyage_ai_api_key_here
VOYAGE_AI_EMBEDDING_MODEL=voyage-3-large

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

**Important:** Replace:
- `YOUR_USERNAME` with your MongoDB database username
- `YOUR_PASSWORD` with your MongoDB database password
- `YOUR_CLUSTER` with your MongoDB cluster name
- `your_voyage_ai_api_key_here` with your Voyage AI API key
- `your_openai_api_key_here` with your OpenAI API key

### 3.5 Test the Installation
```bash
python -m prompt_saver_mcp.server
```

If everything is configured correctly, the server should start without errors. Press `Ctrl+C` to stop it.

**Note:** This test just verifies the server can start. For actual usage in Cursor, you'll import the modules directly (see Step 4).

---

## Step 4: Using in Cursor

### 4.1 Import the Modules

In Cursor, you can use the prompt saver by importing the modules directly. Here's how:

**Option A: Use Helper Scripts (Recommended)**

We've created helper scripts that make it easy to use in Cursor. See `scripts/` directory for:
- `prompt_helper.py` - Main helper with search and save functions
- `save_branch_prompt.py` - Save prompts from GitHub branches

**Option B: Import Directly in Cursor**

You can import and use the modules directly in Cursor's chat or Python scripts:

```python
import asyncio
import json
import sys
import os

# Add the prompt-saver-mcp to path if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'prompt-saver-mcp'))

from prompt_saver_mcp.tools.search_prompts import handle_search_prompts
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt
from prompt_saver_mcp.tools.get_prompt_details import handle_get_prompt_details

# Search for prompts
async def search_prompts(query: str):
    result = await handle_search_prompts(query, limit=5)
    print(result[0].text)
    return result

# Save a conversation
async def save_prompt(conversation_json: str, task_description: str = None):
    result = await handle_save_prompt(conversation_json, task_description)
    print(result[0].text)
    return result

# Example usage
# asyncio.run(search_prompts("Python API client"))
```

### 4.2 Using Helper Scripts

The easiest way is to use the provided helper scripts. See [CURSOR_USAGE.md](CURSOR_USAGE.md) for detailed examples.

For natural language workflow (preview and approve), see [CURSOR_NATURAL_LANGUAGE.md](CURSOR_NATURAL_LANGUAGE.md).

---

## Step 5: Verify Everything Works

### 5.1 Test Searching Prompts

Create a test file `test_prompt_saver.py`:

```python
import asyncio
from prompt_saver_mcp.tools.search_prompts import handle_search_prompts

async def test():
    result = await handle_search_prompts("test query", limit=1)
    print(result[0].text)

asyncio.run(test())
```

Run it:
```bash
python test_prompt_saver.py
```

### 5.2 Test Saving a Prompt

```python
import asyncio
import json
from prompt_saver_mcp.tools.save_prompt import handle_save_prompt

conversation = [
    {"role": "user", "content": "How do I create a Python function?"},
    {"role": "assistant", "content": "To create a Python function, use the 'def' keyword..."}
]

async def test_save():
    result = await handle_save_prompt(
        conversation_messages=json.dumps(conversation),
        task_description="Testing prompt saver"
    )
    print(result[0].text)

asyncio.run(test_save())
```

### 5.3 Use in Cursor Chat

In Cursor's chat, you can ask:

```
"Search my prompt library for anything about Python API clients"
```

Then use the helper scripts or import the modules to execute the search.

---

## Troubleshooting

### Problem: "Failed to connect to MongoDB"
**Solution:**
- Check that your MongoDB URI is correct
- Verify your database user password doesn't have special characters that need URL encoding
- Make sure your IP address is allowed in MongoDB Network Access
- Check that your cluster is running

### Problem: "VOYAGE_AI_API_KEY is required"
**Solution:**
- Make sure your `.env` file exists and has the correct key
- Verify the key is correct (no extra spaces)
- Make sure you're loading the `.env` file (it should be in the same directory)

### Problem: "OPENAI_API_KEY is required"
**Solution:**
- Check your `.env` file has the OpenAI key
- Verify you have credits in your OpenAI account
- Make sure the key starts with `sk-`

### Problem: Vector search not working
**Solution:**
- Make sure you created the vector search index in MongoDB Atlas
- Wait for the index to finish building (check the Search tab in Atlas)
- The index name must be exactly `vector_index`

### Problem: Import errors in Cursor
**Solution:**
- Make sure you've installed the package: `pip install -e .`
- Check that the `prompt-saver-mcp` directory is in your Python path
- Try using absolute imports or add the directory to `sys.path`
- Verify your `.env` file is in the prompt-saver-mcp directory

---

## Next Steps

Once everything is set up:

1. **Start saving prompts**: After completing useful conversations in Cursor, use the helper scripts to save them as reusable templates
2. **Search before starting**: Use `search_prompts` to find relevant prompts before beginning new tasks
3. **Improve prompts**: Use `improve_prompt_from_feedback` to refine prompts based on your experience
4. **Organize by use case**: Use `search_prompts_by_use_case` to find prompts for specific types of tasks
5. **Check out helper scripts**: See `scripts/` directory for convenient wrappers

---

## Need Help?

- Check the main [README.md](../README.md) for detailed documentation
- See [CURSOR_USAGE.md](CURSOR_USAGE.md) for Cursor-specific usage examples
- Check MongoDB Atlas logs if you're having database issues
- Verify your API keys are active and have credits/quota remaining

