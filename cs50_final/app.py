import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from datetime import datetime

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasks.db")

"""Ensure responses aren't cached"""
@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

"""Show list of tasks user is working on"""
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        task_id = request.form.get("task_id")
        db.execute("UPDATE tasks SET state = ?, completed_at = ? WHERE id = ? AND handler_id = ?",
                   "Completed", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), task_id, session["user_id"])
        return redirect("/")
    else:
        tasks = db.execute("SELECT tasks.id, tasks.task, tasks.description, tasks.in_progress_at, users.username AS handler "
                           "FROM tasks JOIN users ON tasks.handler_id = users.id WHERE tasks.handler_id = ? AND tasks.state = ?",
                           session["user_id"], "In Progress")
        return render_template("index.html", tasks=tasks, session_username=session["username"])


"""Show list of tasks that are not yet assigned"""
@app.route("/todo", methods=["GET", "POST"])
@login_required
def toDo():
    if request.method == "POST":
        # Get the task id from the form
        task_id = request.form.get("task_id")

        # Update the task to be "In Progress" and set the handler
        db.execute("UPDATE tasks SET state = ?, handler_id = ?, in_progress_at = ? WHERE id = ?",
                   "In Progress", session["user_id"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), task_id)

        # Redirect to the todo page to allow for more task claims
        return redirect("/todo")

    else:
        # Fetch all tasks in "Created" state
        tasks = db.execute("SELECT tasks.id, tasks.task, tasks.description, tasks.created_at, users.username AS creator "
                           "FROM tasks JOIN users ON tasks.creator_id = users.id WHERE tasks.state = ?", "Created")

        return render_template("todo.html", tasks=tasks)


"""Show list of tasks that are in progress"""
@app.route("/inprogress", methods=["GET", "POST"])
@login_required
def inProgress():
    if request.method == "POST":
        # Get the task id from the form
        task_id = request.form.get("task_id")

        # Update the task to be "Completed"
        db.execute("UPDATE tasks SET state = ?, completed_at = ? WHERE id = ? AND handler_id = ?",
                   "Completed", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), task_id, session["user_id"])

        # Redirect to the inprogress page
        return redirect("/inprogress")

    else:
        # Fetch all tasks in "In Progress" state
        tasks = db.execute("SELECT tasks.id, tasks.task, tasks.description, tasks.in_progress_at, users.username AS handler "
                           "FROM tasks JOIN users ON tasks.handler_id = users.id WHERE tasks.state = ?", "In Progress")

        return render_template("inprogress.html", tasks=tasks, session_username=session["username"])


"""Show list of tasks that have been completed"""
@app.route("/completed", methods=["GET"])
@login_required
def completed():
    tasks = db.execute("SELECT tasks.task, tasks.description, users.username AS handler, tasks.completed_at "
                       "FROM tasks JOIN users ON tasks.handler_id = users.id WHERE tasks.state = ?", "Completed")
    return render_template("completed.html", tasks=tasks)


"""Allow user to create a new task"""
@app.route("/newtask", methods=["GET", "POST"])
@login_required
def newTask():
    if request.method == "POST":
        # Get form data
        task = request.form.get("task")
        description = request.form.get("description")

        # Validate form data
        if not task or not description:
            return apology("must provide task and description", 400)

        # Insert the new task into the database
        db.execute("INSERT INTO tasks (creator_id, task, description, state, created_at) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], task, description, "Created", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Redirect to the home page
        return redirect("/")

    else:
        return render_template("newtask.html")

"""Allow user to log in"""
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

"""Allow user to log out"""
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

"""Allow user to register"""
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Determine if user got to page via GET or POST
    if request.method == "POST":

        # Create variables for username, hashed password, and confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Make sure all variables have been provided by the user
        if not username or not password or not confirmation:
            return apology("MUST INPUT USERNAME, PASSWORD, AND CONFIRMATION")

        # Make sure password and confirmation match
        if password != confirmation:
            return apology("PASSWORD AND CONFIRMATION DO NOT MATCH")

        # Hash user's password
        hashed_password = generate_password_hash(password)

        # Insert user info into database if username is unique
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, hashed_password)
            return render_template("login.html")

        # Handle non-unique username
        except ValueError:
            return apology("USERNAME ALREADY IN USE")

    # Show register if user got to page via GET
    else:
        return render_template("register.html")



