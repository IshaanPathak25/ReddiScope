# 🧠 Reddit Persona Generator

Generate detailed, structured, and visual personas of Reddit users using their public activity. This project uses Reddit's API for scraping and Cohere's LLMs to generate human-like persona descriptions — perfect for marketing research, UX personas, or social analysis.

---

## 🔍 What It Does

1. Takes a Reddit profile URL as input (e.g. `https://www.reddit.com/user/SuperbPercentage8050/`)
2. Scrapes recent posts and comments using `praw`
3. Sends this data to **Cohere’s LLM** to generate a structured user persona
4. Saves the persona in a clean `.txt` file
5. Optionally converts the persona into a polished image format (PNG)

---

## 📁 Project Structure

```graphql
reddit-persona/
├── data/                    # JSON scraped data from Reddit
├── output/                  # Generated persona .txt and .png files

├── main.py                  # Main CLI script (single-command execution)
├── reddit_scraper.py        # Reddit data scraper using PRAW
├── persona_generator.py     # Persona generator using Cohere API
├── visual_generator.py      # Converts persona .txt into styled PNG

├── .env                     # Contains API keys (excluded from version control)
├── requirements.txt         # Python dependencies
├── Arial.ttf                # Arial font file
└── README.md                # Project documentation
```


---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. Create a virtual environment (recommended but not mandatory)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_custom_agent
COHERE_API_KEY=your_cohere_api_key
```

---

## 🚀 How to Use

```bash
python main.py
```

### Example
```php
👋 Welcome to Reddit Persona Generator!
🔗 Enter Reddit profile URL: https://www.reddit.com/user/SuperbPercentage8050/
...
✅ Persona saved to: output/SuperbPercentage8050_persona.txt
✅ Visual persona saved as: output/SuperbPercentage8050_persona.png
```

---

## 🧠 Example Persona Output

```php
👋 Welcome to Reddit Persona Generator!
🔗 Enter Reddit profile URL: https://www.reddit.com/user/SuperbPercentage8050/
...
✅ Persona saved to: output/SuperbPercentage8050_persona.txt
✅ Visual persona saved as: output/SuperbPercentage8050_persona.png
```

---

## 📦 Dependencies

- **cohere** – Used to generate personas using the Cohere LLM API.
- **praw** – For scraping Reddit user data (posts and comments).
- **tqdm** – Adds progress bars while fetching data from Reddit.
- **python-dotenv** – Loads API keys and secrets from a `.env` file.
- **Pillow** – Creates clean, styled PNG visual personas from text files.

### Install via:
```bash
pip install -r requirements.txt
```

---

## 💡 Future Plans

- 🖥️ Build a GUI version (Tkinter / Streamlit / Gradio)
- 📄 Export persona as PDF
- 🌐 Deploy web version on Hugging Face Spaces

---

## 🧪 Tech Stack

- [**Reddit API (via PRAW)**](https://praw.readthedocs.io/en/stable/)  
  Used to scrape user posts and comments from Reddit in a structured format using Python Reddit API Wrapper (PRAW).

- [**Cohere LLMs**](https://cohere.com/)  
  Generates structured and insightful personas using Cohere's `command-r-plus` language model API.

- [**Pillow**](https://pillow.readthedocs.io/en/stable/)  
  Python Imaging Library (PIL fork) used to create visual representations of user personas as dynamically generated PNGs.

- [**Python 3.9+**](https://www.python.org/)  
  The core programming language used for all scraping, processing, and persona generation tasks.

---

## 📜 License
This project is licensed under the MIT License.
Feel free to fork, modify, and build upon it. Just give credit. 🙌

---

## ✨ Author
 Ishaan Pathak
 - 🔗 [GitHub](https://github.com/IshaanPathak25) | 💼 [LinkedIn](https://www.linkedin.com/in/ishaan-pathak-04484325b/)
