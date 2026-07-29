import wikipedia

wikipedia.set_lang("en")

print("=" * 65)
print("📖 Wikipedia Search")
print("Type 'exit' to quit")
print("=" * 65)

while True:

    query = input("\n🔍 Search : ").strip()

    if query.lower() == "exit":
        print("\n👋 Goodbye!")
        break

    if not query:
        continue

    try:

        # Search Wikipedia first
        results = wikipedia.search(query)

        if not results:
            print("\n❌ No Wikipedia page found.")
            continue

        page_title = results[0]

        summary = wikipedia.summary(page_title, sentences=5)

        print("\n" + "=" * 65)
        print("📚 Wikipedia Summary")
        print("=" * 65)
        print(summary)

        page = wikipedia.page(page_title)

        print("\n" + "=" * 65)
        print("🌐 Wikipedia Page")
        print("=" * 65)
        print(page.url)

        print("\n" + "=" * 65)

    except wikipedia.exceptions.DisambiguationError as e:

        print("\n❌ Multiple pages found.")
        print("Try one of these:")

        for option in e.options[:5]:
            print("-", option)

    except wikipedia.exceptions.PageError:

        print("\n❌ No Wikipedia page found.")

    except Exception as e:

        print("\n❌ Error")
        print(e)