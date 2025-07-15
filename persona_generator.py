import json
import os
import cohere
from dotenv import load_dotenv

# Load API Key securely
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
client = cohere.Client(COHERE_API_KEY)

def format_persona_to_sections(raw_text, username):
    sections = {
        "Name": username,  # ✅ Always use Reddit username as Name
        "Bio": "",
        "Interests": "",
        "Needs": "",
        "Frustrations": "",
        "Personality Traits": "",
        "Tone of Voice": "",
        "Writing Style": "",
        "Notable Quotes": ""
    }

    current = None
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        for key in list(sections.keys())[1:]:  # Skip "Name"
            if line.lower().startswith(f"{key.lower()}:"):
                current = key
                line = line[len(key)+1:].strip()
                sections[current] += line + "\n"
                break
        else:
            if current:
                sections[current] += line + "\n"

    return sections

def generate_persona(username):
    print("🔄 Loading data...")
    with open(f"data/{username}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data["posts"]
    comments = data["comments"]

    examples = []
    for item in (posts + comments)[:15]:
        if "title" in item:
            title = item["title"]
            body = item.get("selftext", "")
            examples.append(f"Post: {title}\n{body}")
        else:
            examples.append(f"Comment: {item['body']}")

    prompt = f"""
You are an expert persona profiler. Based on the following Reddit activity, generate a complete and in-depth user persona.

The output should strictly follow these sections in this order:
- Name (Use only the Reddit username: "{username}")
- Bio (Write a 4–5 sentence biography summarizing the user's background, lifestyle, and worldview)
- Interests (List 4–6 specific, well-informed interests based on their Reddit activity)
- Needs (Summarize what this user seeks or values in life or online communities)
- Frustrations (List 2–4 clear pain points, concerns, or complaints they express or imply)
- Personality Traits (List 4–6 thoughtful descriptors or traits supported by tone or behavior)
- Tone of Voice (Describe how the user tends to express themselves)
- Writing Style (Comment on structure, clarity, use of language, memes, or citations)
- Notable Quotes (Pull out 3–5 powerful or interesting quotes from the content, each starting with '>')

Only use insights from the Reddit content provided. Be specific. Avoid generic output.

Reddit Activity:
{''.join(examples)}
""".strip()

    print("💬 Sending prompt to Cohere API...")
    try:
        response = client.generate(
            model="command-r-plus",
            prompt=prompt,
            temperature=0.6,
            max_tokens=1500
        )

        raw_output = response.generations[0].text.strip()
        if not raw_output:
            print("❌ Empty response from Cohere.")
            return

        sections = format_persona_to_sections(raw_output, username)

        formatted = "\n".join([f"{k}:\n{v.strip()}\n" for k, v in sections.items() if v.strip()])

        os.makedirs("output", exist_ok=True)
        with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"✅ Persona saved to output/{username}_persona.txt")

    except Exception as e:
        print(f"❌ Error during Cohere generation: {e}")
