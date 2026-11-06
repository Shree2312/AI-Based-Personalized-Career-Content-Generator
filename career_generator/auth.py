# auth.py – Email-based registration, login check, and session guard

from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for
import database


# Return True if the email string contains both "@" and "." – basic format check
def is_valid_email(email):
    return "@" in email and "." in email


# Register a new user: validate, hash password, store; return error string or None
def register_user(email, password):
    # Email must have "@" and "." to be a plausible address
    if not is_valid_email(email):
        return "Please enter a valid email address (must contain '@' and '.')."
    # Check the database for an existing account with this email
    if database.get_user(email):
        return "This email is already registered. Please log in."
    # generate_password_hash turns "mypassword" into a safe one-way hash string
    hashed = generate_password_hash(password)
    database.create_user(email, hashed)
    return None  # None means registration succeeded with no errors


# Check login: return user dict on success, None if credentials are wrong
def check_login(email, password):
    user = database.get_user(email)
    if not user:
        return None  # Email not found in database
    # check_password_hash rehashes the plain password and compares to the stored hash
    if check_password_hash(user["password_hash"], password):
        return user
    return None  # Password did not match


# Simple session guard: return a redirect to /login if not logged in, else None
def login_required():
    # Flask session stores user_id after login; absence means logged out
    if "user_id" not in session:
        return redirect(url_for("login"))
    return None  # None means user IS logged in – caller continues normally
