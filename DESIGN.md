Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks

Overview:

    DIETITIAN'S FRIEND aids users in providing correct care for patient populations. The app serves as a tool for storing patient information and clinical data, and using this data to perform essential calculations for patient care, including tracking weights and weight change, determining nutritional needs based on a patient's weight, and calculating the nutritional output of tube feeds depoending on the formula.

User Interface:

    Layout:

        General layout:

            - A navigation bar at the top of the page with links:
                - Home (brand logo)
                - before login: Login, Register
                - after login: Patient Entry, Tube Feed Calculator, User History, Logout
            - A footer containing copyright information

        Login page:

            - Login form with inputs for username and password, 'Register' button to access Register page, and 'Login' button to submit form

        Register page:

            - Registration form with inputs for username, password, and password confirmation, and a 'Register' button ot submit form
            - Password requirements listed below form

        Patient Roster page:

            - Patient Roster table with entries for every patient registered under user's care
            - Each entry contains a Patient ID, Last Name, First Name, Age, Bed, and a 'View' button to access patient's Patient Information page

        Patient Entry page:

            - Patient Entry form with inputs for Last Name, First Name, Age, and Bed, and a 'Submit' button to submit form

        Patient Information page:

            - Header with patient name, age, and bed
            - Table containing data from patient's most recent weight check, including Timestamp, Current Weight, and weight changes at 1-month, 3-month, 6-month, and 12-month intervals, with 'Update Weight Check' button to update using most recent weight as current weight
            - Table containing data on patient's nutritional needs, includes Timestamp, Current Weight, and amount of kcals, Protein, and Fluids needed based on patient's current weight
            - Weight Log table containing data on patient weights, including a Log ID, User ID, Patient ID, Weight Date, Patient Weight, and Entry Timestamp, sorted by weight date
            - 'Input Patient Weight' button accesses Weight Entry page

        Weight Entry page:

            - Patient Weight Input form with dropdown select list of patients, inputs for Weight (lb) and Weight Date, and 'Submit' button to submit form

        Tube Feed Calculator page:

            - Tube Feed Calculator form with dropdown select list of formulas, inputs for Tube Feed Rate (mL/hr) and Time (hr), and 'Calculate' button to submit form

        Tube Feed Nutrition page:

            - Table containing Formula, Tube Feed Rate (mL/hr), Time(hr), kcals, Protein (g), and Fluids (mL)
            - 'Return to Tube Feed Calculator' button to return to previous page

        User History page:

            - Table containing entries for every weight entered by the user
            - Each entry contains Entry ID, User ID, Patient ID, Weight Date, Patient Weight, and Timestamp

    Navigation:

        - User arrives at the Login page, where they can login if they have an account using the login form.
        - If user doesn't have an account, they can access the Registration page using the 'Register' button below the login form, or the 'Register' link at the top right of the page. Upon registration, user will be automatically logged in.
        - Upon login, user is directed to the Patient Roster page (/index), where they can view a table populated with patients registered under their care.
        - Navigation to Patient Information pages is done via the 'View' button in each patient's entry on the Patient Roster page.
        - From each Patient Information page, user can access the weight entry form using the 'Input Patient Weight' button.
        - Patient Entry, Tube Feed Calculator, and User History pages are reached via links in the navbar.
        - After submitting the Tube Feed Calculator form, user arrives at Tube Feed Nutrition page, and can return to previous page using the 'Return to Tube Feed Calculator' button.
        - To return to the Patient Roster page, user can click the Dietitian's Friend brand logo.

    Forms and Inputs:

        - Login Form (/login):
            - inputs: username (text), password (text)

        - Patient Entry Form (/patient_entry):
            - inputs: last name (text), first name (text), age (integer), and bed (text)

        - Registration Form (/register):
            - inputs: username (text), password (text), password confirmation (text)

        - Tube Feed Form (/tubefeed):
            - inputs: formula (select menu), tube feed rate in mL/hr (float), time in hr (integer)

        - Weight Entry Form (/weight_entry):
            - inputs: patient (select menu), weight (float), weight date (date)

    Feedback:

        - Errors and alerts appear as flashed messages at the top of each respective page.
        - Users are also informed if a process is completed successfully.

    Aesthetics:

        - The aesthetics of the app were achieved using Bootstrap and CSS.
        - Text contrasts well with the background colors and is highly legible throughout.
        - Forms are centrally aligned to make the more aesthetically pleasing and legible at all screen sizes.

    Responsiveness:

        - Using Bootstrap, the app is designed to be responsive to the screen size.
        - The navigation bar collapses into to a dropdown menu accesible via a hamburger button.
        - The forms are all natively centrally aligned, and fit well within a small screen.
        - The tables collapse and condense based on the width of the screen, with the data remaining legible via text-wrapping within data cells.

