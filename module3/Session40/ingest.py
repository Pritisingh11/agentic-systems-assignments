import shutil
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "hostel_policy_docs"
EMBEDDING_MODEL = "text-embedding-3-small"

if CHROMA_DIR.exists():
    shutil.rmtree(CHROMA_DIR)
    print(f"Removed old Chroma directory: {CHROMA_DIR}")

loader = DirectoryLoader(
    str(DATA_DIR),
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
documents = loader.load()
print(f"Loaded {len(documents)} document(s) from {DATA_DIR}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=60,
    add_start_index=True,
)
chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunk(s)")

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)
vector_store.add_documents(chunks)
print(f"Persisted {len(chunks)} chunk(s) into collection '{COLLECTION_NAME}' at '{CHROMA_DIR}'")
