from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("AZURE_SQL_CONNECTIONSTRING")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route("/")
def home():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    user = User.query.get(id)
    user.name = request.form["name"]
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
