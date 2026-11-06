# consistency.py – Extended consistency checker across profile, gap, and data integrity

import json, os

SKILLS_FILE  = os.path.join(os.path.dirname(__file__), "data", "skills.json")
CAREERS_FILE = os.path.join(os.path.dirname(__file__), "data", "careers.json")


# Load skills.json for validation
def load_skills():
    with open(SKILLS_FILE) as f:
        return json.load(f)


# Load careers.json for validation
def load_careers():
    with open(CAREERS_FILE) as f:
        return json.load(f)


# Full consistency check across profile, gap, summaries, and data integrity
def check_consistency(profile, gap, summaries):
    issues = []

    # --- Existing checks (kept unchanged) ---
    # Check that every generated summary contains the student's exact name
    for i, summary in enumerate(summaries, start=1):
        if profile["name"] not in summary:
            issues.append(f"Summary {i} does not contain the student name '{profile['name']}'.")

    # Check that every generated summary mentions the target role
    for i, summary in enumerate(summaries, start=1):
        if profile["role"] not in summary:
            issues.append(f"Summary {i} does not mention the role '{profile['role']}'.")

    # Check matched skills are truly a subset of the user's own skills
    user_set    = set(profile["skills"])
    matched_set = set(gap["matched"])
    extra = matched_set - user_set
    if extra:
        issues.append(f"Gap report lists matched skills not in profile: {extra}")

    # Check missing skills are truly absent from the user's skill set
    missing_set  = set(gap["missing"])
    false_missing = missing_set & user_set
    if false_missing:
        issues.append(f"Gap report wrongly marks these skills as missing: {false_missing}")

    # --- New check 1: matched + missing must equal required (count integrity) ---
    required_set = set(gap["required"])
    if matched_set | missing_set != required_set:
        issues.append("matched + missing skills do not equal the full required set.")

    # --- New check 2: count-level sanity check ---
    if gap["matched_n"] + len(gap["missing"]) != gap["required_n"]:
        issues.append(
            f"Count mismatch: {gap['matched_n']} matched + {len(gap['missing'])} missing "
            f"does not equal {gap['required_n']} required."
        )

    # --- New check 3: every required skill exists in skills.json ---
    try:
        skills_db = load_skills()
        careers   = load_careers()
        # Skills can live in skills.json OR in the role's legacy skills_meta
        legacy_meta = set(careers.get(profile["role"], {}).get("skills_meta", {}).keys())
        missing_from_db = [s for s in gap["required"] if s not in skills_db and s not in legacy_meta]
        if missing_from_db:
            issues.append(f"Skills not found in skills.json: {missing_from_db}")
    except Exception:
        pass  # Don't crash the page if data files are temporarily missing

    # --- New check 4: at least one interest must be selected ---
    interests = profile.get("interests", [])
    if isinstance(interests, list) and len(interests) == 0:
        issues.append("No interests selected in profile.")

    return {"consistent": len(issues) == 0, "issues": issues}
