import os
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
database_url = os.getenv("DATABASE_URL", "sqlite:///people.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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

# Home → redirect to list
@app.route("/")
def home():
    return redirect(url_for("list_users"))

# CREATE — Add user form
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        new_person = Person(
            firstname=request.form["firstname"],
            surname=request.form["surname"],
            email=request.form["email"],
            telephone=request.form["telephone"],
            address=request.form["address"],
            postal_code=request.form["postal_code"]
        )
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for("list_users"))
    return render_template("add_user.html")

# READ — List all users
@app.route("/users")
def list_users():
    people = Person.query.all()
    return render_template("list_users.html", people=people)

# UPDATE — Edit user
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    person = Person.query.get_or_404(id)
    if request.method == "POST":
        person.firstname = request.form["firstname"]
        person.surname = request.form["surname"]
        person.email = request.form["email"]
        person.telephone = request.form["telephone"]
        person.address = request.form["address"]
        person.postal_code = request.form["postal_code"]

        db.session.commit()
        return redirect(url_for("list_users"))

    return render_template("edit_user.html", person=person)

# DELETE — Remove user
@app.route("/delete/<int:id>")
def delete_user(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()    # ...existing code...
    import os
    from sqlalchemy.exc import IntegrityError
    # ...existing code...
    
    # use DATABASE_URL if set (for Azure), fallback to sqlite for local dev
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///people.db"
    )
    # ...existing code...
    
    @app.route("/add", methods=["GET", "POST"])
    def add_user():
        if request.method == "POST":
            new_person = Person(
                firstname=request.form["firstname"],
                surname=request.form["surname"],
                email=request.form["email"],
                telephone=request.form["telephone"],
                address=request.form["address"],
                postal_code=request.form["postal_code"]
            )
            db.session.add(new_person)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return "Email already exists", 400
            return redirect(url_for("list_users"))
        return render_template("add_user.html")
    # ...existing code...
    
    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    def edit_user(id):
        person = Person.query.get_or_404(id)
        if request.method == "POST":
            person.firstname = request.form["firstname"]
            person.surname = request.form["surname"]
            person.email = request.form["email"]
            person.telephone = request.form["telephone"]
            person.address = request.form["address"]
            person.postal_code = request.form["postal_code"]
    
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return "Email already exists", 400
            return redirect(url_for("list_users"))
    
        return render_template("edit_user.html", person=person)
    # ...existing code...
    
    # Replace GET-based delete with POST to avoid unsafe deletes
    @app.route("/delete/<int:id>", methods=["POST"])
    def delete_user(id):
        person = Person.query.get_or_404(id)
        db.session.delete(person)
        db.session.commit()
        return redirect(url_for("list_users"))
    # ...existing code...
    return redirect(url_for("list_users"))

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)