from memory import get_memory, save_plan, get_saved_plans, update_profile

TEMPLATES={
 'programming':['Fundamentals','Concept practice','Problem solving','Debugging','Mini project'],
 'math':['Concepts','Worked examples','Practice problems','Mixed problems','Timed test'],
 'science':['Core concepts','Formulas/definitions','Worked examples','Practice questions','Revision test'],
 'language':['Grammar','Vocabulary','Reading','Writing','Review'],
 'business':['Core concepts','Case studies','Examples','Practice questions','Revision'],
 'default':['Foundation','Core concepts','Guided practice','Independent practice','Revision/test']}

def category(s):
    s=s.lower()
    if any(x in s for x in ['python','java','coding','programming','dsa','algorithm','sql','dbms','computer']): return 'programming'
    if any(x in s for x in ['math','calculus','algebra','statistics','probability']): return 'math'
    if any(x in s for x in ['physics','chemistry','biology','science']): return 'science'
    if any(x in s for x in ['english','language','grammar','ielts']): return 'language'
    if any(x in s for x in ['finance','marketing','business','management','economics']): return 'business'
    return 'default'

def analyze_subjects(subjects:list)->dict:
    return {'subjects':[{'subject':s,'category':category(s),'phases':TEMPLATES[category(s)]} for s in subjects]}

def build_schedule(subjects:list, days:int, daily_hours:float, session_minutes:int, priority_subject:str='')->dict:
    if not subjects: return {'error':'No subjects provided'}
    days=max(1,min(int(days),120)); daily_hours=max(.5,min(float(daily_hours),16)); session_minutes=max(20,min(int(session_minutes),180))
    n=max(1,int(daily_hours*60)//session_minutes); schedule=[]
    for d in range(1,days+1):
        sessions=[]
        for slot in range(n):
            subject=priority_subject if priority_subject and slot==0 else subjects[((d-1)*n+slot)%len(subjects)]
            activity='Learn + practice' if d<=max(1,int(days*.6)) else 'Practice + revision'
            if d==days: activity='Final revision + self-test'
            sessions.append({'session':slot+1,'subject':subject,'minutes':session_minutes,'activity':activity})
        schedule.append({'day':d,'sessions':sessions})
    return {'days':days,'daily_hours':daily_hours,'session_minutes':session_minutes,'schedule':schedule}

def save_study_plan(title:str, goal:str, schedule:dict, subjects:list)->dict:
    return save_plan({'title':title,'goal':goal,'subjects':subjects,'schedule':schedule})

def get_study_history()->dict:
    m=get_memory(); return {'profile':m['profile'],'saved_plans':get_saved_plans()}

def remember_student_preference(key:str,value:str)->dict:
    allowed={'name','daily_hours','session_minutes','preferred_subject','learning_style'}
    if key not in allowed: return {'success':False,'message':'Unsupported preference'}
    return {'success':True,'profile':update_profile(key,value)}
