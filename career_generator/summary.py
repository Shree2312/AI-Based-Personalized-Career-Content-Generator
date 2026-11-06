# summary.py – Generates a personalised professional summary using rule-based templates

import random, json, os

# Three sentence templates; placeholders filled with the student's actual data
TEMPLATES = [
    (
        "{name} is a {education} student with hands-on experience in "
        "{skills_str}. Passionate about {interests}, {name} is actively "
        "pursuing a career as a {role} with the goal to {career_goal}. "
        "With a current readiness score of {score}%, {name} is on track to "
        "bridge skill gaps through structured self-learning."
    ),
    (
        "An enthusiastic {education} graduate, {name} brings practical "
        "knowledge of {skills_str} and a strong interest in {interests}. "
        "{name}'s career objective is to {career_goal} as a {role}. "
        "Currently scoring {score}% readiness, {name} follows a focused "
        "learning roadmap to reach full job readiness."
    ),
    (
        "{name} combines academic training in {education} with real-world "
        "skills including {skills_str}. Driven by a passion for {interests}, "
        "{name} aims to {career_goal} in the role of {role}. "
        "A readiness score of {score}% highlights clear milestones for "
        "continued professional development."
    ),
]


# Generate 3 summary variations by filling each template with profile data
def generate_summaries(profile, score):
    # Format the user's skills as a readable comma-separated string
    skills_str = ", ".join(profile["skills"]) if profile["skills"] else "various technologies"
    # interests is now a list of strings — join them into a readable phrase
    interests_val = profile.get("interests", [])
    if isinstance(interests_val, list):
        interests_str = ", ".join(interests_val) if interests_val else "technology"
    else:
        interests_str = interests_val  # backward compatibility if still a string
    # Load goals to get the summary phrase for the selected goal
    goals_path = os.path.join(os.path.dirname(__file__), "data", "goals.json")
    try:
        with open(goals_path) as f:
            goals_data = json.load(f)
        # Use summary_phrase if available, else use the goal text directly
        career_goal_text = goals_data.get(profile["career_goal"], {}).get(
            "summary_phrase", profile["career_goal"]
        )
    except Exception:
        career_goal_text = profile["career_goal"]
    # Build the shared fill dict once and use it for all three templates
    fill = {
        "name":        profile["name"],
        "education":   profile["education"],
        "skills_str":  skills_str,
        "interests":   interests_str,
        "role":        profile["role"],
        "career_goal": career_goal_text,
        "score":       score,
    }
    # Fill all three templates and return as a list
    return [t.format(**fill) for t in TEMPLATES]


# Pick one summary at random to use as the "featured" summary
def pick_summary(summaries):
    return random.choice(summaries)
