import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
app.config["MAPS_API_KEY"] = os.environ.get("MAPS_API_KEY")

# mail settings
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['MAIL_USERNAME'],
    "MAIL_PASSWORD": os.environ['MAIL_PASSWORD'],
    "MAIL_DEFAULT_SENDER": os.environ['MAIL_DEFAULT_SENDER'],
    "ADMIN_EMAIL": os.environ.get['ADMIN_EMAIL']
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
    If no results found return flash messag and redirect to home page.
    """
    query = request.form.get("query")
    doctors = list(mongo.db.doctors.find({"$text": {"$search": query}}))

    if len(doctors) <= 0:
        flash(f"No Results found for {query}. Please search again.")
        return redirect(url_for("home"))
    else:
        return render_template("specialists.html", doctors=doctors)


@app.route("/specialists/<speciality_name>", methods=["GET", "POST"])
def specialists(speciality_name):
    """
    Search for the list of doctors based on their speciality available from a
    dropdown list
    """
    if request.method == "POST":
        search = request.form.get("speciality_name")

        if search is None:
            flash(f"No Results found for {search}. Please search again.")
            return redirect(url_for("home"))

        else:
            specialities = mongo.db.specialities.find_one(
                {"speciailty_name": str()})
            doctors = list(
                mongo.db.doctors.find({"doctors": speciality_name}).sort(
                            [("speciality_name", -1)]))
            print(doctors)

        return render_template(
            "specialists.html", doctors=doctors,
            specialities=specialities)


@app.route("/appointment")
def appointment():
    """
    Appointment page where a user will have an option to submit an
    appointment request
    """
    specialities = mongo.db.specialities.find()
    return render_template("appointment.html", specialities=specialities)


@app.route("/appointment_request", methods=["GET", "POST"])
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
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "telephone": request.form.get("telephone"),
            "gender": "",
            "age": ""
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been Successfully Registered")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


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

    return render_template("login.html")


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
            "profile.html", username=username, first_name=first_name,
            last_name=last_name, email=email, telephone=telephone,
            profiles=profiles)

    return redirect(url_for("login"))


# Post profile data to MongoDB
# Link MongoDB gender data to form dropdown
@app.route("/update_profile/<username>", methods=["GET", "POST"])
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
        "update_profile.html", username=username, user=user,
        email=email, telephone=telephone, age=age, gender=gender)


@app.route("/delete_profile/<username>")
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
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    """
    Function to add a new doctor in the database
    """
    if request.method == "POST":
        doctor = {
            "title": request.form.get("title").str.lower(),
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


@app.route("/doctor_login", methods=["GET", "POST"])
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
                session["user"] = request.form.get("email")
                flash("Welcome, dr. {}".format(
                        request.form.get("email")))
                return redirect(url_for(
                        "doctor_profile", email=session["user"]))

            else:
                # Invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("doctor_login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("doctor_login.html")


@app.route("/doctor_profile/<email>", methods=["GET"])
def doctor_profile(email):
    # grab the session user's email from the database
    doctor = mongo.db.doctors.find_one({"email": session["user"]})
    doctor_first_name = doctor["doctor_first_name"]
    doctor_last_name = doctor["doctor_last_name"]
    title = doctor["title"]
    email = doctor["email"]
    phone = doctor["phone"]
    speciality_name = doctor["speciality_name"]
    experience = doctor["experience"]
    visit_type = doctor["visit_type"]
    about = doctor["about"]

    if session["user"]:
        return render_template(
            "doctor_profile.html", doctor=doctor,
            doctor_first_name=doctor_first_name, title=title,
            doctor_last_name=doctor_last_name, email=email,
            phone=phone, speciality_name=speciality_name,
            experience=experience, about=about, visit_type=visit_type)

    return redirect(url_for("doctor_login"))


@app.route("/update_doctor_profile/<email>", methods=["GET", "POST"])
def update_doctor_profile(email):
    """
    Function allows a registered doctor to update some of their
    profile details
    """
    doctor = mongo.db.doctors
    if request.method == "POST":
        doctor.update(
            {"email": session["user"]},
            {"$set":
                {
                    "image_url": request.form.get("image_url"),
                    "phone": request.form.get("phone"),
                    "speciality_name": request.form.get("speciality_name"),
                    "experience": request.form.get("experience"),
                    "about": request.form.get("about")
                }}
        )
        flash("Your profile was successfully updated")
        return redirect(url_for("doctor_profile", email=session["user"]))

    doctor = mongo.db.doctors.find_one({"email": session["user"]})
    image_url = doctor["image_url"]
    phone = doctor["phone"]
    about = doctor["about"]

    return render_template(
        "update_doctor_profile.html", doctor=doctor, image_url=image_url,
        phone=phone, about=about)


@app.route("/doctor_logout")
def doctor_logout():
    # remove user from session cookies
    flash("You have been successfully logged out")
    session.pop("user")
    return redirect(url_for("doctor_login"))


@app.route("/delete_doctor_profile/<email>")
def delete_doctor_profile(email):
    """
    Delete a doctor's profile from the database and logout from the session
    """
    mongo.db.doctors.remove(
        {"email": session["user"]})

    flash("Profile was successfully deleted")
    return redirect(
        url_for("doctor_logout", email=session["user"]))


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


@app.route('/instagram')
def instagram():
    """
    Function to load Instagram
    """
    return redirect("https://www.instagram.com")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
