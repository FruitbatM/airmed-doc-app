import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
if os.path.exists("env.py"):
    import env


# create instance of flask and assign it to "app"
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# mail settings
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['MAIL_USERNAME'],
    "MAIL_PASSWORD": os.environ['MAIL_PASSWORD'],
    "MAIL_DEFAULT_SENDER": os.environ['MAIL_DEFAULT_SENDER'],
    "ADMIN_EMAIL": os.environ['ADMIN_EMAIL']
}

app.config.update(mail_settings)
mail = Mail(app)

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    """
    Renders homepage from main website link and shows the list of the
    specialities for the users to select from the dropdown list
    """
    specialities = mongo.db.specialities.find()
    return render_template("home.html", specialities=specialities)


# About page
# Show top specialities with icons
@app.route("/about")
def about():
    specialities = mongo.db.specialities.find()
    return render_template("about.html", specialities=specialities)


@app.route("/search", methods=["POST"])
def search():
    """
    Search for a doctor based on their first name, last name or speciality.
    If no results found return flash message and redirect to home page.
    """
    query = request.form.get("query")
    doctors = list(mongo.db.doctors.find({"$text": {"$search": query}}))

    if len(doctors) <= 0:
        flash(f"No Results found for {query}. Please search again.")
        return redirect(url_for("home"))
    else:
        return render_template("specialists.html", doctors=doctors)


@app.route("/appointment")
def appointment():
    """
    Appointment page where a user will have an option to submit an
    appointment request
    """
    specialities = mongo.db.specialities.find()
    return render_template("appointment.html", specialities=specialities)


@app.route("/appointment/request", methods=["GET", "POST"])
def appointment_request():
    """
    Populate properties from contact form entries and
    return results via Flask Mail to specified email
    address.
    """
    if request.method == "POST":
        appointment = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "telephone": request.form.get("telephone"),
            "date": request.form.get("date"),
            "time": request.form.get("time"),
            "speciality_name": request.form.get("speciality_name"),
            "message": request.form.get("message")
        }
        mongo.db.appointments.insert_one(appointment)

        try:
            msg = Message("AIRMED Appointment Request",
                          recipients=[mail_settings["ADMIN_EMAIL"]])
            msg.body = ('Hello, \nYour request was received.'
                        '\nWe will contact you shortly.'
                        '\nAIRMED Team')
            mail.send(msg)

            flash("Thank you. Your appointment request has been received!")
            return redirect(url_for('home'))

        except Exception as e:
            flash("Your email could not be sent. \
                 Please try again later.")
            return str(e)

    if "user" in session:
        userToTarget = mongo.db.users.find_one({"username": session["user"]})
        user_email = userToTarget["email"]
    else:
        user_email = ""

    return render_template("home.html", user_email=user_email)


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
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "email": request.form.get("email"),
            "telephone": request.form.get("telephone"),
            "is_admin": False,
            "gender": "",
            "age": ""
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been Successfully Registered")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("patient/register.html")


# Patient log in
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

    return render_template("patient/login.html")


# Patient Profile
@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    # grab the session username from the database
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    username = user["username"]
    first_name = user["first_name"]
    last_name = user["last_name"]
    email = user["email"]
    telephone = user["telephone"]
    profiles = mongo.db.users.find({"username": user["username"]})

    if session["user"]:
        return render_template(
            "patient/profile.html", username=username, first_name=first_name,
            last_name=last_name, email=email, telephone=telephone,
            profiles=profiles)

    return redirect(url_for("login"))


# Post profile data to MongoDB
# Link MongoDB gender data to form dropdown
@app.route("/update/profile/<username>", methods=["GET", "POST"])
def update_profile(username):
    """
    Function allows a registered user to edit and update their
    profile details
    """
    user = mongo.db.users
    gender = mongo.db.gender.find()
    if request.method == "POST":
        user.update(
            {"username": session["user"]},
            {"$set":
                {
                    "gender": request.form.get("gender"),
                    "age": request.form.get("age"),
                    "email": request.form.get("email"),
                    "telephone": request.form.get("telephone")
                }}
        )
        flash("Your profile was successfully updated")
        return redirect(url_for("profile", username=session["user"]))

    user = mongo.db.users.find_one({"username": session["user"]})
    username = user["username"]
    email = user["email"]
    telephone = user["telephone"]
    age = user["age"]
    gender = mongo.db.gender.find().sort("gender", 1)

    return render_template(
        "patient/update_profile.html", username=username, user=user,
        email=email, telephone=telephone, age=age, gender=gender)


@app.route("/delete/profile/<username>")
def delete_profile(username):
    """
    Delete a user profile from the database and logout from the session
    """
    mongo.db.users.remove(
        {"username": session["user"]})

    flash("Profile was successfully deleted")
    return redirect(
        url_for("logout", username=session["user"]))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been successfully logged out")
    session.pop("user", None) or session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/add/doctor", methods=["GET", "POST"])
