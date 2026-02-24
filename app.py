import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import session


# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("AZURE_SQL_CONNECTIONSTRING")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set the secret key for session management
app.secret_key = os.getenv("SECRET_KEY") 
ADMIN_USER = os.getenv("ADMIN_USER") 
ADMIN_PASS = os.getenv("ADMIN_PASS")
# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    postalcode = db.Column(db.String(20), nullable=False)

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin/users')
        return "Invalid credentials", 401
    return render_template('admin_login.html')


# Create the database tables if they don't exist  
@app.route("/")
def home():
    users = User.query.all()
    return render_template("index.html", users=users)

# Route for handling the login page logic 
@app.route('/add', methods=['POST'])
def add_user():
    firstname = request.form['firstname']
    surname = request.form['surname']
    email = request.form['email']
    telephone = request.form['telephone']
    address = request.form['address']
    postalcode = request.form['postalcode']

    user = User(
        firstname=firstname,
        surname=surname,
        email=email,
        telephone=telephone,
        address=address,
        postalcode=postalcode
    )
    db.session.add(user)
    db.session.commit()
    return redirect('/')

# Route for updating a user
@app.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    user = User.query.get(id)
    user.name = request.form["name"]
    db.session.commit()
    return redirect(url_for("home"))

# Route for deleting a user
@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

# Admin logout route  
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin/login')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
