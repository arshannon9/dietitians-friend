# Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks

from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    FloatField,
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
    DateField,
    validators,
)
from wtforms.validators import DataRequired, EqualTo, Length


# Form for user login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


# Form for patient input
class PatientEntryForm(FlaskForm):
    name_last = StringField("Last Name", validators=[DataRequired()])
    name_first = StringField("First Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    bed = StringField("Bed", validators=[DataRequired()])


# Form to access patient info
class PatientInfoForm(FlaskForm):
    view = SubmitField("View")


# Form for user registration
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("confirmation", message="Passwords must match"),
        ],
    )
    confirmation = PasswordField("Confirm Password", validators=[DataRequired()])


# Form for tube feed calculation input
class TubeFeedForm(FlaskForm):
    formulas = SelectField("Formula", choices=[])
    tube_feed_rate = FloatField(
        "Tube Feed Rate (mL/hr)",
        [validators.InputRequired(), validators.NumberRange(min=0)],
    )
    time = IntegerField(
        "Time (hr)", [validators.InputRequired(), validators.NumberRange(min=1)]
    )


# Form for weight input
class WeightForm(FlaskForm):
    patient = SelectField("Patient", choices=[])
    weight = FloatField(
        "Weight (lb)", [validators.InputRequired(), validators.NumberRange(min=0)]
    )
    weight_date = DateField(
        "Weight Date", [validators.InputRequired()], format="%Y-%m-%d"
    )
