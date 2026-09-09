import json, os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from memory import get_memory, add_chat_message
from tools import analyze_subjects, build_schedule, save_study_plan, get_study_history, remember_student_preference

load_dotenv()
SYSTEM='''You are Study Planner Agent, an AI agent, not a simple chatbot. You create realistic study plans for ANY subject: college courses, school subjects, programming, mathematics, science, languages, certifications, competitive exams, interviews and more. Never assume only DSA or DBMS. For a new plan normally: analyze_subjects -> observe -> build_schedule -> observe -> save_study_plan -> final answer. Use get_study_history for previous plans. Use remember_student_preference for stable preferences. Use tool results to decide the next action. Mention assumptions when necessary. Include breaks, revision and practice. Do not claim a plan was saved unless the save tool succeeds.'''
DECLS=[
 {'name':'analyze_subjects','description':'Analyze any academic subjects and suggest study phases.','parameters':{'type':'OBJECT','properties':{'subjects':{'type':'ARRAY','items':{'type':'STRING'}}},'required':['subjects']}},
 {'name':'build_schedule','description':'Build a concrete multi-day schedule.','parameters':{'type':'OBJECT','properties':{'subjects':{'type':'ARRAY','items':{'type':'STRING'}},'days':{'type':'INTEGER'},'daily_hours':{'type':'NUMBER'},'session_minutes':{'type':'INTEGER'},'priority_subject':{'type':'STRING'}},'required':['subjects','days','daily_hours','session_minutes']}},
 {'name':'save_study_plan','description':'Persist a generated study plan.','parameters':{'type':'OBJECT','properties':{'title':{'type':'STRING'},'goal':{'type':'STRING'},'schedule':{'type':'OBJECT'},'subjects':{'type':'ARRAY','items':{'type':'STRING'}}},'required':['title','goal','schedule','subjects']}},
 {'name':'get_study_history','description':'Retrieve saved study plans and student preferences.','parameters':{'type':'OBJECT','properties':{}}},
 {'name':'remember_student_preference','description':'Remember a stable study preference.','parameters':{'type':'OBJECT','properties':{'key':{'type':'STRING'},'value':{'type':'STRING'}},'required':['key','value']}}
]
FUNCS={'analyze_subjects':analyze_subjects,'build_schedule':build_schedule,'save_study_plan':save_study_plan,'get_study_history':get_study_history,'remember_student_preference':remember_student_preference}

class StudyPlannerAgent:
    def __init__(self):
        key=os.getenv('GEMINI_API_KEY'); self.model=os.getenv('GEMINI_MODEL','gemini-3.1-flash-lite')
        if not key: raise RuntimeError('GEMINI_API_KEY is missing in .env')
        self.client=genai.Client(api_key=key)
        self.config=types.GenerateContentConfig(system_instruction=SYSTEM,tools=[types.Tool(function_declarations=DECLS)],temperature=.2)
    def run(self,user_text):
        memory=get_memory(); add_chat_message('user',user_text)
        prompt=f'PERSISTENT MEMORY:\n{json.dumps(memory,ensure_ascii=False)}\n\nUSER REQUEST:\n{user_text}'
        contents=[types.Content(role='user',parts=[types.Part.from_text(text=prompt)])]
        trace=[]
        for _ in range(10):
            response=self.client.models.generate_content(model=self.model,contents=contents,config=self.config)
            content=response.candidates[0].content
            calls=[p.function_call for p in content.parts if getattr(p,'function_call',None)]
            if not calls:
                answer=response.text or 'I completed the study-planning task.'; add_chat_message('assistant',answer); return {'answer':answer,'tool_trace':trace}
            contents.append(content)
            for call in calls:
                args=dict(call.args or {})
                try: result=FUNCS[call.name](**args) if call.name in FUNCS else {'error':'Unknown tool'}
                except Exception as e: result={'error':str(e)}
                trace.append({'step':len(trace)+1,'tool':call.name,'arguments':args,'result':result})
                contents.append(
    types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=call.name,
                response={"result": result}
            )
        ]
    )
)
        raise RuntimeError('Agent exceeded maximum tool-call rounds')
