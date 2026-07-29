from openai import OpenAI
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("❌ OPENROUTER_API_KEY not found in .env file.")
    exit()

# -----------------------------
# OpenRouter Client
# -----------------------------
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# -----------------------------
# Load Knowledge Base
# -----------------------------
try:
    with open("knowledge.txt", "r", encoding="utf-8") as file:
        knowledge = file.read()
except FileNotFoundError:
    print("❌ knowledge.txt not found.")
    exit()

# -----------------------------
# System Prompt
# -----------------------------
SYSTEM_PROMPT = f"""
You are the Official AI Assistant of Student Guidance Cell (SGC).

Use ONLY the information below to answer users.

{knowledge}

Rules:

1. Answer ONLY from the knowledge provided.
2. Never invent information.
3. If the answer is unavailable, reply exactly:
"I'm sorry, I couldn't find that information in the official SGC knowledge base."
4. Keep answers short and professional.
5. Do not answer unrelated questions.
"""

# -----------------------------
# Chatbot
# -----------------------------
print("=" * 60)
print("🎓 Student Guidance Cell AI Assistant")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    question = input("\nYou : ").strip()

    if question.lower() == "exit":
        print("\nSGC AI : Goodbye! 👋")
        break

    if question == "":
        continue

    try:

        response = client.chat.completions.create(

            model="openai/gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ],

            max_tokens=250,
            temperature=0.2
        )

        answer = response.choices[0].message.content

        print(f"\nSGC AI : {answer}")

    except Exception as e:
        print("\n❌ Error:")
        print(e)