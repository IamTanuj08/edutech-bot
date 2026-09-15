import os
from pathlib import Path
from dotenv import load_dotenv
ROOT=Path(__file__).resolve().parents[2]
load_dotenv(ROOT/'.env')
GROQ_API_KEY=os.getenv('GROQ_API_KEY','')
GROQ_MODEL=os.getenv('GROQ_MODEL','openai/gpt-oss-20b')
MAX_RETRIES=int(os.getenv('MAX_RETRIES','2'))
CHROMA_PATH=os.getenv('CHROMA_PATH',str(ROOT/'data'/'chroma'))
SQLITE_PATH=os.getenv('SQLITE_PATH',str(ROOT/'data'/'runs.db'))
HF_TOKEN=os.getenv('HF_TOKEN','')
if HF_TOKEN:
    os.environ['HF_TOKEN']=HF_TOKEN
    os.environ['HUGGING_FACE_HUB_TOKEN']=HF_TOKEN
