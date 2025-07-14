import os
import subprocess
from persona_generator import generate_persona
from visual_generator import generate_visual_persona

def extract_username(url):
    return url.rstrip("/").split("/")[-1]

def main():
    print("👋 Welcome to Reddit Persona Generator!")
    reddit_url = input("🔗 Enter Reddit profile URL: ").strip()

    if not reddit_url.startswith("https://www.reddit.com/user/"):
        print("❌ Invalid Reddit profile URL format.")
        return

    username = extract_username(reddit_url)
    print(f"📥 Scraping data for: {username}...")

    result = subprocess.run([os.sys.executable, "reddit_scraper.py", reddit_url])

    if result.returncode != 0:
        print("❌ Failed to scrape Reddit data.")
        return

    print(f"🧠 Generating persona for: {username}...")
    generate_persona(username)

    print(f"✅ Persona saved to: output/{username}_persona.txt")

    # 🔁 Ask if user wants a visual persona
    choice = input("🎨 Would you like to generate a visual persona as well? (y/n): ").lower().strip()
    if choice == 'y':
        print("🖼️ Generating visual persona...")
        generate_visual_persona(username)
        print(f"✅ Visual persona saved as: output/{username}_persona.png")
    else:
        print("👋 Exiting without visual persona.")

if __name__ == "__main__":
    main()
