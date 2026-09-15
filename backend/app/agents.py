import json,uuid
from groq import Groq
from .config import GROQ_API_KEY,GROQ_MODEL

RUBRIC=['Accuracy','Grounding','Beginner language','Jargon explanation','Explains what RAG is','Explains why RAG matters','Explains how RAG works','Teaches by example','Coherent teaching flow','Standalone lesson']
GEN='''You create a standalone beginner lesson. Learner: 12th-grade graduate in India, basic English, zero AI background. Use simple English, short sentences, examples, and explain every technical term when first used. Use only the supplied context for factual claims. Never say RAG completely eliminates hallucinations. Return JSON with title and lesson containing introduction, what_is_it, why_it_matters, how_it_works (array of step/title/explanation), simple_example (problem/without_rag/with_rag), key_terms (term/meaning), summary (array), quick_check (array of question/answer).'''
EVAL='''You are a strict binary evaluator. PASS only if the criterion is clearly satisfied. No partial credit. Check factual claims against supplied context. Technical terms must be explained for a complete beginner. RAG must not be described as eliminating hallucinations. Return JSON: {"checks":[{"name":...,"status":"PASS|FAIL","reason":...,"evidence":...}],"regeneration_instructions":[]}. Use exactly these checks: '''+', '.join(RUBRIC)

def client():
    if not GROQ_API_KEY: raise RuntimeError('GROQ_API_KEY missing. Copy .env.example to .env and add your Groq key.')
    return Groq(api_key=GROQ_API_KEY)

def generate(topic,context,memory,feedback=None,demo=False):
    ctx='\n\n'.join(f"[{x['metadata'].get('title')}] {x['content']}" for x in context)
    mem='\n'.join(x['content'] for x in memory) or 'No previous memory.'
    demo_text=('For this first generation only, intentionally use one technical term such as embedding or vector database without explaining it, so the evaluator can catch the failure.' if demo else '')
    prompt=f'''TOPIC: {topic}\nREFERENCE:\n{ctx}\nMEMORY:\n{mem}\nPREVIOUS FEEDBACK:\n{json.dumps(feedback or [])}\n{demo_text}\nCreate the lesson.'''
    r=client().chat.completions.create(model=GROQ_MODEL,temperature=.2,response_format={'type':'json_object'},messages=[{'role':'system','content':GEN},{'role':'user','content':prompt}])
    return json.loads(r.choices[0].message.content)

def evaluate(lesson,context):
    ctx='\n\n'.join(f"[{x['metadata'].get('title')}] {x['content']}" for x in context)
    prompt=f'REFERENCE:\n{ctx}\n\nLESSON:\n{json.dumps(lesson,ensure_ascii=False)}\nEvaluate now.'
    r=client().chat.completions.create(model=GROQ_MODEL,temperature=0,response_format={'type':'json_object'},messages=[{'role':'system','content':EVAL},{'role':'user','content':prompt}])
    x=json.loads(r.choices[0].message.content); by={c.get('name'):c for c in x.get('checks',[])}; checks=[]
    for n in RUBRIC: checks.append(by.get(n,{'name':n,'status':'FAIL','reason':'Missing evaluator result','evidence':''}))
    failed=[c['name'] for c in checks if c.get('status')!='PASS']
    return {'passed':not failed,'checks':checks,'failed_checks':failed,'regeneration_instructions':x.get('regeneration_instructions',[]) or [c['reason'] for c in checks if c.get('status')!='PASS']}

def learn(store,topic,ev):
    if ev['passed']: return
    content='; '.join(f"{c['name']}: {c['reason']}" for c in ev['checks'] if c.get('status')!='PASS')
    store.add_memory('memory_'+uuid.uuid4().hex, f'Topic: {topic}\nRecurring failure: {content}\nFuture instruction: {"; ".join(ev["regeneration_instructions"])}', {'topic':topic,'type':'failure_pattern'})
