
#python3 --version   Python 3.14.3
#python3 -m venv venv
#venv\Scripts\activate.bat
# install chromaDB ---- pip install chromadb
#pip install sentence-transformers
#python3 vectorSearch.py 

import chromadb
from sentence_transformers import SentenceTransformer

# Prepare Sample data
policies = [
    {
        "id": "p1",
        "text": "Employees are entitled to 20 days of paid annual leave per year.",
        "metadata": {"category": "leave", "version": 1}
    },
    {
        "id": "p2",
        "text": "Company provides health insurance benefits to all full-time employees.",
        "metadata": {"category": "benefits", "version": 1}
    },
    {
        "id": "p3",
        "text": "Employees must adhere to the company code of conduct at all times.",
        "metadata": {"category": "conduct", "version": 1}
    },
    {
        "id": "p4",
        "text": "Maternity leave of 12 weeks is available to eligible employees.",
        "metadata": {"category": "leave", "version": 1}
    },
    {
        "id": "p5",
        "text": "Performance bonuses are awarded annually based on company results.",
        "metadata": {"category": "benefits", "version": 1}
    },
]

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Create a client for Chroma DB
client = chromadb.PersistentClient(path="./hr_chroma_store")

# Create a collection
collection = client.get_or_create_collection(
    name="hr_policies",
    embedding_function=None
)


# Embed and upsert documents
for policy in policies:
    embedding = model.encode(policy["text"]).tolist()
    collection.upsert(
        ids=[policy["id"]],
        documents=[policy["text"]],
        metadatas=[policy["metadata"]],
        embeddings=[embedding]
    )

# --- Show collection info ---
print("Collection count:", collection.count())
print("Peek:", collection.peek())

# --- Search A: Natural language question ---
query_a = "How many vacation days do employees get?"
query_emb_a = model.encode(query_a).tolist()
results_a = collection.query(query_embeddings=[query_emb_a], n_results=3)

print("\nSearch A results:")
for rank, (id_, doc, meta) in enumerate(zip(results_a["ids"][0], results_a["documents"][0], results_a["metadatas"][0]), start=1):
    print(f"Rank {rank} | ID: {id_} | Snippet: {doc[:50]}... | Metadata: {meta}")

# --- Search B: Filter by category ---
query_b = "What insurance benefits are provided?"
query_emb_b = model.encode(query_b).tolist()
results_b = collection.query(query_embeddings=[query_emb_b], where={"category": "benefits"}, n_results=2)

print("\nSearch B results (category=benefits):")
for rank, (id_, doc, meta) in enumerate(zip(results_b["ids"][0], results_b["documents"][0], results_b["metadatas"][0]), start=1):
    print(f"Rank {rank} | ID: {id_} | Snippet: {doc[:50]}... | Metadata: {meta}")

# --- Update: Add new or update existing policy ---
new_policy = {
    "id": "p6",
    "text": "Employees are eligible for flexible work-from-home arrangements.",
    "metadata": {"category": "benefits", "version": 1}
}
embedding_new = model.encode(new_policy["text"]).tolist()
collection.upsert(
    ids=[new_policy["id"]],
    documents=[new_policy["text"]],
    metadatas=[new_policy["metadata"]],
    embeddings=[embedding_new]
)

# --- Search after update ---
query_c = "Tell me about work from home benefits."
query_emb_c = model.encode(query_c).tolist()
results_c = collection.query(query_embeddings=[query_emb_c], where={"category": "benefits"}, n_results=3)

print("\nSearch after update (category=benefits):")
for rank, (id_, doc, meta) in enumerate(zip(results_c["ids"][0], results_c["documents"][0], results_c["metadatas"][0]), start=1):
    print(f"Rank {rank} | ID: {id_} | Snippet: {doc[:50]}... | Metadata: {meta}")
