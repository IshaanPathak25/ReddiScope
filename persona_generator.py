import json
import os
import cohere
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("YH88uRTPxGnFf6MiWf6rDeTIBI6B97lYMxctW1D7")
client = cohere.Client(COHERE_API_KEY)

def format_persona_to_sections(raw_text):
    # Smart parser that ensures correct mapping for all visual sections
    sections = {
        "Name": "",
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
        for key in sections.keys():
            if line.lower().startswith(f"{key.lower()}:"):
                current = key
                line = line[len(key)+1:].strip()
                sections[current] += line + "\n"
                break
        else:
            if current:
                sections[current] += line + "\n"

    # Return formatted .txt string
    return "\n".join([f"{k}:\n{v.strip()}\n" for k, v in sections.items() if v.strip()])

def generate_persona(username):
    print("🔄 Loading data...")
    with open(f"data/{username}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data["posts"]
    comments = data["comments"]

    # Build prompt
    examples = []
    for item in (posts + comments)[:15]:
        if "title" in item:
            title = item["title"]
            body = item.get("selftext", "")
            examples.append(f"Post: {title}\n{body}")
        else:
            examples.append(f"Comment: {item['body']}")

    prompt = f"""
You are a persona profiling assistant. Based on the following Reddit activity, generate a detailed user persona.

Please return the following sections exactly, in this order:
- Name
- Bio
- Interests
- Needs
- Frustrations
- Personality Traits
- Tone of Voice
- Writing Style
- Notable Quotes (use > for quotes)

Reddit Activity:
{''.join(examples)}
""".strip()

    print("💬 Sending prompt to Cohere API...")
    response = client.chat(
        model="command-r",
        message=prompt,
        temperature=0.6
    )

    raw_output = response.text.strip()
    formatted = format_persona_to_sections(raw_output)

    os.makedirs("output", exist_ok=True)
    with open(f"output/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(formatted)

    print(f"✅ Persona saved to output/{username}_persona.txt")
