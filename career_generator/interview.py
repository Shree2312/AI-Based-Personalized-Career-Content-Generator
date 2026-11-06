# interview.py – Builds all 6 interview sections from JSON data files

import json, os

CAREERS_FILE = os.path.join(os.path.dirname(__file__), "data", "careers.json")
SKILLS_FILE  = os.path.join(os.path.dirname(__file__), "data", "skills.json")
ROLE_Q_FILE  = os.path.join(os.path.dirname(__file__), "data", "role_questions.json")
HR_FILE      = os.path.join(os.path.dirname(__file__), "data", "hr_questions.json")
GOALS_FILE   = os.path.join(os.path.dirname(__file__), "data", "goals.json")


# Load each JSON data file into a Python dict or list
def load_careers():
    with open(CAREERS_FILE) as f: return json.load(f)

def load_skills():
    with open(SKILLS_FILE) as f: return json.load(f)

def load_role_questions():
    with open(ROLE_Q_FILE) as f: return json.load(f)

def load_hr_questions():
    with open(HR_FILE) as f: return json.load(f)

def load_goals():
    with open(GOALS_FILE) as f: return json.load(f)


# Section A: Technical questions for each missing skill (from skills.json)
def build_technical_questions(missing_skills, role):
    skills_db = load_skills()
    careers   = load_careers()
    # Legacy fallback for old roles that still have skills_meta
    meta      = careers.get(role, {}).get("skills_meta", {})
    questions = []
    for skill in missing_skills:
        info = skills_db.get(skill) or meta.get(skill, {})
        # Only add if an interview question is defined for this skill
        if info.get("interview_question"):
            questions.append({
                "skill":    skill,
                "question": info["interview_question"],
                "answer":   info.get("short_answer", "Research this topic further."),
                "type":     "Technical",
            })
    return questions


# Section B: Coding questions for missing skills where coding_question is non-empty
def build_coding_questions(missing_skills, role):
    skills_db = load_skills()
    careers   = load_careers()
    meta      = careers.get(role, {}).get("skills_meta", {})
    questions = []
    for skill in missing_skills:
        info = skills_db.get(skill) or meta.get(skill, {})
        cq   = info.get("coding_question", "")
        # Only add if the coding question field is not empty
        if cq:
            questions.append({
                "skill":    skill,
                "question": cq,
                "answer":   f"Write, test, and trace through your solution step by step.",
                "type":     "Coding",
            })
    return questions


# Section C: 5 role-based conceptual questions from role_questions.json
def build_role_questions(role):
    role_qs   = load_role_questions()
    questions = []
    for item in role_qs.get(role, []):
        questions.append({
            "skill":    role,
            "question": item["question"],
            "answer":   item["answer"],
            "type":     "Role Concept",
        })
    return questions


# Section D: One goal-based question from goals.json based on the selected career goal
def build_goal_question(career_goal):
    goals = load_goals()
    info  = goals.get(career_goal, {})
    q     = info.get("extra_interview_question", "")
    if not q:
        return []  # No question if goal not found in JSON
    return [{
        "skill":    "Career Goal",
        "question": q,
        "answer":   f"Reflect honestly on your goal to {info.get('summary_phrase', career_goal)}.",
        "type":     "Goal",
    }]


# Section E: 8 standard HR questions from hr_questions.json
def build_hr_questions():
    hr_list = load_hr_questions()
    return [{"skill": "HR", "question": q["question"], "answer": q["answer"], "type": "HR"} for q in hr_list]


# Section F: Revision questions for skills the student already has (matched skills)
def build_revision_questions(matched_skills, role):
    skills_db = load_skills()
    careers   = load_careers()
    meta      = careers.get(role, {}).get("skills_meta", {})
    questions = []
    for skill in matched_skills:
        info = skills_db.get(skill) or meta.get(skill, {})
        if info.get("interview_question"):
            questions.append({
                "skill":    skill,
                "question": info["interview_question"],
                "answer":   info.get("short_answer", "Review this skill further."),
                "type":     "Revision",
            })
    return questions


# Combine all 6 sections in the correct order
def build_all_questions(missing_skills, role, matched_skills=None, career_goal=""):
    if matched_skills is None:
        matched_skills = []
    return (
        build_technical_questions(missing_skills, role) +
        build_coding_questions(missing_skills, role) +
        build_role_questions(role) +
        build_goal_question(career_goal) +
        build_hr_questions() +
        build_revision_questions(matched_skills, role)
    )
