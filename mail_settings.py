import os
from app import app
from flask_mail import Mail, Message

# email settings
mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USE_TLS": False,
    "DEBUG": False,
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'),
    "TESTING": True
}

app.config.update(mail_settings)
mail = Mail(app)
