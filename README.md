# 🚀 ANRO AI

## Intelligent Document Intelligence & Retrieval-Augmented Generation Platform

ANRO AI is an intelligent document intelligence platform designed to help users securely upload, process, search, and interact with their documents using Artificial Intelligence and Retrieval-Augmented Generation (RAG).

The platform combines document processing, semantic search, vector-based retrieval, context-aware prompt generation, and Large Language Model (LLM) response generation to provide intelligent answers grounded in the user's document content.

---

## 🌟 Project Overview

Traditional document systems require users to manually search through large amounts of information.

ANRO AI simplifies this process by allowing users to:

* Upload documents
* Process and extract document content
* Convert content into searchable representations
* Retrieve relevant information using semantic search
* Ask natural-language questions
* Generate context-aware AI responses
* Retrieve relevant document sources

The goal of ANRO AI is to create a practical, intelligent, and scalable document interaction system using modern AI technologies.

---

# ✨ Key Features

## 🔐 Secure Authentication

ANRO AI provides authenticated access to the application using JWT-based authentication.

Users can securely:

* Register
* Login
* Access protected APIs
* Upload documents
* Interact with the RAG system

---

## 📄 Intelligent Document Processing

The platform supports document ingestion and processing.

The document processing workflow includes:

1. Document Upload
2. File Validation
3. Content Extraction
4. Text Processing
5. Document Chunking
6. Metadata Management
7. Vector Storage

This allows large documents to become searchable and usable by the RAG system.

---

## 🔎 Semantic Search

ANRO AI uses semantic retrieval to find relevant document content based on the meaning of the user's question rather than relying only on exact keyword matching.

This allows the system to retrieve contextually relevant information from uploaded documents.

---

## 🧠 Retrieval-Augmented Generation

ANRO AI uses a Retrieval-Augmented Generation architecture.

The system first retrieves relevant document chunks and then provides those chunks as context to the AI generation service.

This helps the AI generate responses based on the user's document content.

---

## 💬 AI-Powered Document Question Answering

Users can ask natural-language questions about their documents.

Example:

> What is the cost of capital?

The system processes the question, retrieves relevant document information, builds contextual information, and generates an AI-powered response.

---

## 📚 Context-Aware Responses

The RAG pipeline uses retrieved document content as context before generating the final response.

This helps improve:

* Relevance
* Context awareness
* Document grounding
* Answer quality

---

## 📊 Retrieval Statistics

The system provides information about the retrieval process, including:

* Number of retrieved results
* Context statistics
* Prompt statistics
* Retrieved document results

---

# 🏗️ System Architecture

The high-level architecture of ANRO AI follows this workflow:

```text
                    ┌──────────────────────┐
                    │      User / Client   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Authentication     │
                    │      JWT / User      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Document Upload    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Processing  │
                    │ Text Extraction      │
                    │ Chunking             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Vector Database    │
                    │   Semantic Storage   │
                    └──────────┬───────────┘
                               │
                               │
             ┌─────────────────▼─────────────────┐
             │          User Question           │
             └─────────────────┬─────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Retrieval Service    │
                    │ Semantic Search      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relevant Chunks      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ RAG Generation       │
                    │ Context + Prompt     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ AI / LLM Generation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Final AI Answer      │
                    │ + Retrieved Sources  │
                    └──────────────────────┘
```

---

# 🔄 RAG Workflow

The ANRO AI RAG pipeline follows these steps:

```text
User Question
      ↓
Question Validation
      ↓
Document Retrieval
      ↓
Semantic Search
      ↓
Relevant Chunks
      ↓
Context Building
      ↓
Prompt Construction
      ↓
LLM Generation
      ↓
AI Answer
      ↓
Retrieved Results & Statistics
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* REST API

## Authentication

* JWT Authentication
* Protected API Routes
* User Authentication

## AI & RAG

* Retrieval-Augmented Generation
* Semantic Search
* Vector Retrieval
* LLM Integration
* Context-Aware Prompting

## Document Intelligence

* Document Ingestion
* Text Extraction
* Text Chunking
* Metadata Processing

## Vector Storage

* ChromaDB / Vector Database

## Development

* Git
* GitHub
* VS Code
* Python Virtual Environment

---

# 📂 Project Structure

The project follows a modular architecture.

```text
ANRO-AI/
│
├── app/
│   │
│   ├── api/
│   │   ├── routes_auth.py
│   │   ├── routes_documents.py
│   │   └── routes_rag.py
│   │
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   └── ...
│   │
│   ├── document_processing/
│   │   ├── document_ingestion_manager.py
│   │   ├── document_processor.py
│   │   └── ...
│   │
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   ├── retrieval_service.py
│   │   ├── rag_generation_service.py
│   │   └── ...
│   │
│   ├── database/
│   │   └── ...
│   │
│   └── core/
│       └── ...
│
├── data/
│   ├── documents/
│   └── vector_db/
│
├── tests/
│
├── frontend/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

