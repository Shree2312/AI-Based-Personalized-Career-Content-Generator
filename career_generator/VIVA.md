# VIVA.md – 29 Viva Questions & One-Line Answers

> Covers every file and major concept in the project (original 15 + 8 login questions + 6 new feature questions).

---

## Flask & Routing

**Q1. What is Flask and why did you use it?**
Flask is a lightweight Python web framework; we used it because it needs zero configuration and only one pip install.

**Q2. What does `@app.route("/form", methods=["GET","POST"])` do?**
It maps the URL `/form` to the `form()` function and allows both GET (show form) and POST (submit form) HTTP methods.

**Q3. What is `render_template` in Flask?**
It finds an HTML file in the `templates/` folder, fills in Jinja2 `{{ }}` placeholders, and returns the finished HTML to the browser.

**Q4. What is `redirect(url_for("results", report_id=id))`?**
`url_for` builds the URL string for a named route; `redirect` tells the browser to navigate to that URL.

---

## Python & Logic

**Q5. What is a Python set and how did you use it for skill gap analysis?**
A set is an unordered collection of unique items; we used `&` (intersection) for matched skills and `-` (difference) for missing skills.

**Q6. How is the readiness score calculated?**
`matched_count / required_count × 100`; e.g., 3 matched out of 8 required = 37.5%.

**Q7. How does skill alias resolution work in `profile.py`?**
A dictionary `SKILL_ALIASES` maps short forms like `"py"` to `"python"`; each skill is looked up in this dict after stripping and lowercasing.

**Q8. How are the 3 professional summary variations generated?**
Three string templates with `{name}`, `{role}` etc. placeholders are filled using `.format(**fill_dict)`; `random.choice` picks one as the featured summary.

---

## Database

**Q9. What is SQLite3 and why did you choose it?**
SQLite3 is a file-based relational database built into Python's standard library; no installation or server is needed.

**Q10. What does `json.dumps` / `json.loads` do in `database.py`?**
`json.dumps` converts the Python report dictionary to a JSON string for storage; `json.loads` converts it back to a dict when retrieved.

**Q11. What is `cursor.lastrowid`?**
After an `INSERT` statement, `lastrowid` gives the auto-generated primary key (`id`) of the newly inserted row.

---

## Templates & Frontend

**Q12. What is Jinja2 template inheritance and how does `base.html` work?**
Child templates use `{% extends "base.html" %}` and fill `{% block content %}` blocks; `base.html` holds the shared navbar and footer.

**Q13. Why did you use Bootstrap 5 from a CDN instead of installing it?**
CDN means no npm/installation; a single `<link>` tag loads the full framework so the project stays simple.

**Q14. How does the Print/PDF feature work without any library?**
`window.print()` opens the browser's native print dialog; CSS `@media print` hides the navbar and buttons so the saved PDF looks clean.

---

## Project Design

**Q15. Is this project using any AI or LLM? How does it really generate content?**
No. All output comes from rule-based logic: set operations for skill gap, string templates for summaries, and a JSON knowledge base for recommendations and interview questions. There is no AI, no LLM, and no internet needed.

---

## Login System – Email-Based (8 Questions)

**Q16. Why do we never store a plain-text password in the database?**
If the database is leaked, plain text exposes every user instantly; hashes are one-way and cannot be reversed to get the original password.

**Q17. What does `generate_password_hash("mypassword")` produce?**
A safe string like `pbkdf2:sha256:260000$salt$hash` — the algorithm, random salt, and computed hash combined; never the original text.

**Q18. What does `check_password_hash(stored_hash, plain_text)` do?**
It rehashes the submitted plain password using the same salt embedded in the stored hash, then compares — returns `True` only if they match.

**Q19. What is a Flask `session` and how is it used here?**
`session` is a dict stored in a browser cookie signed by `app.secret_key`; on login we store `user_id` and `email` in it so every request knows who the user is.

**Q20. What does `app.secret_key` do?**
Flask uses it to cryptographically sign the session cookie so the user cannot tamper with their own session data.

**Q21. How does `login_required()` work without being a decorator?**
It checks whether `"user_id"` is in the session — if not, it returns a redirect object; each protected route calls it first and returns that redirect immediately if the user is not logged in.

