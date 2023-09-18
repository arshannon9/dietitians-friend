# Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks

from extensions import db

# Association table linking users to roles
association_table = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


# Models for user and patient storage
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    roles = db.relationship("Role", secondary=association_table, back_populates="users")


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    users = db.relationship("User", secondary=association_table)


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_last = db.Column(db.Text)
    name_first = db.Column(db.Text)
    age = db.Column(db.Integer)
    bed = db.Column(db.Text)
    provider_id = db.Column(db.Integer, db.ForeignKey("users.id"))


# Models for weights functionality
class MonthlyWeights(db.Model):
    __tablename__ = "monthly_weights"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    weight_date = db.Column(db.Date, nullable=False)
    patient_weight = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)


class WeightCheck(db.Model):
    __tablename__ = "weight_check"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    current_weight = db.Column(db.Float)
    one_month = db.Column(db.Float)
    three_month = db.Column(db.Float)
    six_month = db.Column(db.Float)
    twelve_month = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)


# Models for tube feed and nutrition functionality
class Formula(db.Model):
    __tablename__ = "formulas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    kcal_per_ml = db.Column(db.Float)
    lactose_int = db.Column(db.Text)
    gluten_free = db.Column(db.Text)
    kosher = db.Column(db.Text)
    features = db.Column(db.Text)
    indications = db.Column(db.Text)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class Nutrients(db.Model):
    __tablename__ = "nutrients"
    id = db.Column(db.Integer, primary_key=True)
    formula_id = db.Column(db.Integer, db.ForeignKey("formulas.id"))
    kcals = db.Column(db.Integer)
    protein_g = db.Column(db.Float)
    fat_g = db.Column(db.Float)
    carb_g = db.Column(db.Float)
    fiber_g = db.Column(db.Float)
    scfos_g = db.Column(db.Float)


class Minerals(db.Model):
    __tablename__ = "minerals"
    id = db.Column(db.Integer, primary_key=True)
    formula_id = db.Column(db.Integer, db.ForeignKey("formulas.id"))
    sodium_mg = db.Column(db.Integer)
    potassium_mg = db.Column(db.Integer)
    phosphorus_mg = db.Column(db.Integer)
    magnesium_mg = db.Column(db.Integer)
    vitk_mcg = db.Column(db.Integer)


class Fluids(db.Model):
    __tablename__ = "fluids"
    id = db.Column(db.Integer, primary_key=True)
    formula_id = db.Column(db.Integer, db.ForeignKey("formulas.id"))
    free_water_percent = db.Column(db.Float)
    water_ml = db.Column(db.Integer)
    osmolality = db.Column(db.Integer)