Data:

    - Data stored in a SQL database with following tables:

        - users (id [integer, primary], username [text], hash [text])
            - store user account data

        - roles (id [integer, primary], name [text])
            - store roles (e.g. admin, user)

        - user_role (user_id [integer, foreign], role_id [integer, foreign])
            - store association of user with role

        - patients (id [integer, primary], name_last [text], name_first [text], bed [text], provider_id [integer, foreign], age [integer])
            - store patient information

        - monthly_weights (id [integer, primary], user_id [integer, foreign], patient_id [integer, foreign], weight_date [date], patient_weight [float], timestamp [datetime])
            - store monthly patient weight data

        - weight_check (id [integer, primary], patient_id [integer, foreign], current_weight [real], one_month [real], three_month [real], six_month [real], twelve_month [real], timestamp [datetime])
            - store most recent weight check data

        - formulas (id [integer, primary], name [text], category_id [integer, foreign], kcal_per_ml [float], lactose_int [text], gluten_free [text], kosher [text], features [text], indications [text])
            - store basic data on tube feed formulas

        - categories (id [integer, primary], name [text])
            - store tube feed formula categories

        - nutrients (id [integer, primary], formula_id [integer, foreign], kcals [integer], protein_g [float], fat_g [float], carb_g [float], fiber_g [float], scfos_g [float])
            - store nutrient information for tube feed formulas

        - minerals (id [integer, primary], formula_id [integer, foreign], sodium_mg [integer], potassium_mg [integer], phosphorus_mg [integer], magnesium_mg [integer], vitk_mcg [integer])
            - store mineral information for tube feed formulas

        - fluids (id [integer, primary], formula_id [integer, foreign], free_water_percent [float], water_ml [integer], osmolality [integer])
            - store fluid information for tube feed formulas