def add_doctor():
    """
    Function to add a new doctor in the database
    """
    if request.method == "POST":
        doctor = {
            "title": request.form.get("title").capitalize(),
            "doctor_first_name": request.form.get(
                "doctor_first_name").capitalize(),
            "doctor_last_name": request.form.get(
                "doctor_last_name").capitalize(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "speciality_name": request.form.get("speciality_name"),
            "about": request.form.get("about"),
            "experience": request.form.get("experience"),
            "image_url": "",
            "visit_type": ""
        }
        mongo.db.doctors.insert_one(doctor)
        flash("Doctor was successfully added")
        return redirect(url_for("add_doctor"))

    specialities = mongo.db.specialities.find().sort("speciality_name", 1)
    return render_template("doctor/add_doctor.html", specialities=specialities)


@app.route("/doctor/login", methods=["GET", "POST"])
def doctor_login():
    """
    Doctor log in function which checks that user email and password
    match doctor values in the database
    """
    if request.method == "POST":
        # Check if email exists in the database
        existing_doctor = mongo.db.doctors.find_one(
            {"email": request.form.get("email")})

        if existing_doctor:
            # Ensure that hashed password matches doctor's input
            if check_password_hash(
                        existing_doctor["password"],
                        request.form.get("password")):
                session["email"] = request.form.get("email")
                flash("Welcome, dr. {}".format(
                        request.form.get("email")))
                return redirect(url_for(
                        "doctor_profile", email=session["email"]))

            else:
                # Invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("doctor_login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("doctor/doctor_login.html")


@app.route("/doctor/profile/<email>", methods=["GET"])
def doctor_profile(email):
    # grab the session user's email from the database
    doctor = mongo.db.doctors.find_one({"email": session["email"]})
    image_url = doctor["image_url"]
    doctor_first_name = doctor["doctor_first_name"]
    doctor_last_name = doctor["doctor_last_name"]
    title = doctor["title"]
    email = doctor["email"]
    phone = doctor["phone"]
    speciality_name = doctor["speciality_name"]
    experience = doctor["experience"]
    about = doctor["about"]

    if session["email"]:
        return render_template(
            "doctor/doctor_profile.html", doctor=doctor, image_url=image_url,
            doctor_first_name=doctor_first_name, title=title,
            doctor_last_name=doctor_last_name, email=email,
            phone=phone, speciality_name=speciality_name,
            experience=experience, about=about)

    return redirect(url_for("doctor_login"))


@app.route("/update/doctor/profile/<email>", methods=["GET", "POST"])
def update_doctor_profile(email):
    """
    Function allows a registered doctor to update some of their
    profile details
    """
    doctor = mongo.db.doctors
    if request.method == "POST":
        doctor.update(
            {"email": session["email"]},
            {"$set":
                {
                    "image_url": request.form.get("image_url"),
                    "phone": request.form.get("phone"),
                    "experience": request.form.get("experience"),
                    "about": request.form.get("about"),
                    "visit_type": request.form.get("visit_type")
                }}
        )
        flash("Your profile was successfully updated")
        return redirect(url_for("doctor_profile", email=session["email"]))

    doctor = mongo.db.doctors.find_one({"email": session["email"]})
    image_url = doctor["image_url"]
    phone = doctor["phone"]
    experience = doctor["experience"]
    visit_type = doctor["visit_type"]
    about = doctor["about"]

    return render_template(
        "doctor/update_doctor_profile.html",
        doctor=doctor, image_url=image_url,
        phone=phone, experience=experience, about=about,
        visit_type=visit_type)


@app.route("/delete/doctor/profile/<email>")
def delete_doctor_profile(email):
    """
    Delete a doctor's profile from the database and logout from the session
    """
    mongo.db.doctors.remove(
        {"email": session["email"]})

    flash("Profile was successfully deleted")
    return redirect(
        url_for("doctor_logout", email=session["email"]))


# Administrator user function
def admin():
    """
    Define admin user
    """
    return session['user'] == 'admin'


# ADMIN DASHBOARD
@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    """
    Display Admin Dashboard. This page is restricted to the admin user only.
    """
    # check that someone isn't brute-forcing the url get admin functionalities
    if admin():
        doctors = list(mongo.db.doctors.find().sort("email", 1))
        users = list(mongo.db.users.find().sort("username", 1))
    else:
        flash("You are not authorised to view this page")
        return redirect(url_for("login"))
    # return dashboard
    return render_template("dashboard.html", doctors=doctors,
                           users=users)


@app.route("/admin/search", methods=["POST"])
def admin_search():
    """
    Search for a doctor on admin dashboard based on their
    first name, last name or speciality.
    """
    query = request.form.get("query")
    doctors = list(mongo.db.doctors.find({"$text": {"$search": query}}))

    if len(doctors) <= 0:
        flash(f"No Results found for {query}. Please search again.")
        return redirect(url_for("admin_dashboard"))
    else:
        return render_template("dashboard.html", doctors=doctors)


@app.route("/admin/delete/doctor/<doctor_id>")
def admin_delete_profile(doctor_id):
    """
    Delete a doctor's profile from the database and logout from the session
    """
    if admin():
        if not is_object_id_valid(doctor_id):
            abort(404)
        mongo.db.doctors.remove({"_id": ObjectId(doctor_id)})
        flash("Doctor profile was successfully deleted")
        return redirect(url_for("admin_dashboard"))

    else:
        flash("You do not have permission to execute that operation")
        return redirect(url_for("login"))


# Code sourced from CI student project "ai-chat-annotator"
# https://github.com/NgiapPuoyKoh/ai-chat-annotator/blob/7b37842579f8d1783de8d11be544f9790b248f05/app.py
def is_object_id_valid(id_value):
    """ Validate is the id_value is a valid ObjectId
    """
    return id_value != "" and ObjectId.is_valid(id_value)


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


@app.route('/linkedin')
def linkedin():
    """
    Function to load Linkedin
    """
    return redirect("https://www.linkedin.com")


@app.route('/facebook')
def facebook():
    """
    Function to load Facebook
    """
    return redirect("https://www.facebook.com")


@app.route('/github')
def github():
    """
    Function to load Github
    """
    return redirect("https://github.com/FruitbatM")


@app.route('/instagram')
def instagram():
    """
    Function to load Instagram
    """
    return redirect("https://www.instagram.com")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
