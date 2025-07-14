import os
import praw
from dotenv import load_dotenv
import json
import sys
from tqdm import tqdm

load_dotenv()

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def extract_username(profile_url: str) -> str:
    return profile_url.rstrip('/').split('/')[-1]

def scrape_user_data(profile_url: str, limit=100):
    username = extract_username(profile_url)
    redditor = reddit.redditor(username)

    print(f"Scraping Reddit user: {username}")
    data = {"username": username, "posts": [], "comments": []}

    try:
        # Submissions (posts)
        for submission in tqdm(redditor.submissions.new(limit=limit), desc="Fetching posts"):
            data["posts"].append({
                "title": submission.title,
                "selftext": submission.selftext,
                "subreddit": str(submission.subreddit),
                "url": submission.url,
                "created_utc": submission.created_utc
            })

        # Comments
        for comment in tqdm(redditor.comments.new(limit=limit), desc="Fetching comments"):
            data["comments"].append({
                "body": comment.body,
                "subreddit": str(comment.subreddit),
                "link_permalink": comment.permalink,
                "created_utc": comment.created_utc
            })

        # Save to file
        os.makedirs("data", exist_ok=True)
        with open(f"data/{username}.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Data saved to data/{username}.json")

    except Exception as e:
        print(f"❌ Error scraping {username}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reddit_scraper.py <reddit_profile_url>")
    else:
        scrape_user_data(sys.argv[1])
