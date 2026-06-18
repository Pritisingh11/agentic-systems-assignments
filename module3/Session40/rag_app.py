from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "hostel_policy_docs"
EMBEDDING_MODEL = "text-embedding-3-small"

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2},
)

def format_docs(docs):
    formatted = []
    for doc in docs:
        source = Path(doc.metadata.get("source", "")).name
        if source:
            formatted.append(f"Source: {source}\n{doc.page_content}")
        else:
            formatted.append(doc.page_content)
    return "\n\n".join(formatted)

prompt = ChatPromptTemplate.from_template(
    """You are a college hostel policy assistant.
Use only the retrieved context to answer the user's question.
If the answer is present in the context, answer clearly.
If the answer is not present in the context, say: I don't know based on the provided documents.
Do not use outside knowledge.
Mention the source file name wherever possible.

Context:
{context}

Question:
{question}
"""
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

def main():
    queries = [
        ("Q1", "What are the quiet hours on weekdays?"),
        ("Q2", "What is the scholarship amount for hostel residents?"),
    ]
    for label, question in queries:
        answer = rag_chain.invoke(question)
        print(f"{label}: {question}")
        print(f"A: {answer}\n")


if __name__ == "__main__":
    main()
