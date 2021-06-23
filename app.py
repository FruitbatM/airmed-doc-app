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
# Show the list of specialities for user to select from the dropdown list
@app.route("/home")
def home():
    specialities = mongo.db.specialities.find()
    return render_template("home.html", specialities=specialities)


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Search for the list of doctors based on their speciality
# Currently not working
@app.route("/search", methods=["GET", "POST"])
def search():
    specialities = mongo.db.specialities
    doctors = mongo.db.doctors.find()

    return render_template(
            "search.html", specialities=specialities, doctors=doctors)


# Register function was adapted from Code Institute walkthrough project
# Patient registration
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
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "tel": request.form.get("tel"),
            "gender": "",
            "dob": ""
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been Successfully Registered")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# Patinet log in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"],
                    request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(
                        url_for("profile", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session username from the database
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    username = user["username"]
    first_name = user["first_name"]
    last_name = user["last_name"]
    profiles = mongo.db.users.find({"username": user["username"]})

    if session["user"]:
        return render_template(
            "profile.html", username=username, first_name=first_name,
            last_name=last_name, profiles=profiles)

    return redirect(url_for("login"))


# Post profile form data to MongoDB
# Link MongoDB gender data to form dropdown
@app.route("/update_profile/<username>", methods=["GET", "POST"])
def update_profile(username):
    if request.method == "POST":
        user = mongo.db.users
        user.update(
            {"username": session["user"]},
            {"$set":
                {
                    "email": request.form.get("email"),
                    "tel": request.form.get("tel"),
                    "dob": request.form.get("dob")
                }}
        )
        flash("Your profile was successfully updated")
        return redirect(url_for("profile", username=session["user"]))

    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]
    email = user["email"]
    tel = user["tel"]
    dob = user["dob"]
    gender = mongo.db.gender.find().sort("gender", 1)

    return render_template(
        "update_profile.html", username=username, user=user,
        email=email, tel=tel, dob=dob, gender=gender)


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
            {"username": request.form.get("username").lower()})

        if existing_doctor:
            # ensure hashed password matches user input
            if check_password_hash(
                        existing_doctor["password"],
                        request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "doctor_profile", username=session["user"]))

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
            "username": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password")),
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


# 404 error
@app.errorhandler(404)
def error_404(error):
    '''
    Handles 404 error (Page not found)
    '''
    return render_template('error/404.html', error=True,
                           title="Page not found"), 404


# 500 error
@app.errorhandler(500)
def error_500(error):
    '''
    Handles 500 error (Internal Server Error)
    '''
    return render_template('error/500.html', error=True,
                           title="Internal Server Error"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
