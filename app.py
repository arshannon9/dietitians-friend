# Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks

import bcrypt
import re
import secrets

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError
from tempfile import mkdtemp

from extensions import db
from forms import (
    LoginForm,
    PatientEntryForm,
    PatientInfoForm,
    RegistrationForm,
    TubeFeedForm,
    WeightForm,
)
from helpers import login_required, weight_change
from models import (
    User,
    Role,
    Patient,
    MonthlyWeights,
    WeightCheck,
    Formula,
    Category,
    Nutrients,
    Minerals,
    Fluids,
)
from csv_to_db import load_data_from_csv


# Configure application
def create_app():
    app = Flask(__name__)

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # Set the secret key in the app's configuration
    app.config["SECRET_KEY"] = secrets.token_hex(32)

    # Configure SQLAlchemy database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diet.db"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    # Initialize the session with the Flask app
    Session(app)

    return app


app = create_app()

# Load data from CSV files if not loaded into database
load_data_from_csv("data/formulas.csv", Formula, "id")
load_data_from_csv("data/categories.csv", Category, "id")
load_data_from_csv("data/nutrients.csv", Nutrients, "formula_id")
load_data_from_csv("data/minerals.csv", Minerals, "formula_id")
load_data_from_csv("data/fluids.csv", Fluids, "formula_id")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Create an instance of the LoginForm class
    form = LoginForm()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if form.validate_on_submit():
            # Ensure username was submitted
            if not form.username.data:
                flash("Must provide username")
                return render_template("login_user.html", form=form)

            # Ensure password was submitted
            elif not form.password.data:
                flash("Must provide password")
                return render_template("login_user.html", form=form)

        # Query database for username
        user = User.query.filter_by(username=form.username.data).first()

        # Ensure username exists and password is correct
        if not user or not bcrypt.checkpw(
            form.password.data.encode("utf-8"), user.hash
        ):
            flash("Invalid username and/or password")
            return render_template("login_user.html", form=form)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login_user.html", form=form)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Create an instance of RegistrationForm
    form = RegistrationForm()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if form.validate_on_submit():
            # Extract data from the form
            username = form.username.data
            password = form.password.data
            confirmation = form.confirmation.data

            # Ensure password meets requirements
            if len(password) < 8:
                flash("Password must be at least 8 characters", "error")
                return render_template("register_user.html", form=form)

            elif not any(char.isupper() for char in password):
                flash("Password must include at least 1 uppercase letter", "error")
                return render_template("register_user.html", form=form)

            elif not any(char.islower() for char in password):
                flash("Password must include at least 1 lowercase letter", "error")
                return render_template("register_user.html", form=form)

            elif not any(char.isdigit() for char in password):
                flash("Password must include at least 1 digit", "error")
                return render_template("register_user.html", form=form)

            elif not re.search("[!@#\$%\^&\*_\-+=:;\.?]", password):
                flash("Password must include at least one special symbol", "error")
                return render_template("register_user.html", form=form)

            # Check if password confirmation matches password
            elif confirmation != password:
                flash("Passwords don't match", "error")
                return render_template("register_user.html", form=form)

            # Check if username is already taken in the database
            else:
                user_exists = (
                    User.query.filter_by(username=username).first() is not None
                )

            # If username is taken, provide error message
            if user_exists:
                flash("Username already taken", "error")
                return render_template("register_user.html", form=form)
            else:
                # If not, hash password using hashing algorithm
                hashed_password = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )

                # Insert new user with hashed password into database
                new_user = User(username=username, hash=hashed_password)
                db.session.add(new_user)

                # Get the default role object
                role = Role.query.filter_by(name="user").first()

                # Create the default role if it doesn't exist
                if role is None:
                    role = Role(name="user")
                    db.session.add(role)

                # Add the default role to the user's roles
                new_user.roles.append(role)

                try:
                    db.session.commit()
                    flash("Registration successful!", "success")

                    # If successful, fetch new user from the database
                    user = User.query.filter_by(username=username).first()

                    # Login in the new user and redirect to home page
                    session["user_id"] = user.id
                    return redirect("/")

                # If insert fails, provide error message
                except IntegrityError as e:
                    db.session.rollback()
                    flash("Registration failed", "error")
                    return render_template("register_user.html", form=form)

    for field, errors in form.errors.items():
        for error in errors:
            flash(error, "error")
        return render_template("register.html", form=form)

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register_user.html", form=form)


