# 💎 Gem · AI Price Intelligence
### Streamlit app — powered by Claude AI

---

## Local setup (2 steps)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501, enter your Anthropic API key in the sidebar, and start predicting.

---

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a **GitHub repository**
2. Go to → https://share.streamlit.io → **New app**
3. Select your repo, branch `main`, file path `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxxxxxx"
   ```
5. Click **Deploy** — your app is live in ~60 seconds

---

## Get an Anthropic API key

1. Sign up at https://console.anthropic.com
2. Go to **API Keys** → **Create Key**
3. Copy the `sk-ant-…` key
4. Paste it in the sidebar (local) or Streamlit Secrets (cloud)

---

## Files

```
gem_ai_app/
├── app.py                   # Full Streamlit application
├── requirements.txt         # anthropic + streamlit only
├── .streamlit/
│   └── secrets.toml         # Optional: pre-fill API key
└── README.md
```

---

## What the app does

Select 6 jewelry attributes:
- **Category** (Ring, Necklace, Bracelet…)
- **Main Metal** (Gold, Platinum, Silver…)
- **Main Gem** (Diamond, Ruby, None…)
- **Main Color**
- **Target Gender**
- **SKU Quality** (1–5)

Claude returns:
- ✦ Optimal retail price (USD)
- ✦ Recommended price range
- ✦ Confidence score
- ✦ Market demand rating
- ✦ 3–4 price driver explanations
- ✦ Market insight note
