from app.config.db_config import init_db
from app.utils.defaultDBInsert.shift_timing import automate_saving_default_shifts

def initialize_db():
    try:
        init_db()  # Initialize and create tables
        print("Database connection established successfully!")

        automate_saving_default_shifts()
    except Exception as e:
        print(f"Error during database initialization: {e}")