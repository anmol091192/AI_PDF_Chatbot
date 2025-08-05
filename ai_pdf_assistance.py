# -*- coding: utf-8 -*-
"""
AI PDF Assistant - Chatbot
A Gradio-based chatbot that answers questions about any PDF document using RAG (Retrieval Augmented Generation)
"""

import os
import gradio as gr
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify that the API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Global variables to store the current document processing state
current_qa_chain = None
current_vectorstore = None

def create_demo_documents():
    """Create demo documents when no PDF is available"""
    from langchain.schema import Document
    print("⚠️  Running in demo mode with sample documents")
    
    return [
        Document(page_content="This is a demo document about general information. You can upload any PDF document to get started with real content.", metadata={"source": "demo", "page": 1}),
        Document(page_content="Sample content for demonstration purposes. The AI assistant can answer questions about any PDF document you upload.", metadata={"source": "demo", "page": 2}),
        Document(page_content="For best results, upload a PDF document and ask specific questions about its content, structure, or key information.", metadata={"source": "demo", "page": 3}),
        Document(page_content="The system supports various types of documents including reports, manuals, research papers, and other text-based PDFs.", metadata={"source": "demo", "page": 4}),
        Document(page_content="Upload your document using the file upload interface and start asking questions to get AI-powered insights.", metadata={"source": "demo", "page": 5})
    ]

def process_pdf_file(pdf_path):
    """Process a PDF file and return document chunks"""
    try:
        print(f"📄 Loading PDF: {pdf_path}")
        pdf_loader = PyPDFLoader(pdf_path)
        pdf_pages = pdf_loader.load_and_split()
        print(f"✅ Loaded {len(pdf_pages)} pages from PDF")
        
        if pdf_pages:
            print("First 200 characters:", pdf_pages[0].page_content[:200])
            
            # Split the documents
            doc_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
            split_texts = doc_splitter.split_documents(pdf_pages)
            print(f"✅ Split into {len(split_texts)} chunks")
            
            return split_texts
        else:
            print("⚠️  No content found in PDF")
            return create_demo_documents()
            
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        return create_demo_documents()

def initialize_qa_chain(documents):
    """Initialize the QA chain with processed documents"""
    global current_qa_chain, current_vectorstore
    
    try:
        print("🔄 Creating embeddings and vector store...")
        print(f"📊 Processing {len(documents)} document chunks...")
        
        # Check if using demo vs real PDF content
        if documents[0].metadata.get("source") == "demo":
            print("🚨 Using DEMO documents (no PDF uploaded yet)")
        else:
            print("📄 Using UPLOADED PDF content")
            
        openai_embed = OpenAIEmbeddings()
        current_vectorstore = Chroma.from_documents(documents, embedding=openai_embed)
        print("✅ Vector store created successfully!")

        # Setup Chat model
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        print("✅ Chat model initialized!")

        # Create Retrieval-based QA Chain
        current_qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=current_vectorstore.as_retriever(),
            return_source_documents=False
        )
        print("✅ QA Chain created successfully!")
        return current_qa_chain
        
    except Exception as e:
        print(f"❌ Error initializing QA chain: {e}")
        return None

def upload_and_process_pdf(pdf_file):
    """Handle PDF file upload and processing"""
    global current_qa_chain
    
    if pdf_file is None:
        return "⚠️ Please upload a PDF file first.", []
    
    try:
        # Process the uploaded PDF
        documents = process_pdf_file(pdf_file)
        
        # Initialize QA chain with new documents
        qa_chain = initialize_qa_chain(documents)
        
        if qa_chain:
            filename = os.path.basename(pdf_file)
            success_msg = f"✅ Successfully processed '{filename}'! You can now ask questions about this document."
            welcome_chat = [{"role": "assistant", "content": f"Hello! I've successfully processed your PDF document '{filename}'. You can now ask me questions about its content. What would you like to know?"}]
            return success_msg, welcome_chat
        else:
            return "❌ Error processing PDF. Please try again.", []
            
    except Exception as e:
        print(f"❌ Error in upload_and_process_pdf: {e}")
        return f"❌ Error processing PDF: {str(e)}", []

def respond(message, history):
    global current_qa_chain
    
    if not message.strip():
        return "", history
    
    if current_qa_chain is None:
        error_msg = "⚠️ No document loaded. Please upload a PDF file first."
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return "", history
    
    try:
        print(f"🤔 Processing question: {message}")
        answer = current_qa_chain.run(message)
        print(f"✅ Generated answer: {answer[:100]}...")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        answer = f"⚠️ Error: {e}"
    
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    return "", history

# Initialize with demo documents only
print("🚀 Initializing AI PDF Assistant...")
initial_documents = create_demo_documents()
current_qa_chain = initialize_qa_chain(initial_documents)

print("🚀 Starting Gradio interface...")

with gr.Blocks(title="AI PDF Assistant") as demo:
    gr.Markdown("# 📄 AI PDF Assistant")
    gr.Markdown("Upload any PDF document and ask questions about its content using AI-powered search!")
    
    with gr.Row():
        with gr.Column(scale=1):
            # PDF Upload Section
            gr.Markdown("### 📄 Upload PDF Document")
            pdf_upload = gr.File(
                label="Upload PDF File",
                file_types=[".pdf"],
                type="filepath"
            )
            upload_status = gr.Textbox(
                label="Status",
                value="Ready to upload PDF...",
                interactive=False
            )
            process_btn = gr.Button("Process PDF", variant="primary")
            
        with gr.Column(scale=2):
            # Chat Section
            gr.Markdown("### 💬 Chat with Your Document")
            chatbot = gr.Chatbot(
                label="AI Assistant", 
                height=400,
                placeholder="Upload a PDF file and start asking questions!",
                type="messages"
            )
            user_input = gr.Textbox(
                placeholder="Ask questions about the uploaded document...",
                label="Your Question",
                scale=4
            )
            
            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary", scale=1)
                clear_btn = gr.Button("Clear Chat", scale=1)
    
    # Event handlers
    process_btn.click(
        fn=upload_and_process_pdf,
        inputs=[pdf_upload],
        outputs=[upload_status, chatbot]
    )
    
    user_input.submit(
        fn=respond,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot]
    )
    
    submit_btn.click(
        fn=respond,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot]
    )
    
    clear_btn.click(
        fn=lambda: ([], "Chat cleared. You can continue asking questions."),
        outputs=[chatbot, upload_status]
    )
    
    # Add some example questions
    gr.Markdown("""
    ### 💡 Example Questions to Try:
    - What are the main topics covered in this document?
    - Can you summarize the key points from the document?
    - What does the document say about [specific topic]?
    - Are there any requirements, procedures, or guidelines mentioned?
    - What are the important dates, numbers, or statistics in the document?
    - Can you explain [specific section] in simple terms?
    """)

if __name__ == "__main__":
    demo.launch()