import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from openai import OpenAI

# ====================================================
# Load Environment Variables
# ====================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# ====================================================
# OpenRouter Client
# ====================================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ====================================================
# Load Document
# ====================================================

loader = TextLoader(
    "data.txt",
    encoding="utf-8"
)

documents = loader.load()

# ====================================================
# Split into Chunks
# ====================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

print(f"\nLoaded {len(docs)} chunks.\n")

# ====================================================
# Embedding Model
# ====================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ====================================================
# Create Vector Database
# ====================================================

vector_db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# ====================================================
# Retriever
# ====================================================

retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)

print("=" * 60)
print("🧠 Spider-Man RAG Chatbot")
print("Type 'exit' to quit.")
print("=" * 60)

# ====================================================
# Chat Loop
# ====================================================

while True:

    question = input("\nYou : ").strip()

    if question.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    # Retrieve relevant chunks
    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    system_prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer is not found in the context, reply:

"I couldn't find that information in the knowledge base."

Context:

{context}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=300
        )

        answer = response.choices[0].message.content

        print("\nAI :", answer)

    except Exception as e:
        print("\nError :", e)