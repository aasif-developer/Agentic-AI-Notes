from tavily import TavilyClient
from dotenv import load_dotenv
import os

# -----------------------------------
# Load Environment Variables
# -----------------------------------
load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")

if not API_KEY:
    print("❌ TAVILY_API_KEY not found in .env")
    exit()

# -----------------------------------
# Create Tavily Client
# -----------------------------------
client = TavilyClient(api_key=API_KEY)

print("=" * 65)
print("🌍 Tavily AI Web Search")
print("Type 'exit' to quit")
print("=" * 65)

while True:

    query = input("\n🔍 Search : ").strip()

    if query.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    if query == "":
        continue

    try:

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=False,
            include_images=False
        )

        print("\n" + "=" * 65)
        print("🤖 AI Answer")
        print("=" * 65)

        answer = response.get("answer")

        if answer:
            print(answer)
        else:
            print("No concise answer available.")

        print("\n" + "=" * 65)
        print("📚 Sources")
        print("=" * 65)

        for i, result in enumerate(response["results"], start=1):

            print(f"\n{i}. {result['title']}")
            print(f"🌐 {result['url']}")

        print("\n" + "=" * 65)

    except Exception as e:

        print("\n❌ Error")
        print(e)