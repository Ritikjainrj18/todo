from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# model for database
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    complete = db.Column(db.Boolean)


# home route
@app.route('/')
def index():
    return "hello"

# create route
@app.route("/add",methods=["POST"])
def add():
    # add new item to database
    title = request.form.get("title")
    description = request.form.get("description")
    new_todo = Todo(title=title,description=description,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return "success"

# update route for changing description of task
@app.route("/updateDescription/<int:todo_id>",methods=["PUT"])
def updateDescription(todo_id):
    # query from db and update
    try:
        todo = Todo.query.filter_by(id=todo_id).first() 
        todo.description = request.form.get("description")
        todo.title= request.form.get("title")
        db.session.commit()
        return "success"
    except Exception as e:
        return e

# update route for changing status of task
@app.route("/updateStatus/<int:todo_id>",methods=["PUT"])
def updateStatus(todo_id):
    # query from db and update the status 
    todo = Todo.query.filter_by(id=todo_id).first() 
    todo.complete = not todo.complete
    db.session.commit()
    return "success"


# delete route
@app.route("/delete/<int:todo_id>",methods=["DELETE"])
def delete(todo_id):
    # query and remove
    todo = Todo.query.filter_by(id=todo_id).first() 
    db.session.delete(todo)
    db.session.commit()
    return "success"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # creating database
        app.run(debug=True)
    