# 🤖 Digital Twin Voice Agent
### Your AI-powered voice doppelgänger for your portfolio

---

## What this is

A real-time voice AI agent that lives on your portfolio. Visitors click a button,
speak to it, and it responds AS YOU — with your knowledge, your projects, your personality.

**Stack:**
```
Visitor's mic → Deepgram STT → GPT-4o mini → OpenAI TTS → Visitor's speakers
                         ↑ knowledge base (you)
```

All orchestrated by **LiveKit Agents** in a sub-300ms latency pipeline.

---

## Step 0 — Project structure

```
dishant-twin/
├── agent.py           ← LiveKit voice agent (the brain)
├── api.py             ← FastAPI token server (lets frontend connect)
├── knowledge_base.py  ← Your info, projects, personality
├── requirements.txt
├── .env.example       ← Copy to .env and fill in keys
└── frontend/
    └── index.html     ← Drop this on your portfolio
```

---

## Step 1 — Get your API keys (all have free tiers)

| Service | What for | Free tier | Link |
|---------|----------|-----------|------|
| **LiveKit Cloud** | Real-time audio infrastructure | 50 GB/mo free | https://cloud.livekit.io |
| **OpenAI** | LLM (GPT-4o mini) + TTS | Pay-as-you-go, ~$0.01/min | https://platform.openai.com |
| **Deepgram** | Speech-to-text | $200 free credit | https://console.deepgram.com |
| **ElevenLabs** | Voice clone (optional) | 10k chars/mo free | https://elevenlabs.io |

---

## Step 2 — Setup

```bash
# Clone / download this folder, then:
cd dishant-twin

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
# → Open .env and fill in all your API keys
```

---

## Step 3 — Fill in YOUR knowledge base

Open `knowledge_base.py` and fill in the template with:
- Your background, education, location
- Your actual projects (name, stack, impact)
- Your work experience
- Your personality and interests

**The more specific you are, the better it sounds.**
Bad: "I work on AI projects"
Good: "I built a RAG pipeline over 50k Notion docs that reduced our support tickets by 40%"

---

## Step 4 — (Optional) Clone your actual voice with ElevenLabs

1. Go to https://elevenlabs.io → Sign up
2. Click **Voice Lab** → **Add Generative or Cloned Voice**
3. Upload 5–10 minutes of clean audio of yourself speaking (no background noise)
4. Copy the **Voice ID** it gives you
5. In `.env`, set `ELEVENLABS_VOICE_ID=your_id`
6. In `agent.py`, comment out the OpenAI TTS block and uncomment the ElevenLabs block
7. Run: `pip install "livekit-agents[elevenlabs]"`

---

## Step 5 — Run it locally

You need **two terminals**:

### Terminal 1 — Start the token server
```bash
source venv/bin/activate
uvicorn api:app --reload --port 8000
```
You'll see: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2 — Start the voice agent
```bash
source venv/bin/activate
python agent.py dev
```
You'll see: `Starting worker in dev mode...`

### Test it
Open `frontend/index.html` in your browser (use Live Server in VS Code, or just open the file).
Click **Talk to Dishant** and start speaking!

---

## Step 6 — Deploy to production

### Option A — Railway (easiest, ~$5/mo)

```bash
# Install Railway CLI
npm i -g @railway/cli
railway login

# Deploy
railway init
railway up
```

Set all your `.env` variables in the Railway dashboard.

### Option B — Deploy on a VPS (DigitalOcean, Hetzner, etc.)

```bash
# On your server:
git clone your-repo
cd dishant-twin
pip install -r requirements.txt

# Run both services (use screen or tmux)
uvicorn api:app --host 0.0.0.0 --port 8000 &
python agent.py start

# Or use systemd services for production reliability
```

### Option C — Docker

```bash
# Build and run
docker-compose up   # (Dockerfile coming — ask Claude to generate one)
```

---

## Step 7 — Embed on your portfolio

Once deployed, update `TOKEN_SERVER_URL` in `frontend/index.html`:

```javascript
const TOKEN_SERVER_URL = "https://your-deployed-api.railway.app/token";
```

Then either:
- **Hosted portfolio** (Next.js, React): Convert the HTML widget to a React component
- **Static site** (plain HTML): Paste the widget code directly into your page
- **Framer/Webflow**: Use the HTML embed block

---

## Customization ideas

| Feature | How |
|---------|-----|
| Your real voice | ElevenLabs voice clone (Step 4) |
| Smarter answers | Switch `gpt-4o-mini` → `gpt-4o` in `agent.py` |
| Log conversations | Add a database write in `agent.py`'s `on_enter` / session hooks |
| Analytics | Track session starts in `api.py` |
| Custom greeting | Change the text in `DishantTwin.on_enter()` |
| Different language | Change `language="en-US"` in Deepgram STT config |

---

## Troubleshooting

**"Token server error"** → Is `uvicorn api:app` running? Check terminal 1.

**"Agent not responding"** → Is `python agent.py dev` running? Check terminal 2.

**Mic not working** → Browser needs HTTPS for mic access in production. Use localhost for dev.

**High latency** → Switch Deepgram to `nova-2-general`, use `tts-1` not `tts-1-hd`.

**Voice sounds robotic** → Upgrade to ElevenLabs voice clone.

---

## Cost estimate

For a portfolio site (~100 conversations/month, ~3 min each):
- LiveKit: Free (under 50GB)
- Deepgram: ~$1.80 (300 min × $0.006/min)
- OpenAI GPT-4o mini: ~$0.60
- OpenAI TTS: ~$0.90
- **Total: ~$3.30/month** 🎉

---

Built with ❤️ using LiveKit Agents · Deepgram · OpenAI · FastAPI
