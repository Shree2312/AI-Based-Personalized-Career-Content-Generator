# app.py – Flask routes only; all logic delegated to helper modules

import json, os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import profile as prof, analyzer, summary as summ, interview, consistency, database, auth

app = Flask(__name__)
# Secret key signs the session cookie – CHANGE THIS before real deployment
app.secret_key = "career_gen_secret_2024"
database.init_db()  # Create tables on startup (safe to call every time)


# Load role names from careers.json for the dropdown
def get_roles():
    path = os.path.join(os.path.dirname(__file__), "data", "careers.json")
    with open(path) as f:
        return list(json.load(f).keys())


# Load interest names from interests.json for the checkbox list
def get_interests():
    path = os.path.join(os.path.dirname(__file__), "data", "interests.json")
    with open(path) as f:
        return list(json.load(f).keys())


# Load goal names from goals.json for the dropdown
def get_goals():
    path = os.path.join(os.path.dirname(__file__), "data", "goals.json")
    with open(path) as f:
        return list(json.load(f).keys())


# Public home page – no login required
@app.route("/")
def index():
    return render_template("index.html")


# Register: GET shows the form; POST creates the account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")
        # Server-side validation – never rely on browser alone
        if not email or not password or not confirm:
            flash("All fields are required.", "danger")
        elif not auth.is_valid_email(email):
            flash("Please enter a valid email address (must contain '@' and '.').", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        else:
            error = auth.register_user(email, password)
            if error:
                flash(error, "danger")
            else:
                flash("Account created! Please log in.", "success")
                return redirect(url_for("login"))
    return render_template("register.html")


# Login: GET shows the form; POST verifies credentials
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = auth.check_login(email, password)
        if user:
            # Store identity in the signed session cookie
            session["user_id"] = user["id"]
            session["email"]   = user["email"]
            return redirect(url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


# Logout: wipe session and return to login
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Form: protected – generates a career report on POST
@app.route("/form", methods=["GET", "POST"])
def form():
    redir = auth.login_required()
    if redir: return redir
    roles     = get_roles()
    interests = get_interests()
    goals     = get_goals()
    if request.method == "GET":
        return render_template("form.html", roles=roles, interests=interests, goals=goals, errors=[])
    errors = prof.validate_form(request.form)
    if errors:
        return render_template("form.html", roles=roles, interests=interests, goals=goals, errors=errors)
    profile      = prof.build_profile(request.form)
    gap          = analyzer.compute_skill_gap(profile["skills"], profile["role"])
    readiness    = analyzer.compute_readiness(gap["pct"])
    recs         = analyzer.build_recommendations(gap["missing"], profile["role"])
    # Build roadmap from missing skills sorted by priority (same order as recs)
    roadmap      = analyzer.build_roadmap([r["skill"] for r in recs])
    summaries    = summ.generate_summaries(profile, readiness["score"])
    featured     = summ.pick_summary(summaries)
    questions    = interview.build_all_questions(
                       gap["missing"], profile["role"],
                       matched_skills=gap["matched"],
                       career_goal=profile["career_goal"]
                   )
    consist      = consistency.check_consistency(profile, gap, summaries)
    # --- New helper results ---
    best_roles   = analyzer.best_matching_roles(profile["skills"])
    learn_time   = analyzer.total_learning_time(gap["missing"], profile["role"])
    hint         = analyzer.next_level_hint(readiness["score"], len(gap["missing"]))
    suggested    = analyzer.suggest_roles(profile["interests"])
    extra_skills = analyzer.get_extra_skills(profile["skills"], profile["role"])
    report = {
        "profile":      profile,
        "gap":          gap,
        "readiness":    readiness,
        "recs":         recs,
        "roadmap":      roadmap,
        "summaries":    summaries,
        "featured":     featured,
        "questions":    questions,
        "consist":      consist,
        "best_roles":   best_roles,
        "learn_time":   learn_time,
        "hint":         hint,
        "suggested":    suggested,
        "extra_skills": extra_skills,
    }
    # Pass the logged-in user's id so the report is linked to their account
    report_id = database.save_report(
        profile["name"], profile["role"], readiness["score"], report, session["user_id"]
    )
    return redirect(url_for("results", report_id=report_id))


# Results: protected – view one saved report
@app.route("/results/<int:report_id>")
def results(report_id):
    redir = auth.login_required()
    if redir: return redir
    report = database.get_report(report_id)
    if not report: return "Report not found.", 404
    return render_template("results.html", report=report, report_id=report_id)


# Interview prep: protected – same saved report, different template
@app.route("/interview/<int:report_id>")
def interview_page(report_id):
    redir = auth.login_required()
    if redir: return redir
    report = database.get_report(report_id)
    if not report: return "Report not found.", 404
    return render_template("interview.html", report=report, report_id=report_id)


# History: protected – shows only THIS user's reports
@app.route("/history")
def history():
    redir = auth.login_required()
    if redir: return redir
    return render_template("history.html", reports=database.list_reports(session["user_id"]))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
