import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load your API key from .env file
load_dotenv()

# Define paths
DOCS_PATH = "docs"
VECTORSTORE_PATH = "vectorstore"

def load_documents():
    """Load all markdown files from the docs folder."""
    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s)")
    return documents

def split_documents(documents):
    """Split documents into smaller chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

def create_vectorstore(chunks):
    """Convert chunks to embeddings and store in ChromaDB."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_PATH
    )
    print("Vectorstore created and saved successfully")
    return vectorstore

if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    create_vectorstore(chunks)