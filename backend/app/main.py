from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .store import Store
from .workflow import run
app=FastAPI(title='Self-Evaluating RAG Lesson Agent')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
store=Store()
class Req(BaseModel): topic:str='Introduction to RAG'; demo_error:bool=False
@app.get('/health')
def health(): return {'status':'ok','knowledge_documents':store.k.count(),'memory_documents':store.mem.count()}
@app.post('/api/generate')
def generate(req:Req):
    try:
        x=run(store,req.topic,req.demo_error)
        return {'run_id':x['run_id'],'status':x['status'],'attempt_number':x['attempt'],'lesson':x['lesson'],'evaluation':x['evaluation'],'rejection_log':x['rejection_log'],'memory_used':[m['content'] for m in x['memory']]}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500,str(e))
