import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# create instance of flask and assign it to "app"
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Home page
@app.route("/")
@app.route("/home")
def home():
    specialities = mongo.db.specialities.find()
    return render_template("home.html", specialities=specialities)


@app.route("/about")
def about():
    return render_template("about.html")


# Register function was adapted from Code Institute walkthrough project
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username with this name already exists")
            return redirect(url_for("register"))

        register = {
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower(),
            "tel": request.form.get("tel")

        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been Successfully Registered")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been successfully logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/doctor_login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        # check if email exists in the database
        existing_doctor = mongo.db.doctors.find_one(
            {"email": request.form.get("email").lower()})

        if existing_doctor:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_doctor["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("email")))
                    return redirect(url_for(
                        "doctor_profile", email=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("doctor_login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("doctor_login.html")


@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        doctor = {
            "title": request.form.get("title"),
            "doctor_first_name": request.form.get("doctor_first_name"),
            "doctor_last_name": request.form.get("doctor_last_name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "speciality_name": request.form.get("speciality_name"),
            "about": request.form.get("about"),
            "experience": request.form.get("experience")
        }
        mongo.db.doctors.insert_one(doctor)
        flash("Doctor successfully added")
        return redirect(url_for("add_doctor"))

    specialities = mongo.db.specialities.find().sort("speciality_name", 1)
    return render_template("add_doctor.html", specialities=specialities)


@app.route("/doctor_profile/<email>", methods=["GET", "POST"])
def doctor_profile(email):
    # grab the session user's email from the database
    user = mongo.db.doctors.find_one({"email": session["user"]})
    email = user["email"]
    doctors = mongo.db.doctors.find({"email": user["email"]})
    if session["user"]:
        return render_template(
            "doctor_profile.html", email=email, doctors=doctors)

    return redirect(url_for("doctor_login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
