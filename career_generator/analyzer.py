# analyzer.py – Skill gap analysis, readiness score, recommendations, roadmap, and new helper functions

import json
import os

# Paths to data files
CAREERS_FILE  = os.path.join(os.path.dirname(__file__), "data", "careers.json")
SKILLS_FILE   = os.path.join(os.path.dirname(__file__), "data", "skills.json")


# Load and return the careers knowledge base from careers.json
def load_careers():
    with open(CAREERS_FILE, "r") as f:
        return json.load(f)


# Load and return the shared skills database from skills.json
def load_skills():
    with open(SKILLS_FILE, "r") as f:
        return json.load(f)


# Return dict with matched, missing, required skill sets and match percentage
def compute_skill_gap(user_skills, role):
    careers = load_careers()
    # Get required skills for the chosen role (default empty list if not found)
    required = set(careers.get(role, {}).get("required_skills", []))
    # Convert user skills list to a set for set operations
    user_set = set(user_skills)
    matched = user_set & required        # Set intersection: skills user HAS
    missing = required - user_set        # Set difference: skills user LACKS
    # Calculate percentage; avoid division by zero
    pct = round(len(matched) / len(required) * 100, 1) if required else 0
    return {
        "required":   sorted(required),
        "matched":    sorted(matched),
        "missing":    sorted(missing),
        "pct":        pct,
        "matched_n":  len(matched),
        "required_n": len(required),
        # Human-readable formula shown on the results page
        "formula":    f"{len(matched)} matched / {len(required)} required × 100 = {pct}",
    }


# Return readiness score with a text label based on thresholds
def compute_readiness(pct):
    score = pct
    if score >= 75:
        label = "Job Ready"
    elif score >= 50:
        label = "Intermediate"
    elif score >= 25:
        label = "Beginner"
    else:
        label = "Needs Significant Work"
    return {"score": score, "label": label}


# Priority sort order: High comes first, then Medium, then Low
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


# Build recommendations list; reads from skills.json first, falls back to careers skills_meta
def build_recommendations(missing_skills, role):
    skills_db = load_skills()
    careers   = load_careers()
    # Legacy fallback: some old roles may still have skills_meta entries
    meta = careers.get(role, {}).get("skills_meta", {})
    recs = []
    for skill in missing_skills:
        # Try skills.json first (single source of truth), then fall back
        info = skills_db.get(skill) or meta.get(skill, {})
        recs.append({
            "skill":    skill,
            "why":      info.get("why", "Important for this role."),
            "activity": info.get("learning_activity", f"Study {skill} fundamentals."),
            "project":  info.get("project", f"Build a small {skill} project."),
            "days":     info.get("duration_days", 7),
            "priority": info.get("priority", "Medium"),
            # coding_question is shown on interview page (empty string if not applicable)
            "coding_q": info.get("coding_question", ""),
        })
    # Sort so High priority skills appear first in the table and roadmap
    recs.sort(key=lambda r: PRIORITY_ORDER.get(r["priority"], 1))
    return recs


# Return top-3 roles sorted by match % for the student's skills
def best_matching_roles(student_skills):
    careers  = load_careers()
    user_set = set(student_skills)
    results  = []
    for role, data in careers.items():
        required = set(data.get("required_skills", []))
        matched  = user_set & required
        # Calculate percentage; avoid division by zero
        pct = round(len(matched) / len(required) * 100, 1) if required else 0
        results.append({"role": role, "pct": pct})
    # Sort highest percentage first, then slice top 3
    results.sort(key=lambda x: x["pct"], reverse=True)
    return results[:3]


# Add up duration_days for all missing skills; reads from skills.json
def total_learning_time(missing_skills, role):
    skills_db = load_skills()
    careers   = load_careers()
    meta      = careers.get(role, {}).get("skills_meta", {})
    total_days = 0
    for skill in missing_skills:
        info = skills_db.get(skill) or meta.get(skill, {})
        # Get duration_days from JSON, default 7 if not found
        total_days += info.get("duration_days", 7)
    # Convert days to weeks using integer division
    weeks = total_days // 7
    if weeks > 0:
        time_str = f"{total_days} days (about {weeks} weeks)"
    else:
        time_str = f"{total_days} days"
    return {"days": total_days, "text": time_str}


# Return a motivational sentence about how close the student is to the next level
def next_level_hint(score, missing_count):
    if score >= 75:
        return "You are Job-Ready! Great work — keep practising to stay sharp."
    elif score >= 40:
        # Skills needed to reach 75% (Job-Ready threshold)
        return f"Learn {missing_count} more skill(s) to reach Job-Ready level."
    else:
        # Skills needed to reach 40% (Intermediate threshold)
        return f"Learn {missing_count} more skill(s) to reach Intermediate level."


# Count how many selected interests point to each role; return top 3 role names
def suggest_roles(interests):
    interests_file = os.path.join(os.path.dirname(__file__), "data", "interests.json")
    with open(interests_file, "r") as f:
        interest_map = json.load(f)
    # Count votes: each interest adds 1 vote to its mapped roles
    vote = {}
    for interest in interests:
        for role in interest_map.get(interest, []):
            vote[role] = vote.get(role, 0) + 1
    # Sort roles by vote count descending and return top 3 names
    sorted_roles = sorted(vote, key=lambda r: vote[r], reverse=True)
    return sorted_roles[:3]


# Return skills the user has that are NOT required for the chosen role
def get_extra_skills(user_skills, role):
    careers  = load_careers()
    required = set(careers.get(role, {}).get("required_skills", []))
    # Extra = user has them but the role does not require them
    return [s for s in user_skills if s not in required]


# Build a 4-week roadmap from the missing skills list (preserves priority order from recs)
def build_roadmap(missing_skills):
    # Distribute missing skills across 4 themed weeks
    weeks = {
        "Week 1 – Fundamentals":   [],
        "Week 2 – Intermediate":   [],
        "Week 3 – Project Work":   [],
        "Week 4 – Revision & Mock":[],
    }
    week_keys = list(weeks.keys())
    for i, skill in enumerate(missing_skills):
        # Cycle through weeks using modulo so all skills are placed
        week = week_keys[i % 4]
        weeks[week].append(skill)
    # Remove weeks that ended up empty
    return {k: v for k, v in weeks.items() if v}
