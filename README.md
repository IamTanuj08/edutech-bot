# Self-Evaluating RAG Lesson Content Agent

Copy-paste project for the GenAI Engineer take-home. It uses Groq + LangGraph + ChromaDB + FastAPI + React/Vite.

## Run locally

1. Copy `.env.example` to `.env` and add `GROQ_API_KEY`.
2. Backend:

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/ingest.py
uvicorn app.main:app --reload --port 8000
```

3. Frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally http://localhost:5173.

## Docker

Copy `.env.example` to `.env`, add the Groq key, then:

```bash
docker compose up --build
```

## Demo

Enable `Demo error injection`. The first generation intentionally introduces unexplained jargon. The evaluator should reject it, save the failure to Chroma memory, and regenerate.

## Data

`data/rag_knowledge.json` contains short original/paraphrased notes with source metadata. Sources: the original RAG paper and Microsoft Azure RAG guidance.

The system uses two Chroma collections: `knowledge_base` and `agent_memory`.

## Rubric

Accuracy, Grounding, Beginner language, Jargon explanation, What RAG is, Why RAG matters, How RAG works, Example, Coherent flow, Standalone lesson. All are hard PASS/FAIL gates.
