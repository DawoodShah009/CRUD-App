
from flask import Flask, redirect, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    desc = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    
db.init_app(app)
with app.app_context():
    db.create_all()



@app.route("/", methods = ['GET','POST'])
def hello_world():
    
    if request.method == "POST" and len(request.form["title"])!=0 and len(request.form["desc"])!=0 :
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)




@app.route("/delete/<int:sno>")
def delete(sno):
    row = Todo.query.filter_by(sno=sno).first()
    db.session.delete(row)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:sno>",  methods = ['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        row = Todo.query.filter_by(sno=sno).first()
        row.title = title
        row.desc = desc
        db.session.add(row)
        db.session.commit()
        return redirect('/')
    row = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', row=row)



if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    app.run(debug=True)
    
    
# python
# >>> from todo import db
# >>> db.create_all()


