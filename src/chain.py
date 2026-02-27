import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load API key from .env
load_dotenv()

# Path to your saved vectorstore
VECTORSTORE_PATH = "vectorstore"

# System prompt - strictly grounds the LLM in retrieved context only
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions strictly 
    based on the provided context. If the answer is not in the context, say 
    'I don't have enough information to answer that question.' 
    Never make up answers or use knowledge outside the provided context.
    
    Context: {context}"""),
    ("human", "{question}")
])

def format_docs(docs):
    """Convert retrieved document chunks into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def load_retriever():
    """Load ChromaDB vectorstore and return a retriever."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    return retriever

def build_chain():
    """Build and return the full RAG chain using LCEL."""
    retriever = load_retriever()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT_TEMPLATE
        | llm
        | StrOutputParser()
    )

    return chain

if __name__ == "__main__":
    chain = build_chain()
    response = chain.invoke("What is the OpenAI API?")
    print(response)