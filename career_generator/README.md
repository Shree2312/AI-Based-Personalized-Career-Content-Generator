# AI-Based Personalized Career Content Generator

> Rule-based Flask web app — no LLM, no internet calls, no magic.

---

## What It Does

Takes a student's name, education, skills, interests, and career goal, then generates:
- A personalised skill gap report with match % and readiness score
- Priority-sorted learning recommendations with duration
- A 4-week roadmap
- Role suggestions based on selected interests
- 6-section interview prep (Technical, Coding, Role Concept, Goal, HR, Revision)
- A professional summary in 3 variations

---

## 14 Target Roles

| Existing | New (added in v2) |
|---|---|
| Python Developer | Frontend Developer |
| Data Analyst | Backend Developer |
| Web Developer | Full Stack Developer |
| ML Engineer | Data Scientist |
| Software Engineer | DevOps Engineer |
| Java Developer | Cybersecurity Analyst |
| | Android App Developer |
| | Database Administrator |

---

## Data Files (`data/`)

| File | Purpose |
|---|---|
| `skills.json` | Single source of truth — all 60+ skills with 8 fields each |
| `careers.json` | 14 roles, each with a list of required skill names |
| `interests.json` | 20 interests, each mapped to 2–3 related roles |
| `goals.json` | 12 career goals with a summary phrase and an interview question |
| `role_questions.json` | 5 conceptual questions per role for the interview page |
| `hr_questions.json` | 8 standard HR questions with model answers |
| `aliases.json` | 50+ short aliases mapped to canonical skill names |

---

## How to Add a New Role (4 Steps)

1. **Add skills to `skills.json`** — add any new skill keys with all 8 fields:
   `why, learning_activity, project, duration_days, priority, interview_question, short_answer, coding_question`

2. **Add the role to `careers.json`** — add an entry with `required_skills` list and `skills_meta: {}`:
   ```json
   "My New Role": {
     "required_skills": ["python", "my-new-skill"],
     "skills_meta": {}
   }
   ```

3. **Add questions to `role_questions.json`** — add 5 role-concept questions:
   ```json
   "My New Role": [
     {"question": "...", "answer": "..."},
     ...
   ]
   ```

4. **Run the validator** to confirm everything is consistent:
   ```bash
   python validate_data.py
   ```
   Fix any errors, then start the app normally.

---

## How to Run

```bash
cd career_generator
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

---

## Project Structure

```
career_generator/
├── app.py              # Flask routes
├── analyzer.py         # Skill gap, readiness, recommendations, roadmap, suggest_roles
├── profile.py          # Form parsing, alias resolution, validation
├── summary.py          # 3-template professional summary generator
├── interview.py        # 6-section interview question builder
├── consistency.py      # Cross-report consistency checker
├── database.py         # SQLite report storage
├── auth.py             # Login / register / session helpers
├── validate_data.py    # Standalone data integrity checker (run in terminal)
├── data/
│   ├── skills.json
│   ├── careers.json
│   ├── interests.json
│   ├── goals.json
│   ├── role_questions.json
│   ├── hr_questions.json
│   └── aliases.json
├── templates/
│   ├── base.html
│   ├── form.html
│   ├── results.html
│   ├── interview.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   └── register.html
└── static/
    ├── style.css
    └── form.js
```

---

## Technical Notes

- **No LLM, no AI** — everything is set operations, templates, and JSON lookups.
- **No new pip libraries** — uses only Flask, Werkzeug (for password hashing), and Python stdlib.
- **Single source of truth** — all skill data lives in `skills.json`; `careers.json` stores only role names and required skill lists.
- **Skill aliases** — 50+ aliases in `aliases.json` (e.g. `py→python`, `k8s→kubernetes`, `ts→typescript`).