**Q22. How does `session.clear()` log the user out?**
It deletes all keys from the session dict so the next request has no `user_id`, and all protected routes redirect back to `/login`.

**Q23. How do you validate an email address in this project?**
The `is_valid_email()` function checks that the string contains both `"@"` and `"."` — a simple rule sufficient for a college project without needing regex or external libraries.

---

## New Features (M1-P1 Additions) – 6 Questions

**Q24. How does `best_matching_roles()` work?**
It loops over every role in `careers.json`, computes match % using the same set-intersection formula as `compute_skill_gap`, sorts by percentage descending, and returns the top 3 as a list of dicts.

**Q25. How does `total_learning_time()` calculate weeks from days?**
It sums `duration_days` for all missing skills from `skills_meta` in the JSON, then divides by 7 using integer division (`//`) to get whole weeks.

**Q26. What does the `priority` field in `careers.json` control?**
It labels each skill as High, Medium, or Low; `build_recommendations` sorts missing skills using a dict `{"High":0,"Medium":1,"Low":2}` so High-priority skills appear first in the table and roadmap.

**Q27. How does `next_level_hint()` decide what sentence to show?**
It checks the score against two thresholds: 75% = Job-Ready (you're done), 40–74% = Intermediate (need Job-Ready), below 40% = Beginner (need Intermediate); `missing_count` is inserted into the sentence.

**Q28. How does the "Fill Sample Data" button work without any library?**
The `fillSampleData()` function in `form.js` uses `document.querySelector('[name="…"]').value = "…"` to set each input, and loops over `roleSelect.options` to match and set the dropdown — pure browser JavaScript, no library.

**Q29. Why is the percentage in "Best Roles For You" guaranteed to match the main Readiness Score for the selected role?**
Both use the same set-intersection formula: `len(user_set & required) / len(required) × 100`; `best_matching_roles` calls the same `load_careers()` data source as `compute_skill_gap`, so the numbers are always identical.

---

## Data Expansion (M1-P1 v2) – 8 Questions

**Q30. What is `skills.json` and why is it the "single source of truth"?**
`skills.json` is a flat dict where every skill (key) stores why, activity, project, duration_days, priority, interview_question, short_answer, and coding_question; all Python modules read from it so updating one file updates the entire app.

**Q31. Why do `careers.json` roles now have an empty `skills_meta: {}`?**
`skills_meta` was the old per-role skill data; it is now replaced by `skills.json` so the same skill (e.g. python) has identical wording in every role — `build_recommendations` reads `skills.json` first and falls back to `skills_meta` only for backward compatibility.

**Q32. What is `interests.json` and how does `suggest_roles()` use it?**
`interests.json` maps each interest string to 2–3 related role names; `suggest_roles` counts how many selected interests "vote" for each role and returns the top 3 by vote count.

**Q33. What is `goals.json` and how does `summary.py` use it?**
`goals.json` maps each career goal to a `summary_phrase` (a nicer sentence fragment) and an `extra_interview_question`; `generate_summaries` replaces the raw goal text with the phrase, and `interview.py` adds the question to the Goal section.

**Q34. How does `validate_data.py` work and when should you run it?**
It loads all 7 JSON files, checks every skill has 8 required fields, every role skill exists in `skills.json`, every interest maps to a real role, and every question has non-empty text — run it after adding any new role or skill, then fix errors before starting the app.

**Q35. What changed in `profile.py` with the interests field?**
Interests changed from a single free-text `<input>` to a list of checkboxes; `validate_form` now calls `form_data.getlist("interests")` to read all checked values as a Python list, and `build_profile` stores that list in the profile dict.

**Q36. What are the 6 sections in the new interview prep page?**
Technical (questions for missing skills), Coding (code challenges for missing skills), Role Concept (5 broad role questions), Goal (one question from the student's career goal), HR (8 standard questions), and Revision (questions for skills the student already has).

**Q37. What does the extended `check_consistency()` now verify?**
It checks that name and role appear in every summary, matched skills are real, missing skills are genuinely absent, matched + missing = required (count integrity), every required skill exists in `skills.json`, and at least one interest was selected.

