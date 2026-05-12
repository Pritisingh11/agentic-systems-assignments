# python3 -m venv venv
# source venv/bin/activate

# install chromaDB ---- pip install chromadb
# embeddings - OpenAI API or sentence-transformers
#pip install sentence-transformers

import chromadb
from sentence_transformers import SentenceTransformer

# Prepare Sample data
records = [
    {
        "id": "doc1",
        "text": "Customers can return products within 30 days of delivery.",
        "metadata": {"category": "returns", "source": "policy"}
    },
    {
        "id": "doc2",
        "text": "Refunds are processed within 5 to 7 business days after the return is approved.",
        "metadata": {"category": "returns", "source": "policy"}
    },
    {
        "id": "doc3",
        "text": "Orders above 499 rupees qualify for free shipping.",
        "metadata": {"category": "shipping", "source": "faq"}
    },
    {
        "id": "doc4",
        "text": "You can reset your password from the account settings page.",
        "metadata": {"category": "account", "source": "help_center"}
    },
    {
        "id": "doc5",
        "text": "Express delivery orders usually arrive within 24 to 48 hours.",
        "metadata": {"category": "shipping", "source": "faq"}
    },
    {
        "id": "doc6",
        "text": "If your payment fails, try another card or use UPI.",
        "metadata": {"category": "payments", "source": "help_center"}
    }
]

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert documents into embeddings.
# documents = []
# for record in records:
#     documents.append(record['text'])

documents = [record["text"] for record in records]
doc_ids = [record["id"] for record in records]
doc_metadatas = [record["metadata"] for record in records]

document_embeddings = model.encode(documents, convert_to_numpy=True).tolist()
# [[.....], [.....], [.....], [.....], [.....], [.....]]

# Create a client for Chroma DB
client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection
collection = client.get_or_create_collection(
    name="knowledge_vector_db",
    embedding_function=None
)

# Store the embeddings into collection
# upsert - update + insert
collection.upsert(
    ids=doc_ids,
    documents=documents,
    metadatas=doc_metadatas,
    embeddings=document_embeddings
)

#print("Number of records in collection: ", collection.count())
#print("Stored records in collection: ", collection.peek())

user_query = "I want to return my shoes and get my money back"

# convert the user query into embedding.
query_embedding = model.encode([user_query], convert_to_numpy=True).tolist()

# Perform Similarity Search
results = collection.query(
    query_embeddings=query_embedding,
    n_results=1
)

#print("===============================")
#print("Results - ", results)

user_query_2 = "How fast I will receive my order ?"

query_embedding_2 = model.encode([user_query_2], convert_to_numpy=True).tolist()

results_2 = collection.query(
    query_embeddings=query_embedding_2,
    n_results=2,
    where={"category":"shipping"}
)

#print("Results - ", results_2)

new_record = {
    "id": "doc7",
    "text": "Cancelled orders are refunded to the original payment method.",
    "metadata": {"category": "payments", "source": "policy"}
}

new_embedding = model.encode([new_record["text"]], convert_to_numpy=True).tolist()

collection.upsert(
    ids=[new_record["id"]],
    documents=[new_record["text"]],
    metadatas=[new_record["metadata"]],
    embeddings=new_embedding
)

#print("Number of records in collection: ", collection.count())
#print("Stored records in collection: ", collection.peek())



user_query_3 = "How will I refund get the refund for a cancelled order?"

query_embedding_3 = model.encode([user_query_3], convert_to_numpy=True).tolist()

results_3 = collection.query(
    query_embeddings=query_embedding_3,
    n_results=2,
    where={"category":"payments"}
)

print("Results - ", results_3)

# Code is present in the notes for your reference.
# Try to use OpenAI embedding model in place of sentence-transformer.
# Try to update an existing document in the collection and then try to query.

