-- Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks
-- Schema for SQL database
-- Tables to store user data
CREATE TABLE
  users (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username)
  );

CREATE TABLE
  roles (id INTEGER NOT NULL, name TEXT, PRIMARY KEY (id));

CREATE TABLE
  user_role (
    user_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (role_id) REFERENCES roles (id)
  );

-- Table to store patient bio, weight, and weight check data
CREATE TABLE
  patients (
    id INTEGER NOT NULL,
    name_last TEXT,
    name_first TEXT,
    bed TEXT,
    provider_id INTEGER,
    age INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (provider_id) REFERENCES users (id)
  );

CREATE TABLE
  monthly_weights (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    weight_date DATE NOT NULL,
    patient_weight FLOAT,
    TIMESTAMP DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY (patient_id) REFERENCES patients (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
  );

CREATE TABLE
  weight_check (
    id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    current_weight REAL,
    one_month REAL,
    three_month REAL,
    six_month REAL,
    twelve_month REAL,
    TIMESTAMP DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patients (id),
    PRIMARY KEY (id)
  );

-- Tables to store data for tube feed calculations
CREATE TABLE
  formulas (
    id INTEGER NOT NULL,
    name TEXT,
    category_id INTEGER,
    kcal_per_ml FLOAT,
    lactose_int TEXT,
    gluten_free TEXT,
    kosher TEXT,
    features TEXT,
    indications TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
  );

CREATE TABLE
  categories (id INTEGER NOT NULL, name TEXT, PRIMARY KEY (id));

CREATE TABLE
  nutrients (
    id INTEGER NOT NULL,
    formula_id INTEGER,
    kcals INTEGER,
    protein_g FLOAT,
    fat_g FLOAT,
    carb_g FLOAT,
    fiber_g FLOAT,
    scfos_g FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY (formula_id) REFERENCES formulas (id)
  );

CREATE TABLE
  minerals (
    id INTEGER NOT NULL,
    formula_id INTEGER,
    sodium_mg INTEGER,
    potassium_mg INTEGER,
    phosphorus_mg INTEGER,
    magnesium_mg INTEGER,
    vitk_mcg INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (formula_id) REFERENCES formulas (id)
  );

CREATE TABLE
  fluids (
    id INTEGER NOT NULL,
    formula_id INTEGER,
    free_water_percent FLOAT,
    water_ml INTEGER,
    osmolality INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (formula_id) REFERENCES formulas (id)
  );