> Note: The exact folder structure may vary depending on the current implementation and future project updates.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ANRO-AI.git
```

Navigate to the project:

```bash
cd ANRO-AI
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
APP_NAME=ANRO AI

SECRET_KEY=your_secret_key_here

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=your_model_name
```

Never commit the real `.env` file to GitHub.

Use `.env.example` as a safe template.

---

# ▶️ Running the Application

Start the backend application using the project's configured startup command.

Example:

```bash
py run.py
```

Or, if running directly with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API can then be accessed through the configured local server.

---

# 📡 API Endpoints

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
```

---

## Documents

```text
POST /api/documents/upload
GET  /api/documents
```

---

## RAG

```text
POST /api/rag/ask
GET  /api/rag/status
GET  /api/rag/conversation
DELETE /api/rag/conversation
```

> API endpoints may change as the project continues to evolve.

---

# 💬 Example RAG Request

Example request:

```json
{
    "question": "What is cost of capital?",
    "document_id": "your-document-id"
}
```

The RAG system processes the question and retrieves relevant information before generating an AI response.

---

# 🧠 RAG Pipeline

The core pipeline is implemented through the `RAGPipeline` service.

The pipeline performs:

```text
Question
    ↓
Validation
    ↓
Retrieval Service
    ↓
Relevant Document Chunks
    ↓
RAG Generation Service
    ↓
Context Building
    ↓
Prompt Generation
    ↓
LLM
    ↓
Final Answer
```

---

# 🔒 Security

ANRO AI is designed with security considerations including:

* JWT-based authentication
* Protected API endpoints
* Environment-based configuration
* Sensitive credentials excluded from Git
* `.env` protection using `.gitignore`

For production deployment, additional security measures should be implemented, including:

* HTTPS
* Secure secret management
* Rate limiting
* Input validation
* Production database configuration
* Access control
* Logging and monitoring

---

# 🧪 Testing

Before deployment, test the complete workflow:

```text
1. Start Backend
        ↓
2. Register User
        ↓
3. Login
        ↓
4. Receive JWT Token
        ↓
5. Upload Document
        ↓
6. Process Document
        ↓
7. Select Document
        ↓
8. Ask Question
        ↓
9. Retrieve Relevant Chunks
        ↓
10. Generate AI Answer
```

---

# 🚀 Future Roadmap

Future versions of ANRO AI may include:

* Multi-document conversations
* Document-specific retrieval filters
* Advanced citation generation
* Conversation history
* Streaming AI responses
* Multiple LLM provider support
* Advanced document formats
* Role-based access control
* Cloud deployment
* AI-powered document summarization
* Document comparison
* Enterprise document intelligence
* Advanced analytics dashboard

---

# 🌟 Vision

The long-term vision of ANRO AI is to build a powerful AI-driven document intelligence platform that allows users and organizations to interact with their knowledge base using natural language.

The goal is to transform static documents into intelligent, searchable, and interactive sources of knowledge.

---

# 👨‍💻 Project Credits

## ANRO AI

**Intelligent Document Intelligence & Retrieval-Augmented Generation Platform**

**Created & Developed by:**
Rohit Prajapati

**AI Development Partner:**
ChatGPT

---

# 📜 License

This project is currently intended for educational, portfolio, and development purposes.

A formal open-source license may be added in a future release.

---

# ⭐ Support

If you find this project interesting, consider starring the repository on GitHub.

Thank you for exploring **ANRO AI**! 🚀

---

## ANRO AI

### Built with Python, AI, RAG, and a vision for intelligent document interaction

**Created by Rohit Prajapati**
**AI Development Partner: ChatGPT**
