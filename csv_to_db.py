# # Copyright (C) 2023 Anthony Ryan Shannon/Ars Artis Softworks

import csv
import logging

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Set up SQLAlchemy
engine = create_engine("sqlite:///instance/diet.db")

Session = sessionmaker(bind=engine)

session = Session()

# Create a logger
logger = logging.getLogger(__name__)


def is_table_empty(model, id):
    """Check if table is empty"""
    count = session.query(func.count(getattr(model, id))).scalar()
    return count == 0


def load_data_from_csv(csv_file, model, id):
    """Load data from a CSV file into a specified model if not already loaded"""
    # Check if database table is already populated
    if is_table_empty(model, id):
        try:
            # Open CSV file
            with open(csv_file, "r") as csvfile:
                csvreader = csv.DictReader(csvfile)

                # For each row in the CSV file:
                for row in csvreader:
                    # Create a new instance of the model, setting each attribute to the corresponding value in the row
                    instance = model(**row)

                    # Add the new instance to the SQLAlchemy session
                    session.add(instance)

        # Handle any exceptions appropriately, such as file not found or data conversion errors
        except FileNotFoundError:
            logger.error(
                "Error: File not found. Please check the file path and try again."
            )
        except ValueError:
            logger.error("Error: There was a problem converting the data.")

        # After the loop, commit the session to insert all the new instances into the database
        session.commit()


# After all data has been loaded, close session
session.close()
