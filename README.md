# AI PDF Assistant - Universal PDF Chatbot

A Gradio-based chatbot that can answer questions about **any PDF document** using RAG (Retrieval Augmented Generation). Upload your own PDF files and get instant AI-powered answers!

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "AI PDF Assistant"
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-actual-openai-api-key-here
```

### 5. Run the Application
```bash
python ai_pdf_assistance.py
```

> **Note**: The main script is named `ai_pdf_assistance.py` for historical reasons. You can rename it to `ai_pdf_assistant.py` or similar for better consistency with the generic PDF functionality.

The app will start and display:
- Local URL: http://127.0.0.1:7860  
- Public URL: A shareable link (if share=True)

### 6. Upload and Chat with Your PDF
1. Open the web interface
2. Upload any PDF file using the "Upload PDF File" button
3. Click "Process PDF" to analyze the document
4. Start asking questions about your document!

## ✨ Features

- 🤖 AI-powered chat interface using OpenAI's GPT-3.5-turbo
- 📄 **Upload any PDF document** through the web interface
- 🔍 Semantic search through document chunks using ChromaDB
- 💬 User-friendly Gradio web interface with file upload
- 🔄 Real-time question answering about uploaded documents
- 🔒 Secure API key management with environment variables
- 📋 Automatic fallback to demo mode if no PDF is uploaded
- 🎯 Support for multiple document formats and sizes

## �️ How It Works

1. **Document Upload**: Users can upload any PDF file through the web interface
2. **Document Processing**: PDF is loaded and split into manageable chunks
3. **Embedding**: Text chunks are converted to embeddings using OpenAI
4. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
5. **Question Processing**: User questions are matched with relevant document chunks
6. **Answer Generation**: GPT-3.5-turbo generates contextual answers based on retrieved content

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for OpenAI API calls

## 🚀 Deployment Options

### Option 1: Hugging Face Spaces (Recommended - Free)
1. Create account on [Hugging Face](https://huggingface.co/)
2. Create a new Space with Gradio SDK
3. Upload your files to the Space
4. Add `OPENAI_API_KEY` in Space settings → Secrets
5. Your app will be live at `https://huggingface.co/spaces/username/space-name`

### Option 2: Streamlit Cloud (Free)
1. Convert to Streamlit (requires code changes)
2. Deploy to [Streamlit Cloud](https://streamlit.io/cloud)

### Option 3: Railway (Free tier available)
1. Connect your GitHub repo to [Railway](https://railway.app/)
2. Add `OPENAI_API_KEY` as environment variable
3. Deploy with one click

### Option 4: Google Colab (Free but temporary)
1. Upload notebook to Google Colab
2. Run and use the public URL
3. Note: Session expires when inactive

### Option 5: Local Network
```bash
# Run on local network (accessible to other devices on same network)
python ai_pdf_assistance.py
```

> **Note**: Consider renaming the script to `ai_pdf_assistant.py` for better clarity about its generic PDF functionality.

## 🔧 Configuration

- **Model**: Change `model="gpt-3.5-turbo"` to `"gpt-4"` for better responses (higher cost)
- **Chunk Size**: Modify `chunk_size=1024` in `RecursiveCharacterTextSplitter` for different text processing
- **Port**: Change `server_port=7860` to use a different port

## ⚠️ Important Notes

- Keep your OpenAI API key secure and never commit it to the repository
- Monitor your OpenAI API usage to avoid unexpected charges
- The demo mode uses sample data when no PDF is provided

## Screenshot


