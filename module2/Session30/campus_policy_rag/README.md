# Campus Policy RAG Assistant

A Python-based Retrieval-Augmented Generation (RAG) system that answers student questions using campus policy documents. Instead of relying on general knowledge, the assistant retrieves relevant policy excerpts and generates answers grounded only in the retrieved context.

## Features

- **Multi-document PDF support**: Load and index multiple policy documents (hostel, refund, library, etc.)
- **Semantic search**: Retrieve the 3 most relevant policy chunks for each query using embeddings
- **Grounded responses**: Answers come exclusively from policy documents—no hallucinations
- **Policy metadata tracking**: Each retrieved chunk tracks its source file, page number, and policy type
- **Persistent vector storage**: ChromaDB stores embeddings for fast retrieval

## Project Structure

```
campus_policy_rag/
├── campus_policy_rag.py          # Main RAG implementation
├── requirements.txt               # Dependencies
├── .gitignore                     # Git ignore config (excludes API keys, DB)
├── README.md                      # This file
├── policy_documents/              # Store your policy PDFs here
│   ├── hostel_policy.pdf
│   ├── refund_policy.pdf
│   └── library_policy.pdf
└── chroma_db/                     # Created automatically by ChromaDB
    └── (vector database files)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `openai` — Embedding and chat models
- `chromadb` — Vector database
- `pypdf` — PDF text extraction

### 2. Set Your API Key

Export your OpenAI API key to the environment:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
```

**Windows (Command Prompt):**
```cmd
setx OPENAI_API_KEY "your-openai-api-key"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Add Policy Documents

Place your policy PDF files in the `policy_documents/` folder. The script infers the policy type from the filename:
- `hostel_policy.pdf` → hostel
- `refund_policy.pdf` → refund
- `library_policy.pdf` → library
- `course_withdrawal_policy.pdf` → withdrawal

## Running the Script

```bash
python campus_policy_rag.py
```

### Example Output

```
Building campus policy knowledge base...
Loaded 1 pages from: hostel_policy.pdf
Loaded 1 pages from: library_policy.pdf
Loaded 1 pages from: refund_policy.pdf
Total chunks created: 8
Knowledge base is ready. Collection: campus_policies

==============================
User Query: Can I get a refund after dropping a course?
Retrieved 3 relevant chunks.
Answer:
According to the refund policy, students may request a refund within 14 days of course registration. If a student drops a course before the refund deadline, the tuition fee may be reimbursed minus administrative charges. However, after the deadline, refunds are not guaranteed and are handled case by case by the finance office.

==============================
User Query: What is the deadline for returning a library book?
Retrieved 3 relevant chunks.
Answer:
According to the library policy, library books must be returned within 21 days from the checkout date. Overdue fines apply after the return deadline at a daily rate set by the library office.

==============================
User Query: Are hostel visitors allowed on weekends?
Retrieved 3 relevant chunks.
Answer:
Yes, according to the hostel policy, visitors are allowed between 8 AM and 10 PM daily, which includes weekends. However, quiet hours begin at 11 PM and all overnight guests require prior approval from hostel administration. Additionally, no visitors are permitted inside student rooms after 10 PM.
```

## How It Works

### 1. **Document Loading**
The script reads all PDF files from `policy_documents/` using `pypdf.PdfReader` and extracts text from each page.

### 2. **Text Cleaning**
Raw text is cleaned by removing extra whitespace and newlines to prepare for chunking.

### 3. **Chunking with Overlap**
Text is split into fixed-size chunks (default: 150 words) with 15% overlap to preserve context across boundaries.

### 4. **Embedding Generation**
Each chunk is converted to a dense vector embedding using OpenAI's `text-embedding-3-small` model.

### 5. **Vector Storage**
Embeddings and metadata (source, page, policy type) are stored in a persistent ChromaDB collection.

### 6. **Query Processing**
When a student asks a question:
- The query is embedded using the same embedding model
- ChromaDB retrieves the top-3 most similar chunks
- The retrieved chunks are passed to GPT-3.5-turbo with a grounding prompt

### 7. **Grounded Answer Generation**
The LLM generates a response using only the retrieved policy context. If the context doesn't contain the answer, it responds with "I don't have that information."

## Configuration

Edit `campus_policy_rag.py` to adjust:

```python
OPENAI_MODEL_EMBEDDING = "text-embedding-3-small"  # Embedding model
OPENAI_MODEL_CHAT = "gpt-3.5-turbo"                # Chat/generation model
COLLECTION_NAME = "campus_policies"                # ChromaDB collection name
```

Customize chunking parameters:
```python
def split_text_into_chunks(text: str, chunk_size: int = 150, overlap_ratio: float = 0.15):
```

- `chunk_size`: Words per chunk (100–200 recommended)
- `overlap_ratio`: Overlap percentage (0.1–0.2 recommended)

## Adding More Policies

1. Add your PDF file to `policy_documents/`
2. Ensure the filename includes the policy type (e.g., `discipline_policy.pdf`)
3. Run the script—it will automatically detect and index the new document

## API Key Security

The script reads your API key from the `OPENAI_API_KEY` environment variable. Never hardcode it or commit it to version control.

The `.gitignore` file excludes:
- `.env` files (if you use a .env file)
- `api_key*.txt` (for any local key files)
- `chromadb/` (database files—recreated on each run)

## Testing Custom Queries

Edit the `queries` list in the `if __name__ == "__main__"` block to test with your own questions:

```python
queries = [
    "Your custom question here?",
    "Another question?",
]
```

## Notes

- The first run will build the knowledge base, which may take a few seconds
- Subsequent runs will reuse the ChromaDB collection (no re-indexing)
- To force a rebuild, delete the `chroma_db/` folder
- All answers are grounded in retrieved policy text—the model will not invent information

## Troubleshooting

**Error: `ModuleNotFoundError: No module named 'openai'`**
- Run `pip install -r requirements.txt` to install dependencies

**Error: `OPENAI_API_KEY is not set in environment variables`**
- Ensure your API key is exported: `setx OPENAI_API_KEY "your-key"`
- Restart your terminal after setting the environment variable

**No PDFs found in `policy_documents/`**
- Check that your PDF files are in the correct folder
- Filenames should include the policy type (e.g., `hostel_policy.pdf`)

**Empty or irrelevant answers**
- Your policy documents may not contain the answer
- Add more relevant policy text to the documents
- Increase `top_k` in `retrieve_relevant_chunks()` to retrieve more chunks
