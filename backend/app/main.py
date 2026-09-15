import io, uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pypdf
from .store import Store
from .workflow import run
app=FastAPI(title='Self-Evaluating RAG Lesson Agent')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
store=Store()
class Req(BaseModel): topic:str='Introduction to RAG'; demo_error:bool=False
@app.get('/health')
def health(): return {'status':'ok','knowledge_documents':store.k.count(),'memory_documents':store.mem.count()}
@app.post('/api/upload')
async def upload(file: UploadFile = File(...)):
    try:
        reader = pypdf.PdfReader(io.BytesIO(await file.read()))
        text = '\n'.join(p.extract_text() or '' for p in reader.pages).strip()
        if not text: raise ValueError('No readable text found in PDF.')
        chunks = [text[i:i+500].strip() for i in range(0, len(text), 450) if text[i:i+500].strip()]
        stem = Path(file.filename or 'Document').stem.replace('_', ' ').replace('-', ' ').title()
        records = [{'id': f'pdf_{uuid.uuid4().hex[:8]}_{i}', 'content': c, 'metadata': {'title': stem, 'source': file.filename or 'upload.pdf'}} for i, c in enumerate(chunks)]
        store.add(records)
        return {'status': 'ok', 'filename': file.filename, 'topic_suggested': stem, 'chunks_ingested': len(records), 'total_knowledge_docs': store.k.count()}
    except Exception as e:
        raise HTTPException(500, str(e))
@app.post('/api/generate')
def generate(req:Req):
    try:
        x=run(store,req.topic,req.demo_error)
        return {'run_id':x['run_id'],'status':x['status'],'attempt_number':x['attempt'],'lesson':x['lesson'],'evaluation':x['evaluation'],'rejection_log':x['rejection_log'],'memory_used':[m['content'] for m in x['memory']]}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500,str(e))
