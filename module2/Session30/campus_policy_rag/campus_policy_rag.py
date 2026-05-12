import os
import math
from pathlib import Path

import chromadb
import openai
from pypdf import PdfReader

POLICY_DIR = Path(__file__).parent / "policy_documents"
DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "campus_policies"

OPENAI_MODEL_EMBEDDING = "text-embedding-3-small"
OPENAI_MODEL_CHAT = "gpt-3.5-turbo"


def infer_policy_type(filename: str) -> str:
    lower = filename.lower()
    if "hostel" in lower:
        return "hostel"
    if "refund" in lower:
        return "refund"
    if "library" in lower:
        return "library"
    if "withdrawal" in lower or "course" in lower:
        return "withdrawal"
    return "general"


def load_pdf_texts(policy_dir: Path):
    pdf_paths = sorted(policy_dir.glob("*.pdf"))
    documents = []

    for path in pdf_paths:
        reader = PdfReader(path)
        for page_number, page in enumerate(reader.pages, start=1):
            raw_text = page.extract_text() or ""
            cleaned = clean_text(raw_text)
            if cleaned:
                documents.append(
                    {
                        "source": path.name,
                        "page": page_number,
                        "policy_type": infer_policy_type(path.name),
                        "text": cleaned,
                    }
                )
        print(f"Loaded {len(reader.pages)} pages from: {path.name}")

    return documents


def clean_text(text: str) -> str:
    return " ".join(text.split())


def split_text_into_chunks(text: str, chunk_size: int = 150, overlap_ratio: float = 0.15):
    words = text.split()
    if not words:
        return []

    overlap = max(1, math.floor(chunk_size * overlap_ratio))
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap

    return chunks


def create_embeddings(texts):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set in environment variables.")

    openai.api_key = api_key
    response = openai.Embeddings.create(model=OPENAI_MODEL_EMBEDDING, input=texts)
    return [item["embedding"] for item in response["data"]]


def setup_chroma_collection(path: Path, collection_name: str):
    path.mkdir(parents=True, exist_ok=True)
    try:
        client = chromadb.PersistentClient(path=str(path))
    except Exception:
        client = chromadb.Client()
    return client.get_or_create_collection(name=collection_name)


def index_documents(collection, documents):
    chunk_texts = []
    metadatas = []
    ids = []
    for doc_index, item in enumerate(documents, start=1):
        chunks = split_text_into_chunks(item["text"])
        for chunk_index, chunk in enumerate(chunks, start=1):
            chunk_id = f"{item['source']}::page{item['page']}::chunk{chunk_index}"
            chunk_texts.append(chunk)
            metadatas.append(
                {
                    "source": item["source"],
                    "page": item["page"],
                    "policy_type": item["policy_type"],
                }
            )
            ids.append(chunk_id)

    if not chunk_texts:
        return 0

    embeddings = create_embeddings(chunk_texts)
    collection.upsert(
        ids=ids,
        documents=chunk_texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    return len(chunk_texts)


def retrieve_relevant_chunks(collection, query: str, top_k: int = 3):
    query_embedding = create_embeddings([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append(
            {
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )
    return chunks


def build_prompt(query: str, chunks):
    context_text = "\n\n".join(
        [f"- {c['text']} (Source: {c['metadata']['source']} page {c['metadata']['page']})" for c in chunks]
    )
    return (
        "You are a helpful campus policy assistant. Answer the student question using only the policy context below. "
        "If the answer is not contained in the provided context, respond with: I don't have that information. "
        "Keep the response short and student-friendly.\n\n"
        f"Policy Context:\n{context_text}\n\n"
        f"Student Question: {query}\n\nAnswer:"
    )


def generate_answer(query: str, chunks):
    prompt = build_prompt(query, chunks)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set in environment variables.")

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL_CHAT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=250,
    )
    return response["choices"][0]["message"]["content"].strip()


def answer_question(collection, query: str):
    chunks = retrieve_relevant_chunks(collection, query)
    print(f"Retrieved {len(chunks)} relevant chunks.")
    return generate_answer(query, chunks)


if __name__ == "__main__":
    print("Building campus policy knowledge base...")
    documents = load_pdf_texts(POLICY_DIR)
    if not documents:
        raise FileNotFoundError("No PDF policy documents found in policy_documents/.")

    collection = setup_chroma_collection(DB_DIR, COLLECTION_NAME)
    total_chunks = index_documents(collection, documents)
    print(f"Total chunks created: {total_chunks}")
    print("Knowledge base is ready. Collection:", COLLECTION_NAME)

    queries = [
        "Can I get a refund after dropping a course?",
        "What is the deadline for returning a library book?",
        "Are hostel visitors allowed on weekends?",
    ]

    for query in queries:
        print("\n==============================")
        print(f"User Query: {query}")
        answer = answer_question(collection, query)
        print("Answer:")
        print(answer)
