# Submission document

## Goal
Build a self-evaluating lesson generator for a 12th-grade beginner learning Introduction to RAG.

## Architecture
React/Vite -> FastAPI -> LangGraph -> retrieval + memory + Groq generation + Groq evaluation -> retry/ship.

## Data
Curated paraphrased notes from authoritative RAG sources. Each record stores source title, URL and topic metadata.

## Evaluation
Ten binary checks. The lesson ships only if all ten pass.

## Memory
Rejected lessons produce reusable failure-pattern memories stored in a second Chroma collection. Future runs retrieve those patterns before generation.

## Safety of the loop
Maximum two retries after the initial generation, so the workflow always terminates.

## Deliberate failure
Demo mode intentionally introduces unexplained technical jargon. The evaluator catches it and requests regeneration.

## Main trade-offs
Groq is used for generation/evaluation. Local sentence-transformers handle embeddings. Chroma is used because the assessment is small and needs persistent vector search. SQLite is not required for the core demo; Chroma stores the learning memory.
