# DIETITIAN'S FRIEND

## A Python-based web application, built using the Flask framework, intended for use by dietitians in a clinical context, aiding users in providing correct care for patient populations.

### Demo: [Watch Demo Video](https://youtu.be/24hW9lJdbHU)

**Features:**

- The application can be used to:

  - Register individual providers to track care for patients
  - Store patient data in SQL database for use in clinical calculations
  - Track weight change over time and check weight gain/loss significance benchmarks
  - Determine nutritional needs based on patient's age and weight
  - Calculate tube feed requirements based on patient's nutritional needs

- This application utilizes several security features:
  - User password policy that encourages creating stronger passwords
  - User password hashing with bcrypt
  - CSRF protection of form inputs
  - Session management using 'filesystem'
  - Randomly generated secret key used to sign session cookies and secure sensitive data
  - SQL injection prevention via SQLAlchemy
  - Error handling to prevent exposure of sensitive information
  - Data validation using Flask-WTF form validation to prevent malicious data entry

**How to Run:**

1. **Installation:**

   - Python v.3.11.4 [Download Python](https://www.python.org/downloads/release/python-3114/) and Flask v.2.3.2 [Download Flask](https://pypi.org/project/Flask/) need to be installed.

2. **Set up a virtual environment:**

   - In the terminal, enter the command `python3 -m venv env`
   - If using Unix/macOS, enter `source env/bin/activate`
   - If using Windows, enter `.\env\Scripts\activate`

3. **Run the app:**
   - To start the Flask server, enter `flask run` in the terminal and click the link provided.

**Usage Guide:**

1. **Login/Register:**

   - The first page you encounter will be the Login page, which contains a login form and two buttons, labeled 'Login' and 'Register'. 'Login' and 'Register' links are also found in the top right of the page.
   - If visiting for the first time, click the 'Register' button, which will take you to the Register page. Fill out and submit the registration form, and if successful, you will be logged in automatically.
   - If already registered, fill out the login form and click the 'Login' button.

2. **Patient Roster:**

   - Upon login, you are directed to the Patient Roster page, which displays all patients currently registered under your care. Patients are displayed in a table, each with a button used to access the patient's information.
   - In the navbar at the top left of the Patient Roster page, there are links to the 'Patient Entry', 'Tube Feed', and 'History' pages, as well as a 'Logout' link at the top right.

3. **Patient Entry:**

   - Clicking the 'Patient Entry' link in the navbar will bring you to the Patient Entry page. Use this form to input the name, age, and bed number of a new patient.

4. **Patient Information:**

   - Each patient has a Patient Information page containing tables displaying their most recent Weight Check, a log of their Weights, and a calculation of their nutritional needs (kcals, protein, fluids) based on their most recent weight.

5. **Weight Input:**

   - To enter a new patient weight, click the 'Input Patient Weight' button above the Weight Log. This button will bring you to a new page with a form for inputting the patient ID, weight, and the date the weight was taken.
   - The Weight Log stores this information, along with a timestamp to see when weights were entered (sometimes old weights need to be entered, or there is a delay between weighing and recording).

6. **Weight Check:**

   - After you enter a new patient weight, click the 'Update Weight Check' button below the Weight Check table to recalculate the weight change percentages for each month interval benchmark.
   - If the weight change (loss or gain) is within the parameters of the month interval benchmark (5% for 1 month, 7.5% for 3 months, 10% for 6 months, 20% for 12 months), the weight check value will be displayed in GREEN. If not, it will be displayed in RED, signaling a clinically significant weight change at the month interval.

7. **Tube Feed:**

   - Access the Tube Feed page via the 'Tube Feed' link in the navbar. This page presents a form for choosing a tube feed formula and inputting tube feed rate (mL/hr) and time (hrs).
   - After clicking the 'Calculate' button, a new page will display a table with the nutrients provided (kcals, grams of protein, fluid volume).
   - Click the 'Return to Tube Feed Calculator' button to return to the previous page.

8. **History:**
   - If you click the History link in the navbar, you will access a log of all weights entered by the user for all patients under their care.

**Dependencies:**

- bcrypt
- Flask
- Flask-Session
- Flask-WTF
- python-dateutil
- SQLAlchemy
- WTForms

**Database Schema:**

The schema for the SQL database is found in the file 'schema.sql'. The models utilized by SQLAlchemy are found in 'models.py'.

**Technologies Used:**

The application consists of:

- Frontend built using HTML, CSS, and JavaScript, with style enhancements using Bootstrap, and form handling via WTForms.
- Backend built using Python and Flask, communicating with SQLite3 database using SQLAlchemy, and session management via Flask-Session.

**License:**

GPL-3.0

**Future Improvements:**

**Backend:**

- Data encryption
- Improved authentication and authorization systems
- Admin-only access protocols

**Frontend:**

- Increase nutritional needs functionality by incorporating more complex calculations for different age groups and disease states

**Credits:**

Thanks to:

- The Diet Office at Hebrew Rehabilitation Center for inspiring the creation of this project.
- David Malan and the Harvard cs50 crew for laying the knowledge foundations for this project.