Algorithms and Data Structures:

    User Authentication and Registration:

        - SQL query to check if a username already exists during registration:
            user = User.query.filter_by(username=username).first()

    Patient Management:

        - SQL query to retreive patients under care of specific user for patient roster:
            patients = Patient.query.filter_by(provider_id=session["user_id"]).all()

        - SQL query to insert new patient into database:
            new_patient = Patient(name_last=name_last, name_first=name_first, age=age, bed=bed, provider_id=session["user_id"])
            db.session.add(new_patient)
            db.session.commit()

    Patient Information and Weight Tracking:

        - SQL query to retreive patient information for specific patient:
            patient = Patient.query.get(patient_id)

        - SQL query to retreive patient's most recent weight check:
            weight_check_row = WeightCheck.query.filter_by(patient_id=patient_id).first()

        - SQL query to retreive most recent weight to calculate percent weight change at different intervals:
            current_weight = MonthlyWeights.query.filter_by(patient_id=patient_id).order_by(MonthlyWeights.weight_date.desc()).first()

        - SQL query to update weight check data:
            weight_check_row.current_weight = current_weight.patient_weight
            weight_check_row.one_month = one_month
            weight_check_row.three_month = three_month
            weight_check_row.six_month = six_month
            weight_check_row.twelve_month = twelve_month
            weight_check_row.timestamp = datetime.now()
            db.session.add(weight_check_row)
            db.session.commit()

        - SQL query to fetch monthly weight records for patient:
            monthly_weights = MonthlyWeights.query.filter_by(patient_id=patient_id).order_by(MonthlyWeights.weight_date.desc()).all()

    Weight Change Tracking:

        - SQL query to find weight record at the closest date before the calculated date:
            weight_at_interval_ago = (MonthlyWeights.query.filter_by(patient_id=patient_id).filter(MonthlyWeights.weight_date <= interval_ago).order_by(MonthlyWeights.weight_date.desc()).first())

        - SQL query to find weight record one month before interval month, for finding average in case of missing interval weight:
            weight_before = (MonthlyWeights.query.filter(MonthlyWeights.patient_id == patient_id, MonthlyWeights.weight_date == interval_ago_before,).order_by(MonthlyWeights.weight_date.desc()).first())

        - SQL query to find weight record one month after interval month, for finding average in case of missing interval weight:
            weight_before = (MonthlyWeights.query.filter(MonthlyWeights.patient_id == patient_id, MonthlyWeights.weight_date == interval_ago_after,).order_by(MonthlyWeights.weight_date.desc()).first())

    Tube Feed Calculator:

        - SQL query to retreive info for selected tube feed formula:
            formula = Formula.query.filter_by(id=formula_id).first()

        - SQL query to retreive nutrient info for selected tube feed formula:
            formula_nutrients = Nutrients.query.filter_by(formula_id=formula_id).first()

        - SQL query to retreive fluid info for selected tube feed formula:
            formula_fluids = Fluids.query.filter_by(formula_id=formula_id).first()

    User History:

        - SQL query to retreive hostory of patient weights for specific user:
            history = MonthlyWeights.query.filter_by(user_id=session["user_id"]).all()

