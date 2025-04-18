# Cancha 24 – Automated Football News Publisher

*A lightweight Python pipeline that scrapes, rewrites and publishes real‑time football news to Blogger and Twitter.*

---

## 1  Overview
Cancha 24 watches reliable **calciomercato** and club RSS feeds, enriches each article with GPT‑generated headlines and summaries, publishes the result to your Blogger blog and then tweets it — all without human intervention.

```
Latest RSS/HTML  →  Keyword filter  →  GPT‑powered rewrite  →  Blogger post  →  Tweet
```

### Highlights
- **Fully automated** end‑to‑end workflow.
- **AI transformation** for unique, SEO‑friendly copy driven by prompt templates you control.
- **Rate‑limit aware** duplicate guard and one‑tweet‑per‑post policy.
- **Shell wrapper** (`exec_cancha.sh`) for cron, systemd or CI/CD execution.

---

## 2  Repository layout
```
├── README.md              # you’re here
├── TODO.txt               # development backlog / notes
├── exec_cancha.sh         # convenience launcher (bash)
├── post_news.py           # main orchestration script (callable by the shell wrapper)
│
├── api_completion.py      # GPT‑rewrite helper
├── api_edit.py            # (experimental) inline GPT edit endpoint
├── blogger.py             # Blogger v3 API client
├── twitter_bot.py         # Tweepy client for Twitter v2
├── calciomercato.py       # scraping + keyword filter logic
├── configuration.py       # prompt templates & per‑blog settings
│
├── dependencies.txt       # pinned pip package versions
├── client_secrets.json    # OAuth 2.0 credentials for Google APIs *(never commit real keys!)*
├── feed.xml               # cached sample feed for offline testing
├── equipos.txt            # Spanish club‑name whitelist
├── jugadores.txt          # Spanish surname whitelist
└── cancha24/              # cache folder that stores published article IDs (auto‑created at runtime)
```

---

## 3  Installation

### 3.1  Prerequisites
- Python 3.8+ (tested with 3.12)
- Google Cloud project with Blogger v3 enabled
- Twitter developer account with elevated v2 access
- OpenAI API key *(or compatible endpoint)*

### 3.2  Dependencies
Install required libraries (pinned for stability):
```bash
pip install -r dependencies.txt
```
Key packages include **feedparser**, **beautifulsoup4**, **tweepy** and **openai**.

---

## 4  Configuration
1. Copy `client_secrets.json.example` → `client_secrets.json` and fill in your Google OAuth credentials.
2. Create a `.env` file (dotenv format):
   ```
   # OpenAI
   OPENAI_API_KEY=...

   # Blogger
   BLOG_ID=1234567890123456789
   GOOGLE_REFRESH_TOKEN=...

   # Twitter
   TWITTER_API_KEY=...
   TWITTER_API_SECRET=...
   TWITTER_ACCESS_TOKEN=...
   TWITTER_ACCESS_SECRET=...
   ```
3. Adjust prompt templates in `configuration.py` (Spanish by default).

---

## 5  Usage
### 5.1  Local run
```bash
bash exec_cancha.sh       # wrapper sets PYTHONPATH & launches post_news.py
```
The script processes **one** fresh article per run (see `news[:1]` slice); schedule the wrapper via **cron**, **systemd timer** or **GitHub Actions** for continuous operation.

### 5.2  Docker (optional)
A minimal Dockerfile is on the roadmap (see *TODO.txt*). Contributions welcome!

---

## 6  Extending
| Task | Where to tweak |
|------|----------------|
| Add/replace news feeds | `calciomercato.py` & `feed.xml` |
| Refine keyword whitelist | `equipos.txt`, `jugadores.txt` |
| Change HTML template | Section *organise source and image and HTML* in `post_news.py` |
| Multi‑language output | Add new prompts in `configuration.py` |

---

## 7  Security & quota
- Blogger and Twitter enforce rate limits — HTTP 429 responses are handled with exponential back‑off.
- **Never commit** `.env`, `client_secrets.json` or other credentials; use GitHub Secrets or a secret manager.

---

## 8  License
Licensed under the **GNU General Public License v3.0** – see `LICENSE`.

---

*Built with 🇦🇷 passion & Python – automate the news, focus on the game.*

