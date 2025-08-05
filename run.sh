#!/bin/bash

# AI HR Assistant Startup Script

echo "🚀 Starting AI HR Assistant..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please copy .env.example to .env and add your OpenAI API key"
    cp .env.example .env
    echo "✏️  Edit .env file and add your OPENAI_API_KEY, then run this script again"
    exit 1
fi

# Run the application
echo "🎯 Starting the application..."
python ai_pdf_assistance.py
