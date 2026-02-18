from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///people.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Person {self.firstname} {self.surname}>"

@app.route("/")
def home():
    return "Database is ready!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
