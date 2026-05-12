#python3 --version   Python 3.14.3
#python3 -m venv venv
#venv\Scripts\activate.bat
# install chromaDB ---- pip install chromadb
#pip install sentence-transformers
#pip install openai
#pip install google-generativeai
#python3 vectorSearch.py 

#setx GEMINI_API_KEY "AIzaSyAdp4gUkimmgH6C6JDkG3wJ36D-v4hJK70"

import os
import chromadb
import google.generativeai as genai

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Step 1 — Define HR Policy Documents
POLICY_DOCUMENTS = [
    {
        "id": "leave_policy",
        "text": "Employees are entitled to 20 days of annual leave per calendar year. Sick leave can be availed with medical certification. Unused annual leave up to 5 days may be carried forward to the next year. Extended leave requires prior approval from HR.",
        "metadata": {"category": "Leave Policy", "source": "HR Handbook"}
    },
    {
        "id": "wfh_policy",
        "text": "Employees may work from home up to 2 days per week. Eligibility requires completion of probation. All WFH requests must be approved by the reporting manager at least one day in advance.",
        "metadata": {"category": "Work From Home Policy", "source": "HR Handbook"}
    },
    {
        "id": "appraisal_policy",
        "text": "Appraisals are conducted annually in April. Performance is rated on a 5-point scale. Salary increments are directly linked to appraisal ratings, with higher ratings receiving proportionally higher increments.",
        "metadata": {"category": "Appraisal Policy", "source": "HR Handbook"}
    },
    {
        "id": "code_of_conduct",
        "text": "Employees must maintain professional behavior at all times. Data privacy must be respected, and confidential information should not be shared externally. Any conflict of interest must be disclosed to HR immediately.",
        "metadata": {"category": "Code of Conduct", "source": "HR Handbook"}
    }
]

# Step 2 — Functions

def create_embeddings(texts):
    model = genai.GenerativeModel("text-embedding-004")
    embeddings = []
    for text in texts:
        result = model.embed_content(text)
        embeddings.append(result.embedding)
    return embeddings

def setup_vector_database():
    persistent_client = chromadb.PersistentClient(path="chroma_hr_policy_db")
    collection = persistent_client.get_or_create_collection(
        name="hr_policy_collection"
    )
    return collection

def index_hr_documents(collection):
    for doc in POLICY_DOCUMENTS:
        collection.upsert(
            documents=[doc["text"]],
            metadatas=[doc["metadata"]],
            ids=[doc["id"]]
        )

def retrieve_hr_content(collection, query, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })
    return chunks

def build_grounded_prompt(query, chunks):
    context = "\n\n".join([f"- {c['text']} (Source: {c['metadata']['source']})" for c in chunks])
    prompt = f"""
You are an HR Policy Assistant. Answer the following employee query ONLY using the provided policy context. 
If the context does not contain the answer, say "The policy does not specify this."

Employee Query: {query}

Policy Context:
{context}

Answer:
"""
    return prompt

def generate_answer(query, chunks):
    prompt = build_grounded_prompt(query, chunks)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def answer_with_rag(collection, query, top_k=3):
    chunks = retrieve_hr_content(collection, query, top_k)
    print("\nRetrieved Chunks:")
    for c in chunks:
        print(f"- {c['text']} (Category: {c['metadata']['category']}, Distance: {c['distance']:.4f})")
    answer = generate_answer(query, chunks)
    print("\nFinal Answer:")
    print(answer)

def generate_answer_without_retrieval(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)
    return response.text

# Step 3 — Test Queries
if __name__ == "__main__":
    collection = setup_vector_database()
    index_hr_documents(collection)

    queries = [
        "How many days of annual leave am I entitled to per year?",
        "Do I need manager approval before working from home?",
        "When is the appraisal cycle conducted and how is the increment decided?"
    ]

    for q in queries:
        print("\n==============================")
        print(f"Query: {q}")
        answer_with_rag(collection, q)

    # Step 4 — Side-by-Side Comparison
    test_query = "How many days of annual leave am I entitled to per year?"
    print("\n==============================")
    print("Side-by-Side Comparison")
    print("Without RAG:")
    print(generate_answer_without_retrieval(test_query))
    print("\nWith RAG:")
    answer_with_rag(collection, test_query)