@app.route("/")
@login_required
def index():
    """Show roster of patients"""

    form = PatientInfoForm()

    # Query database for all patients under care of the user
    patients = Patient.query.filter_by(provider_id=session["user_id"]).all()

    # Render index template, passing in the necessary data
    return render_template("index.html", patients=patients, form=form)


@app.route("/patient_entry", methods=["GET", "POST"])
@login_required
def patient_entry():
    """Input patients"""

    form = PatientEntryForm()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store patient information from form input
        if form.validate_on_submit():
            name_last = form.name_last.data
            name_first = form.name_first.data
            age = form.age.data
            bed = form.bed.data

            # Check if the patient already exists for the current user
            existing_patient = Patient.query.filter_by(
                name_last=name_last,
                name_first=name_first,
                age=age,
                bed=bed,
                provider_id=session["user_id"],
            ).first()

            if existing_patient:
                flash("Patient already exists")
                return redirect("/patient_entry")
            else:
                # If patient doesn't exist, add patient to patients table
                new_patient = Patient(
                    name_last=name_last,
                    name_first=name_first,
                    age=age,
                    bed=bed,
                    provider_id=session["user_id"],
                )
                db.session.add(new_patient)
                db.session.commit()

                flash("Patient successfully added!")
                return redirect("/")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("patient_entry.html", form=form)


@app.route("/patient_info/<int:patient_id>", methods=["GET", "POST"])
@login_required
def patient_info(patient_id):
    """Show patient information"""

    # Query patient's info from the database
    patient = Patient.query.get(patient_id)

    if patient is None:
        flash("Patient not found")

    # Query the patient's most recent weight check from the database
    weight_check_row = WeightCheck.query.filter_by(patient_id=patient_id).first()

    # Query the patient's monthly weights from the database
    monthly_weights = (
        MonthlyWeights.query.filter_by(patient_id=patient_id)
        .order_by(MonthlyWeights.weight_date.desc())
        .all()
    )

    # Grab timestamp for calculation
    timestamp = datetime.now()

    # Get the current weight and convert it to kgs for calculations
    weight_query = (
        MonthlyWeights.query.filter_by(patient_id=patient_id)
        .order_by(MonthlyWeights.weight_date.desc())
        .first()
    )

    if weight_query is not None:
        current_weight = weight_query.patient_weight
        current_weight_kg = current_weight / 2.2
    else:
        current_weight = 0.0
        current_weight_kg = 0.0

    # Calculate low and high limits for kcals
    kcals_low = "{:.1f}".format(current_weight_kg * 25)
    kcals_high = "{:.1f}".format(current_weight_kg * 30)

    # Calculate low and high limits for Protein
    protein_low = "{:.1f}".format(current_weight_kg * 1.2)
    protein_high = "{:.1f}".format(current_weight_kg * 1.5)

    # Calculate low and high limits for Fluids
    fluids_low = "{:.1f}".format(current_weight_kg * 30)
    fluids_high = "{:.1f}".format(current_weight_kg * 35)

    return render_template(
        "patient_info.html",
        patient=patient,
        monthly_weights=monthly_weights,
        weight_check_row=weight_check_row,
        timestamp=timestamp,
        current_weight=current_weight,
        kcals_low=kcals_low,
        kcals_high=kcals_high,
        protein_low=protein_low,
        protein_high=protein_high,
        fluids_low=fluids_low,
        fluids_high=fluids_high,
    )


@app.route("/weight_entry", methods=["GET", "POST"])
@login_required
def weight_entry():
    """Input patient weights"""

    # Create an instance of WeightForm
    form = WeightForm()

    patients = Patient.query.all()

    choices = [("", "Select a patient...")]

    for patient in patients:
        choice = (patient.id, patient.name_last + ", " + patient.name_first)

        choices.append(choice)

    # Populate the patient dropdown menu
    form.patient.choices = choices

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store patient id and weight from form input
        if form.validate_on_submit():
            patient = form.patient.data
            weight = form.weight.data
            weight_date = form.weight_date.data

            # Add weight in monthly_weights table
            new_weight = MonthlyWeights(
                user_id=session["user_id"],
                patient_id=patient,
                patient_weight=weight,
                weight_date=weight_date,
                timestamp=datetime.now(),
            )
            db.session.add(new_weight)

            # Commit changes to database
            db.session.commit()

            flash("Weight entry added successfully!")
            return redirect("/patient_info/" + str(patient))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error)

            # If form is not valid, render the template with the form and the flashed error messages
            return render_template("weight_entry.html", form=form)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("weight_entry.html", form=form)


