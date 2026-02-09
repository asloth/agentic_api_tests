# Agentic API Tests

A comprehensive framework for testing APIs using intelligent agents powered by Google's Agent Development Kit (ADK) and Vertex AI. This project leverages agentic workflows to automatically generate test data and execute intelligent tests on API endpoints.

## 🎯 Overview

**Agentic API Tests** is a Python-based system that uses AI agents to:
- **Analyze API Documentation**: Extract and understand API endpoint specifications automatically
- **Generate Test Data**: Create intelligent test datasets based on API schemas
- **Execute Tests**: Run comprehensive tests against APIs using multiple specialized agents
- **Manage Database**: Handle SQLite database operations for test data storage and retrieval

The system employs multiple specialized agents working in coordination:
- **RAG Agent**: Retrieves and analyzes API documentation using Retrieval Augmented Generation
- **Database Agent**: Understands database structure and generates meaningful test data
- **Root Agent**: Orchestrates the workflow between different agents

## 📋 Project Structure

```
agentic_api_tests/
├── main.py                      # Entry point
├── pyproject.toml              # Project dependencies and configuration
├── main_agents/                # Core agent implementations
│   ├── __init__.py            # Vertex AI initialization
│   ├── agent.py               # Agent definitions and session management
│   ├── config.py              # RAG and Vertex AI configuration
│   ├── prompts.py             # System prompts for different agents
│   ├── tools.py               # Custom tools for agents (RAG query, etc.)
│   └── api_docs.md            # Sample API documentation
├── utils/                      # Utility modules
│   ├── connection_db.py        # SQLite database connection handler
│   ├── generate_database.py    # Database initialization and data ingestion
│   └── library_database.db     # SQLite database (generated)
└── .env                        # Environment variables (not included)
```

## 🛠️ Prerequisites

- **Python**: 3.13 or higher
- **Google Cloud Account**: For Vertex AI access
- **Environment Setup**: Proper authentication for Google Cloud

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/asloth/agentic_api_tests.git
cd agentic_api_tests
```

### 2. Create Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### 3. Install Dependencies

Using UV (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

### Dependencies Include:
- `google-adk>=1.19.0` - Agent Development Kit
- `google-cloud-aiplatform>=1.128.0` - Vertex AI integration
- `google-cloud-storage>=3.6.0` - Cloud storage operations
- `google-genai>=1.52.0` - Generative AI models

## 🚀 Quick Start

### 1. Generate the Database

First, initialize the SQLite database with sample data:

```bash
python -m utils.generate_database
```

This creates `utils/library_database.db` with:
- **books** table: Sample book collection
- **users** table: Sample users
- **sales** table: Sales transactions
- **sales_details** table: Sales line items with relationships

### 2. Run the Application

```bash
python main.py
```

Expected output:
```
Hello from agentic-api-tests!
```

### 3. Use the Agents

Import and use agents in your scripts:

```python
from main_agents import agent
from main_agents.prompts import return_instructions_rag_agent, return_instructions_database_agent

# Use RAG agent to analyze API documentation
# Use Database agent to understand and test database operations
```

## 🤖 Agent System

### RAG Agent (API Documentation Analysis)
- Analyzes API documentation files
- Extracts endpoint specifications (HTTP methods, parameters, response structures)
- Provides structured information for test generation
- Returns status codes and error handling details

### Database Agent
- Analyzes SQLite database structure
- Identifies table relationships and foreign keys
- Retrieves sample data
- Helps generate meaningful test data based on actual schema

### Root Agent
- Orchestrates workflow between specialized agents
- Manages session state
- Coordinates multi-step testing processes

## 📊 Database Schema

The system includes a library database with the following tables:

### Books
```sql
book_id (INTEGER, PK)
title (TEXT)
author (TEXT)
published_year (INTEGER)
genre (TEXT)
```

### Users
```sql
user_id (INTEGER, PK)
name (TEXT)
email (TEXT, UNIQUE)
```

### Sales
```sql
sale_id (INTEGER, PK)
user_id (INTEGER, FK → users)
sale_date (TEXT)
total_amount (DECIMAL)
```

### Sales_Details
```sql
sale_id (INTEGER, FK → sales)
book_id (INTEGER, FK → books)
quantity (INTEGER)
PK: (sale_id, book_id)
```

## ⚙️ Configuration

### Vertex AI Configuration
Located in `main_agents/config.py`:
- `PROJECT_ID`: Google Cloud project identifier
- `LOCATION`: Vertex AI location (default: us-central1)

### RAG Configuration
- `DEFAULT_CHUNK_SIZE`: 512 tokens
- `DEFAULT_CHUNK_OVERLAP`: 100 tokens
- `DEFAULT_TOP_K`: 3 results
- `DEFAULT_EMBEDDING_MODEL`: text-embedding-005
- `DEFAULT_CORPUS_NAME`: endpoint-documentation

### Agent Configuration
- `MODEL_NAME`: gemini-2.5-flash
- `RETRY_CONFIG`: 5 attempts with exponential backoff
- Session management: In-memory session service

## 📝 API Documentation Format

The system expects API documentation in the following format (see `main_agents/api_docs.md`):

```markdown
# API Documentation

## Base URL
https://api.example.com

## Authentication
Authorization: Bearer YOUR_API_TOKEN

## Endpoints
- GET /api/endpoint
- POST /api/endpoint
- PUT /api/endpoint/{id}
- DELETE /api/endpoint/{id}
```

## 🔧 Development

### Running Tests
```bash
# Generate database with sample data
python -m utils.generate_database

# Run main application
python main.py
```

### Adding New Agents
1. Create agent definition in `main_agents/agent.py`
2. Define system prompts in `main_agents/prompts.py`
3. Implement custom tools in `main_agents/tools.py`

### Working with Database
Use the `DatabaseConnection` class from `utils/connection_db.py`:

```python
from utils.connection_db import DatabaseConnection

db = DatabaseConnection()
db.connect()
tables = db.get_tables()
schema = db.get_table_schema("books")
results = db.execute_query("SELECT * FROM books LIMIT 5")
db.disconnect()
```

## 🔐 Google Cloud Setup

1. Create a Google Cloud project
2. Enable required APIs:
   - Vertex AI API
   - Cloud Storage API
3. Set up authentication:
   ```bash
   gcloud auth application-default login
   ```
4. Configure environment variables in `.env`

## 📚 API Documentation Example

The project includes `main_agents/api_docs.md` with a sample Customer API demonstrating:
- Multiple HTTP methods (GET, POST, PUT, DELETE)
- Path parameters and query parameters
- Request/response examples
- Status codes and error handling
- Authentication requirements

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact & Support

For questions or support, please open an issue on the GitHub repository.

---

**Last Updated**: December 2025
**Version**: 0.1.0
**Python Version**: 3.13+