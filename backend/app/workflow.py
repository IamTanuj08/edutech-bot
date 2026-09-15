import uuid
from typing import TypedDict
from langgraph.graph import StateGraph,END
from .config import MAX_RETRIES
from .agents import generate,evaluate,learn

class State(TypedDict, total=False):
    run_id:str; topic:str; context:list; memory:list; lesson:dict; evaluation:dict; rejection_log:list; attempt:int; demo:bool

def run(store,topic,demo=False):
    s={'run_id':str(uuid.uuid4()),'topic':topic,'attempt':0,'rejection_log':[],'demo':demo}
    context=store.search(topic+' what is RAG why it matters how it works examples terminology',7)
    memory=store.search('previous failures for '+topic,5,store.mem)
    s.update(context=context,memory=memory)
    while True:
        s['lesson']=generate(topic,context,memory,s.get('evaluation',{}).get('regeneration_instructions',[]),demo and s['attempt']==0)
        s['evaluation']=evaluate(s['lesson'],context)
        if s['evaluation']['passed']: s['status']='approved'; return s
        failed=[c for c in s['evaluation']['checks'] if c.get('status')!='PASS']
        s['rejection_log'].append({'attempt':s['attempt']+1,'failed_checks':[c['name'] for c in failed],'reasons':[c['reason'] for c in failed],'changes_for_retry':s['evaluation']['regeneration_instructions']})
        learn(store,topic,s['evaluation'])
        if s['attempt']>=MAX_RETRIES: s['status']='rejected_after_retries'; return s
        s['attempt']+=1
