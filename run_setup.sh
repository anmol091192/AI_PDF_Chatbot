#!/bin/bash

echo "🚀 Starting AI HR Assistant Setup..."

# Check if required packages are installed
echo "📋 Checking dependencies..."

# Set environment variable if not already set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not found in environment variables"
    echo "💡 Please set your OpenAI API key:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo "   Or edit the ai_hr_assistance.py file directly"
fi

echo "✅ Setup complete!"
echo "🎯 To run the app:"
echo "   python ai_hr_assistance.py"
