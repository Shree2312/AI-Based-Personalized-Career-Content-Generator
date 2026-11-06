# validate_data.py – Run this script to validate all data JSON files

import json, os

BASE = os.path.dirname(__file__)

# Helper to load a JSON file by filename inside data/
def load(filename):
    with open(os.path.join(BASE, "data", filename)) as f:
        return json.load(f)

errors = []  # Collect all error messages

skills_db = load("skills.json")
careers   = load("careers.json")
interests = load("interests.json")
goals     = load("goals.json")
hr_qs     = load("hr_questions.json")
role_qs   = load("role_questions.json")
aliases   = load("aliases.json")

# Fields every skill in skills.json must have
REQUIRED_SKILL_FIELDS = [
    "why", "learning_activity", "project", "duration_days",
    "priority", "interview_question", "short_answer", "coding_question"
]

# Check 1: Every skill in skills.json has all required fields and no empty critical fields
for skill, data in skills_db.items():
    for field in REQUIRED_SKILL_FIELDS:
        if field not in data:
            errors.append(f"skills.json: '{skill}' missing field '{field}'")
        elif field in ("interview_question", "short_answer", "why") and not data[field]:
            errors.append(f"skills.json: '{skill}'.'{field}' is empty")

# Check 2: Every required skill in every role exists in skills.json
for role, data in careers.items():
    for skill in data.get("required_skills", []):
        if skill not in skills_db:
            errors.append(f"careers.json: role '{role}' skill '{skill}' not in skills.json")

# Check 3: Every interest maps to roles that exist in careers.json
all_roles = set(careers.keys())
for interest, roles in interests.items():
    for role in roles:
        if role not in all_roles:
            errors.append(f"interests.json: interest '{interest}' maps to unknown role '{role}'")

# Check 4: Every goal has both required fields and they are non-empty
for goal, data in goals.items():
    for field in ["summary_phrase", "extra_interview_question"]:
        if not data.get(field):
            errors.append(f"goals.json: goal '{goal}' missing or empty '{field}'")

# Check 5: Every HR question has both question and answer
for i, q in enumerate(hr_qs):
    if not q.get("question") or not q.get("answer"):
        errors.append(f"hr_questions.json: item {i} missing question or answer")

# Check 6: role_questions.json has questions for all roles
for role in careers.keys():
    if role not in role_qs or len(role_qs[role]) == 0:
        errors.append(f"role_questions.json: no questions for role '{role}'")
    else:
        for i, q in enumerate(role_qs[role]):
            if not q.get("question") or not q.get("answer"):
                errors.append(f"role_questions.json: '{role}' item {i} missing question or answer")

# Print final results
if errors:
    print(f"\n FOUND {len(errors)} ERROR(S):\n")
    for e in errors:
        print(" -", e)
else:
    print("\n All data valid.\n")
