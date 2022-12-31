import sqlite3
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

SHEETS = [
    "SQL",
    "VSCODE",
    "GIT"
]

SQL = [ {"command": "SELECT", "description": "Retrieves data from a database table."}, {"command": "INSERT INTO", "description": "Inserts new data into a database table."}, {"command": "UPDATE", "description": "Modifies existing data in a database table."}, {"command": "DELETE FROM", "description": "Deletes data from a database table."}, {"command": "CREATE TABLE", "description": "Creates a new database table."}, {"command": "DROP TABLE", "description": "Deletes a database table."}, {"command": "ALTER TABLE", "description": "Modifies the structure of a database table."}, {"command": "SELECT DISTINCT", "description": "Retrieves unique data from a database table."}, {"command": "WHERE", "description": "Filters results based on specified conditions."}, {"command": "AND/OR", "description": "Combines multiple conditions in a WHERE clause."}, {"command": "ORDER BY", "description": "Sorts results in ascending or descending order."}, {"command": "GROUP BY", "description": "Groups results by a specified column or columns."}, {"command": "HAVING", "description": "Filters grouped results based on specified conditions."}, {"command": "JOIN", "description": "Retrieves data from multiple tables based on a common column."}, {"command": "INNER JOIN", "description": "Retrieves data from two tables where there is a match in both tables."}, {"command": "LEFT JOIN", "description": "Retrieves all data from the left table and matching data from the right table."}, {"command": "RIGHT JOIN", "description": "Retrieves all data from the right table and matching data from the left table."}, {"command": "FULL OUTER JOIN", "description": "Retrieves all data from both tables, regardless of whether there is a match in both."}, {"command": "UNION", "description": "Combines the results of two SELECT statements."}, {"command": "UNION ALL", "description": "Combines the results of two SELECT statements, including duplicate rows."}, {"command": "MIN/MAX", "description": "Returns the minimum or maximum value in a column."}, {"command": "COUNT", "description": "Counts the number of rows in a table."}, {"command": "AVG", "description": "Calculates the average value in a column."}, {"command": "SUM", "description": "Calculates the sum of values in a column."}, {"command": "TRUNCATE TABLE", "description": "Deletes all data from a table, but does not delete the table structure."}, {"command": "TRANSACTION", "description": "Controls the commit or rollback of a series of database queries."} ]

VSCODE = [ {"command": "Ctrl + Shift + P", "description": "Show Command Palette"},    {"command": "Ctrl + P", "description": "Quick Open"},    {"command": "Ctrl + Shift + N", "description": "New window/instance"},    {"command": "Ctrl + W", "description": "Close window/instance"},    {"command": "Ctrl + Shift + W", "description": "Close editor"},    {"command": "Ctrl + K, Ctrl + S", "description": "Open User Settings"},    {"command": "Ctrl + K, Ctrl + W", "description": "Open User Keybindings"},    {"command": "Ctrl + K, Ctrl + T", "description": "Open User Snippets"},    {"command": "Ctrl + K, Ctrl + C", "description": "Copy path of active file"},    {"command": "Ctrl + K, Ctrl + M", "description": "Change syntax mode"},    {"command": "Ctrl + K, Ctrl + I", "description": "Show hover"},    {"command": "Ctrl + K, Ctrl + X", "description": "Trim trailing whitespace"},    {"command": "Ctrl + K, Ctrl + Y", "description": "Reformat code"},    {"command": "Ctrl + K, Ctrl + L", "description": "Toggle word wrap"},    {"command": "Ctrl + K, Ctrl + J", "description": "Join lines"},    {"command": "Ctrl + K, Ctrl + D", "description": "Duplicate line"},    {"command": "Ctrl + K, Ctrl + Up", "description": "Move line/selection up"},    {"command": "Ctrl + K, Ctrl + Down", "description": "Move line/selection down"},    {"command": "Ctrl + K, Ctrl + F", "description": "Format document"},    {"command": "Ctrl + K, Ctrl + B", "description": "Toggle side bar"},    {"command": "Ctrl + K, Ctrl + O", "description": "Open Markdown preview"},    {"command": "Ctrl + K, Ctrl + Z", "description": "Toggle Zen mode"},    {"command": "Ctrl + K, Ctrl + Q", "description": "Close panel"},    {"command": "Ctrl + K, Ctrl + U", "description": "Toggle output panel"},    {"command": "Ctrl + K, Ctrl + G", "description": "Find in files"},]

GIT = [ {"command": "git clone", "description": "clone a repository from a remote source"}, {"command": "git add", "description": "add changes in the working directory to the staging area"}, {"command": "git commit", "description": "commit changes to the local repository"}, {"command": "git push", "description": "push commits to a remote repository"}, {"command": "git pull", "description": "fetch and merge changes from a remote repository"}, {"command": "git branch", "description": "create, list, or delete branches"}, {"command": "git checkout", "description": "switch branches or restore files"}, {"command": "git merge", "description": "merge branches together"}, {"command": "git status", "description": "view the status of the working directory and staging area"}, {"command": "git log", "description": "view commit history"}, {"command": "git diff", "description": "view changes between commits, commit and working directory, etc."}, {"command": "git stash", "description": "temporarily save changes that are not ready to be committed"}, {"command": "git reset", "description": "undo commits, move the HEAD pointer, or unstage files"}, {"command": "git rebase", "description": "apply commits from one branch onto another"}, {"command": "git tag", "description": "add tags to specific commits"}, {"command": "git fetch", "description": "download objects and refs from a remote repository"}, {"command": "git grep", "description": "search the working tree for a string or pattern"}, {"command": "git config", "description": "set configuration options for the repository or global settings"}, {"command": "git init", "description": "initialize a new repository"}, {"command": "git remote", "description": "manage connections to remote repositories"}, {"command": "git gc", "description": "clean up unnecessary files and optimize the repository"}, {"command": "git ls-files", "description": "display information about files in the index and the working tree"}, {"command": "git blame", "description": "track down when and why a line of code was changed"}, {"command": "git cherry-pick", "description": "apply the changes introduced by a commit"}, {"command": "git bisect", "description": "find the commit that introduced a bug"}, {"command": "git filter-branch", "description": "rewrite the entire commit history of a branch"} ]



# index route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", sheets=SHEETS)
    else:
        sheet = request.form.get("sheet")
        if sheet == "SQL":
            tables = SQL
        elif sheet == "VSCODE":
            tables = VSCODE
        elif sheet == "GIT":
            tables = GIT
        # sheet variable is sending selected button to new template
        return render_template("sheet.html", sheets=SHEETS, sheet=sheet, tables=tables)

