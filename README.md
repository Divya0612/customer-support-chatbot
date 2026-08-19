# Customer Support Chatbot

An AI-powered customer support chatbot built with Google Gemini. Uses agentic tool calling and RAG (Retrieval-Augmented Generation) to handle order queries and answer policy questions through a browser-based chat UI.

---

## Features

- Track, cancel, and check refund status on orders
- Answer policy and FAQ questions via semantic search over a knowledge base
- Escalate to a human agent when needed
- Persistent order state and conversation history across sessions

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini (`gemini-3.5-flash`) |
| Backend | FastAPI |
| Frontend | Plain HTML/CSS/JS |
| Embeddings | `gemini-embedding-001` + numpy cosine similarity |
| Persistence | JSON files (`orders.json`, `chat_history.json`) |

---



## Project Structure

```
proj1/
├── app.py                  # Core logic: chat session, tool loop, history
├── api.py                  # FastAPI server
├── tools.py                # Order tool functions
├── tool_definitions.py     # Gemini function declarations
├── rag.py                  # Embedding index + retrieval
├── persona.py              # System prompt
├── mock_data.py            # Seed order data
├── requirements.txt        # Python dependencies
├── knowledge_base/         # .txt files indexed for RAG
│   ├── company_info.txt
│   ├── faq.txt
│   ├── refund_policy.txt
│   └── shipping.txt
└── frontend/
    └── index.html          # Chat UI
```

---

## Setup

**1. Clone the repository**
```bash
git clone <repo-url>
cd proj1
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Gemini API key**
```bash
cp .env.example .env
# Edit .env and add your key
```

**5. Run the server**
```bash
uvicorn api:app --reload
```

**6. Open in browser**
```
http://localhost:8000
```

---

## Notes

- Delete `orders.json` to reset order data to the original seed state.
- Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).
