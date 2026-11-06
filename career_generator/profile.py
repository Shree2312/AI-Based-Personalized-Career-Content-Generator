# profile.py – Cleans and normalises raw form data into one profile dict

import json, os


# Load skill aliases from data/aliases.json (50+ aliases mapped to canonical names)
def load_aliases():
    path = os.path.join(os.path.dirname(__file__), "data", "aliases.json")
    with open(path, "r") as f:
        return json.load(f)


# Normalise a single skill string using aliases loaded from JSON
def normalise_skill(raw_skill):
    aliases = load_aliases()
    # Strip whitespace and convert to lowercase for uniform matching
    cleaned = raw_skill.strip().lower()
    # Return alias value if found, otherwise return the cleaned skill as-is
    return aliases.get(cleaned, cleaned)


# Parse comma-separated skills string and return a normalised list
def parse_skills(skills_raw):
    parts = skills_raw.split(",")
    # Normalise each part and drop empty strings
    return [normalise_skill(p) for p in parts if p.strip()]


# Validate the form; interests is now a list from checkboxes, career_goal is a dropdown
def validate_form(form_data):
    errors = []
    # Check every required text field is non-empty
    for field in ["name", "education", "skills", "career_goal", "role"]:
        if not form_data.get(field, "").strip():
            errors.append(f"Field '{field}' cannot be empty.")
    # Interests are checkboxes — getlist returns a Python list
    interests = form_data.getlist("interests") if hasattr(form_data, "getlist") else []
    if len(interests) == 0:
        errors.append("Please select at least 1 interest.")
    if len(interests) > 5:
        errors.append("Please select at most 5 interests.")
    if not errors:
        skills = parse_skills(form_data.get("skills", ""))
        if len(skills) == 0:
            errors.append("Please enter at least one skill.")
    return errors


# Build and return the single profile dict used by all other modules
def build_profile(form_data):
    # getlist reads all checked checkboxes with the same name
    interests = form_data.getlist("interests") if hasattr(form_data, "getlist") else []
    return {
        "name":        form_data["name"].strip(),
        "education":   form_data["education"].strip(),
        "skills":      parse_skills(form_data["skills"]),
        # interests is now a list of selected strings (not a single text value)
        "interests":   interests,
        "career_goal": form_data["career_goal"].strip(),
        "role":        form_data["role"].strip(),
    }
