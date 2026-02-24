import os
from flask_migrate import Migrate
from functools import wraps
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

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(120))
    telephone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    postalcode = db.Column(db.String(20))

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

# Decorator to check if the user is an admin
def admin_required(f): 
    @wraps(f) 
    def wrapper(*args, **kwargs): 
        if not session.get('admin'): 
            return redirect(url_for('admin_login')) 
        return f(*args, **kwargs) 
    return wrapper

# Decorator to protect admin routes
@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)


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

    user.firstname = request.form["firstname"]
    user.surname = request.form["surname"]
    user.email = request.form["email"]
    user.telephone = request.form["telephone"]
    user.address = request.form["address"]
    user.postalcode = request.form["postalcode"]

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
