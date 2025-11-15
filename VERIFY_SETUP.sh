#!/bin/bash
# Verification script for natural language workflow setup

echo "================================================================"
echo "VERIFYING NATURAL LANGUAGE WORKFLOW SETUP"
echo "================================================================"
echo ""

cd "/Users/subhra.kundu/Desktop/MCP Repo/prompt-saver-mcp"

echo "1. Checking required files..."
echo ""

# Check .cursorrules
if [ -f ".cursorrules" ]; then
    echo "✅ .cursorrules exists"
else
    echo "❌ .cursorrules missing"
    exit 1
fi

# Check helper script
if [ -f "scripts/cursor_prompt_helper.py" ]; then
    echo "✅ cursor_prompt_helper.py exists"
else
    echo "❌ cursor_prompt_helper.py missing"
    exit 1
fi

# Check test file
if [ -f "test_conversation.json" ]; then
    echo "✅ test_conversation.json exists"
else
    echo "❌ test_conversation.json missing"
    exit 1
fi

# Check .env
if [ -f ".env" ]; then
    echo "✅ .env exists"
else
    echo "❌ .env missing - create from .env.example"
    exit 1
fi

echo ""
echo "2. Testing helper script..."
echo ""

# Test help command
python scripts/cursor_prompt_helper.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Helper script runs successfully"
else
    echo "❌ Helper script error"
    exit 1
fi

echo ""
echo "3. Testing preview command..."
echo ""

# Test preview
OUTPUT=$(python scripts/cursor_prompt_helper.py preview --file test_conversation.json --task "Test" 2>&1)
if echo "$OUTPUT" | grep -q "PROMPT PREVIEW"; then
    echo "✅ Preview command works"
else
    echo "❌ Preview command failed"
    echo "$OUTPUT"
    exit 1
fi

echo ""
echo "4. Testing save command..."
echo ""

# Test save (will save the preview from step 3)
OUTPUT=$(python scripts/cursor_prompt_helper.py save --context "Verification test" 2>&1)
if echo "$OUTPUT" | grep -q "Successfully saved prompt"; then
    echo "✅ Save command works"
else
    echo "❌ Save command failed"
    echo "$OUTPUT"
    exit 1
fi

echo ""
echo "================================================================"
echo "✅ ALL CHECKS PASSED!"
echo "================================================================"
echo ""
echo "Your natural language workflow is ready to use!"
echo ""
echo "Next steps:"
echo "1. Open Cursor"
echo "2. Say: 'Generate a prompt preview from our conversation'"
echo "3. Review the preview"
echo "4. Say: 'Save it'"
echo ""
echo "Enjoy! 🎉"
echo ""

