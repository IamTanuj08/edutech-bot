import chromadb
from sentence_transformers import SentenceTransformer
from .config import CHROMA_PATH

class Embedder:
    def __init__(self): self.m=SentenceTransformer('all-MiniLM-L6-v2')
    def __call__(self,input): return self.m.encode(list(input),normalize_embeddings=True).tolist()
    def embed_query(self,input): return self(input)
    def embed_documents(self,input): return self(input)
    def name(self): return 'all-MiniLM-L6-v2'

class Store:
    def __init__(self):
        self.c=chromadb.PersistentClient(path=CHROMA_PATH); e=Embedder()
        self.k=self.c.get_or_create_collection('knowledge_base',embedding_function=e)
        self.mem=self.c.get_or_create_collection('agent_memory',embedding_function=e)
    def add(self,records):
        self.k.upsert(ids=[x['id'] for x in records],documents=[x['content'] for x in records],metadatas=[x['metadata'] for x in records])
    def search(self,q,k=7,col=None):
        col=col or self.k
        if col.count()==0:return []
        r=col.query(query_texts=[q],n_results=min(k,col.count()))
        return [{'id':i,'content':d,'metadata':m or {}} for i,d,m in zip(r['ids'][0],r['documents'][0],r['metadatas'][0])]
    def add_memory(self,id,content,metadata): self.mem.upsert(ids=[id],documents=[content],metadatas=[metadata])
