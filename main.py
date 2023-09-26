from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MADIFICATIONS'] = False
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todoList = TODO.query.all()
    return render_template("index.html", todoList=todoList)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    newTodo = TODO(title=title, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todoId>")
def update(todoId):
    item = TODO.query.filter_by(id=todoId).first()
    item.complete = not item.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todoId>")
def delete(todoId):
    item = TODO.query.filter_by(id=todoId).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)