import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.store import Store
p=Path(__file__).resolve().parents[2]/'data'/'rag_knowledge.json'
records=json.loads(p.read_text(encoding='utf-8')); s=Store(); s.add(records); print('Ingested',len(records),'records. Total:',s.k.count())