@app.route("/weight_check/<int:patient_id>", methods=["GET", "POST"])
@login_required
def weight_check(patient_id):
    """Perform weight check at given intervals"""

    weight_check_row = WeightCheck.query.filter_by(patient_id=patient_id).first()

    # If a row doesn't exist yet, create a new one
    if weight_check_row is None:
        weight_check_row = WeightCheck(patient_id=patient_id)

    # Get the current weight and the weight date for the patient
    current_weight = (
        MonthlyWeights.query.filter_by(patient_id=patient_id)
        .order_by(MonthlyWeights.weight_date.desc())
        .first()
    )

    if current_weight is None:
        flash("No current weight data available")
        return redirect("/patient_info/" + str(patient_id))
    else:
        weight_date = current_weight.weight_date

        # Calculate percent weight change at 1, 3, 6, and 12 month intervals
        one_month = weight_change(patient_id, 1, current_weight, weight_date)
        three_month = weight_change(patient_id, 3, current_weight, weight_date)
        six_month = weight_change(patient_id, 6, current_weight, weight_date)
        twelve_month = weight_change(patient_id, 12, current_weight, weight_date)

        # Update weight check fields
        weight_check_row.current_weight = current_weight.patient_weight
        weight_check_row.one_month = one_month
        weight_check_row.three_month = three_month
        weight_check_row.six_month = six_month
        weight_check_row.twelve_month = twelve_month
        weight_check_row.timestamp = datetime.now()

        # Add the row to the session
        db.session.add(weight_check_row)

        # Commit changes to database
        db.session.commit()

        flash("Weight check updated successfully!")
        return redirect("/patient_info/" + str(patient_id))


@app.route("/history")
@login_required
def history():
    """Show history of patient weights input by user"""

    # When the user visits the history page...
    if request.method == "GET":
        # Retrieve all weights associated with the patient from the database
        history = MonthlyWeights.query.filter_by(user_id=session["user_id"]).all()

        # Display the history in a table
        return render_template("history.html", history=history)


@app.route("/tubefeed", methods=["GET", "POST"])
@login_required
def tubefeed():
    """Calculate tube feed nutrition provided"""

    # Create an instance of TubeFeedForm
    form = TubeFeedForm()

    # Populate the formulas dropdown menu
    form.formulas.choices = [(f.id, f.name) for f in Formula.query.all()]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store input data from form
        if form.validate_on_submit():
            formula_id = form.formulas.data
            tube_feed_rate = form.tube_feed_rate.data
            time = form.time.data

            # Retreive formula id and name
            formula = Formula.query.filter_by(id=formula_id).first()
            selected_formula = Formula.query.get(formula_id)
            formula_name = selected_formula.name

            if formula is not None:
                # Calculate kcals provided
                kcal_per_ml = formula.kcal_per_ml
                kcals_total = "{:.1f}".format(kcal_per_ml * tube_feed_rate * time)

                # Calculate protein provided in grams
                formula_nutrients = Nutrients.query.filter_by(
                    formula_id=formula_id
                ).first()

                protein = formula_nutrients.protein_g

                protein_per_mL = protein / 1000

                protein_total = "{:.1f}".format(protein_per_mL * tube_feed_rate * time)

                # Calculate fluids provided in mL
                formula_fluids = Fluids.query.filter_by(formula_id=formula_id).first()

                free_water_percent = formula_fluids.free_water_percent

                free_water_per_mL = free_water_percent / 100

                free_water_total = "{:.1f}".format(
                    free_water_per_mL * tube_feed_rate * time
                )

                return render_template(
                    "tubefeed_nutrition.html",
                    formula_name=formula_name,
                    tube_feed_rate=tube_feed_rate,
                    time=time,
                    kcals_total=kcals_total,
                    protein_total=protein_total,
                    free_water_total=free_water_total,
                )
            else:
                flash("Formula data could not be retreived")
                return render_template("tubefeed.html", form=form)

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error)

    else:
        return render_template("tubefeed.html", form=form)


if __name__ == "__main__":
    app.run()
