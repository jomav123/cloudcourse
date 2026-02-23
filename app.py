from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load .env file locally
load_dotenv()

app = Flask(__name__)

# Read connection string from environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("AZURE_SQL_CONNECTIONSTRING")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Example table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route("/")
def home():
    users = User.query.all()
    return f"Connected to Azure SQL! Users count: {len(users)}"

if __name__ == "__main__":
    app.run(debug=True)
