import json
from datetime import datetime
from pathlib import Path
import streamlit as st

FILE = Path(__file__).resolve().parent / 'study_memory.json'

def default():
    return {'profile': {'name':'','daily_hours':3.0,'session_minutes':60}, 'plans': [], 'chat_history': []}

def load():
    if not FILE.exists():
        data=default(); save(data); return data
    try:
        data=json.loads(FILE.read_text(encoding='utf-8'))
    except Exception:
        data=default(); save(data)
    data.setdefault('profile', default()['profile']); data.setdefault('plans', []); data.setdefault('chat_history', [])
    return data

def save(data): FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def initialize_memory():
    data=load(); st.session_state.setdefault('study_memory', data); st.session_state.setdefault('messages', [])
    if not st.session_state.messages:
        st.session_state.messages=data.get('chat_history', [])[-20:]

def get_memory(): initialize_memory(); return st.session_state.study_memory

def add_chat_message(role, content):
    initialize_memory(); item={'role':role,'content':content,'time':datetime.now().isoformat(timespec='seconds')}
    st.session_state.messages.append(item); m=get_memory(); m['chat_history'].append(item); m['chat_history']=m['chat_history'][-100:]; save(m)

def save_plan(plan):
    m=get_memory(); plan['created_at']=datetime.now().isoformat(timespec='seconds'); m['plans'].insert(0,plan); m['plans']=m['plans'][:20]; save(m); return {'success':True,'plan':plan}

def get_saved_plans(): return get_memory().get('plans',[])

def update_profile(key,value):
    m=get_memory(); m['profile'][key]=value; save(m); return m['profile']

def clear_memory():
    data=default(); save(data); st.session_state.study_memory=data; st.session_state.messages=[]