Modules and Functions:

    - Module: app.py

        - Purpose: This file is the main driver of the Flask application, and contains the app's main functions

        - Function: create_app()
            - Description: Configures application
            - Inputs: none
            - Returns: app

        - Function: after_request()
            - Description: Ensures responses aren't cached
            - Inputs: one passed variable (response)
            - Returns: response

        - Function: login()
            - Description: Logs user in
            - Inputs: two form inputs (username, password)
            - Returns: user logged in and redirected to index

        - Function: logout()
            - Description: Logs user out
            - Inputs: none
            - Returns: user logged out and redirected to login

        - Function: register()
            - Description: Registers user
            - Inputs: three form inputs (username, password, confirmation)
            - Returns: user registered, logged in, and redirected to index

        - Function: index()
            - Description: Renders index, which shows roster of patients
            - Inputs: none
            - Returns: roster of patients

        - Function: patient_entry()
            - Description: Inputs patients into database
            - Inputs: four form inputs (name_last, name_first, age, bed)
            - Returns: patient entered into database, user redirected to index

        - Function: patient_info()
            - Description: Shows patient information
            - Inputs: one passed variable (patient_id)
            - Returns: patient information displayed, including most recent weight check, nutritional needs based on current weight, and log of patient weights

        - Function: weight_entry()
            - Description: Inputs patient weights
            - Inputs: three form inputs (patient, weight, weight_date)
            - Returns: weight added to database, user redirected to patient information page

        - Function: weight_check()
            - Description: Performs weight check at given intervals
            - Inputs: one passed variable (patient_id)
            - Returns: weight check, redirect to patient information page where displayed

        - Function: history()
            - Description: Shows history of patient weights input by user
            - Inputs: none
            - Returns: renders history page with log of patient weights entered by user

        - Function: tubefeed()
            - Description: Calculates tube feed nutrition provided
            - Inputs: three form inputs (formula, tube_feed_rate, time)
            - Returns: renders tube feed nutrition page, which displays outputs (kcals, protein, and fluids provided)

    - Module: csv_to_db.py

        - Purpose: This file contains functions to check if a SQL table is empty, and if so, load it with data from coinciding CSV file

        - Function: is_table_empty()
            - Description: Checks if a SQL table is empty
            - Inputs: two passed variables (model, id)
            - Returns: Boolean value storing whether count of IDs in a table is equal to 0

        - Function: load_data_from_csv()
            - Description: Loads data from CSV file into a specified model if not already loaded
            - Inputs: three passed variables (csv_file, model, id)
            - Returns: SQL tables populated with static data from CSV

    - Module: extensions.py

        - Purpose: Creates an instance of SQLAlchemy() to import and use across different modules in application, ensuring that user is working with the same database session everywhere in the app

    - Module: forms.py

        - Purpose: Contains the forms defined as classes to import and use in the application

        - Class: LoginForm()
            - Description: Form for user to input login credentials
            - Fields: username, password

        - Class: PatientEntryForm()
            - Description: Form for user to input new patient
            - Fields: name_last, name_first, age, bed

        - Class: PatientInfoForm()
            - Description: Form for user to access patient information
            - Fields: view (submit button)

        - Class: RegistrationForm()
            - Description: Form for user to register
            - Fields: username, password, confirmation

        - Class: TubeFeedForm()
            - Description: Form for user to calculate tube feed nutrition
            - Fields: formulas, tube_feed_rate, time

        - Class: WeightForm()
            - Description: Form for user to input new patient weight
            - Fields: patient, weight, weight_date

    - Module: helpers.py

        - Purpose: Contains helper functions used in main application

        - Function: login_required()
            - Description: Decorate routes to require login

        - Function: weight_change()
            - Description: Calculates percentage weight change in a given interval of months
            - Inputs: four passed variables (patient_id, interval_months, current_weight, weight_date)
            - Returns: percent_change

    - Module: models.py

        - Purpose: Stores models for SQLAlchemy to communicate with SQL tables

        - Association Table: user_role
            - Description: Association table connecting users to roles
            - Fields: user_id, role_id

        - Class: User()
            - Description: Model for users SQL table
            - Fields: id, username, hash, roles

        - Class: Role()
            - Description: Model for roles SQL table
            - Fields: id, name, users

        - Class: Patient()
            - Description: Model for patients SQL table
            - Fields: id, name_last, name_first, age, bed, provider_id

        - Class: MonthlyWeights()
            - Description: Model for monthly_weights SQL table
            - Fields: id, user_id, patient_id, weight_date, patient_weight, timestamp

        - Class: WeightCheck()
            - Description: Model for weight_check SQL table
            - Fields: id, patient_id, current_weight, one_month, three_month, six_month, twelve_month, timestamp

        - Class: Formula()
            - Description: Model for formulas SQL table
            - Fields: id, name, category_id, kcal_per_ml, lactose_int, gluten_free, kosher, features, indications

        - Class: Category()
            - Description: Model for categories SQL table
            - Fields: id, name

        - Class: Nutrients()
            - Description: Model for nutrients SQL table
            - Fields: id, formula_id, kcals, protein_g, fat_g, carb_g, fiber_g, scfos_g

        - Class: Minerals()
            - Description: Model for minerals SQL table
            - Fields: id, formula_id, sodium_mg, potassium_mg, phosphorus_mg, magnesium_mg, vitk_mcg

        - Class: Fluids()
            - Description: Model for fluids SQL table
            - Fields: id, formula_id, free_water_percent, water_ml, osmolality

    - Module: schema.sql

        - Purpose: Contains the SQL commands to set up database.

Testing:

    - The application was tested using fake patient info and data.
    - Each process was tested in branching sequences to check for errors.
    - Errors, when encountered, were debugged and resolved.