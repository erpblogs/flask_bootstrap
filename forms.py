from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, validators, RadioField, IntegerField, SubmitField


class ContactForm(FlaskForm):
    name = TextField("Name", [validators.Required("Please enter your name")])
    email = TextField("Email", [validators.Required("Please enter your name"),
                                validators.Email("Email invalid!!")])

    gender = RadioField('Gender', [validators.Required("Please select gender")],
                        choices=[('M', 'Male'), ('F', 'Female')])
    age = IntegerField("Age")
    password = PasswordField("Password", [validators.Required("Please enter your password")])
    send = SubmitField("Send")
