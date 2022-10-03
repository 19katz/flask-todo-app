from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get the database for this app using SQLAlchemy, a Python program
# that facilitates communication between Python apps and relational
# databases
db = SQLAlchemy(app)

# Class that represents a single item on the todo list
class Todo(db.Model):
    # contains id (integer), title (string), and completion status (boolean)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Defines that when the app is routed to /add, it performs the
# following operations
@app.route("/add", methods=["POST"])
def add():
    # Get the title (the input submitted with the add button)
    # from the post request
    title = request.form.get("title")
    # Create a new todo with this title that has not yet been completed
    new_todo = Todo(title=title, complete=False)
    # Add the todo to the database for this session. The ID will be auto-generated
    db.session.add(new_todo)
    # Committing the database commits the change
    db.session.commit()
    # Redirect to the homepage
    return redirect(url_for("home"))

# When the app is called to update a certain todo, define
# its behavior
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Get the todo corresponding to the id
    todo = Todo.query.filter_by(id=todo_id).first()
    # Set the todo's complete status to its complement
    todo.complete = not todo.complete
    # Commit these changes to the database
    db.session.commit()
    # Redirect to the homepage
    return redirect(url_for("home"))

# When the app is called to delete a certain todo, define
# its behavior
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Get the todo corresponding to the id given in the request URL
    todo = Todo.query.filter_by(id=todo_id).first()
    # Delete the todo from the database
    db.session.delete(todo)
    # Commit the deletion change
    db.session.commit()
    # Redirect to the homepage
    return redirect(url_for("home"))

# Defines the homepage for the ap
@app.route("/")
def home():
    # Get all the todos. The query method queries from the database
    # all instances of the model class
    todo_list = Todo.query.all()
    # Get number of incomplete todos to be rendered on the website. 
    num_todos = Todo.query.filter_by(complete=False).count()
    # Generates the home website from the base.html template, which uses
    # a template engine that then inserts the todo list data into the
    # template.
    return render_template("base.html", todo_list=todo_list, num_todos=num_todos)

if __name__ == "__main__":
    # Creates the initial databases and tables
    db.create_all()
    # runs the app
    app.run(debug=True)