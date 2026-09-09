import streamlit as st
from agent import StudyPlannerAgent
from memory import initialize_memory,get_memory,get_saved_plans,clear_memory

st.set_page_config(page_title='Study Planner Agent',page_icon='📚',layout='wide')
initialize_memory()
if 'agent' not in st.session_state: st.session_state.agent=StudyPlannerAgent()
if 'messages' not in st.session_state: st.session_state.messages=[]
agent=st.session_state.agent

st.title('📚 Study Planner Agent')
st.caption('AI agent with multi-step planning, tool calling, and persistent memory for any subject.')

with st.sidebar:
    st.header('Student Settings')
    m=get_memory(); profile=m['profile']
    daily=st.number_input('Available hours/day',.5,16.0,float(profile.get('daily_hours',3)),.5)
    sessions=[30,45,60,75,90,120]; current=int(profile.get('session_minutes',60)); idx=sessions.index(current) if current in sessions else 2
    session=st.selectbox('Preferred session length',sessions,index=idx)
    profile['daily_hours']=daily; profile['session_minutes']=session
    from memory import save
    save(m)
    if st.button('🗑️ Clear Memory',use_container_width=True): clear_memory(); st.session_state.agent=StudyPlannerAgent(); st.rerun()
    st.info('Works with Python, DSA, DBMS, math, physics, English, AWS, GATE, IELTS, interviews, certifications, and any other subject.')

a,b,c=st.columns(3); a.metric('Saved Plans',len(get_saved_plans())); b.metric('Daily Time',f'{daily:g} h'); c.metric('Session',f'{session} min')
left,right=st.columns([1.2,1])
with left:
    st.subheader('💬 Planner Agent')
    for msg in st.session_state.messages:
        if msg['role'] in ('user','assistant'):
            with st.chat_message(msg['role']): st.markdown(msg['content'])
    prompt=st.chat_input('Create a 14-day plan for Python, SQL and aptitude...')
    if prompt:
        st.session_state.messages.append({'role':'user','content':prompt})
        with st.chat_message('user'): st.markdown(prompt)
        with st.chat_message('assistant'):
            try:
                with st.spinner('Agent is planning and using tools...'): result=agent.run(prompt)
                st.markdown(result['answer'])
                if result['tool_trace']:
                    with st.expander('🔎 Agent tool trace',expanded=True):
                        for x in result['tool_trace']:
                            st.write(f"**Step {x['step']} — `{x['tool']}`**")
                            st.write(f"Arguments: `{x['arguments']}`")
                            st.json(x['result'])
                st.session_state.messages.append({'role':'assistant','content':result['answer']})
            except Exception as e:
                st.error('AI request failed. Check your Gemini API key and model.')
                st.exception(e)
with right:
    st.subheader('🧠 Persistent Memory')
    p=get_memory()['profile']; st.write(f"Daily time: **{p.get('daily_hours',3)} h**"); st.write(f"Session: **{p.get('session_minutes',60)} min**")
    st.divider(); st.subheader('📋 Saved Plans')
    plans=get_saved_plans()
    if not plans: st.info('No saved plans yet.')
    for plan in plans:
        with st.expander(plan.get('title','Study Plan')):
            st.write('**Goal:**',plan.get('goal','')); st.write('**Subjects:**',', '.join(plan.get('subjects',[]))); st.caption(plan.get('created_at',''))

st.divider(); st.subheader('🎯 Demo Prompts')
q1,q2,q3=st.columns(3)
q1.code('Create a 14-day plan for Python, SQL and aptitude. I can study 3 hours a day and Python is my weakest subject.')
q2.code('Remember that I prefer 60-minute study sessions.')
q3.code('What was my last saved study plan?')
