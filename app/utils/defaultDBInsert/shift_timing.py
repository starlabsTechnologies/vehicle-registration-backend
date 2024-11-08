from app.schema.shiftTiming import ShiftTiming
from app.config.db_config import SessionLocal
from datetime import time

def automate_saving_default_shifts():
    db=SessionLocal() 
    # Check if any data already exists in the shift_timing table
    existing_shifts = db.query(ShiftTiming).count()
    
    if existing_shifts == 0:
        # If no data exists, insert the default shifts
        default_shifts = [
            ShiftTiming(shift_name="A Shift", from_time=time(6,00,00), to_time=time(13,59,59)),
            ShiftTiming(shift_name="B Shift", from_time=time(14,00,00), to_time=time(21,59,59)),
            ShiftTiming(shift_name="C Shift", from_time=time(22,00,00), to_time=time(5,59,59)),
        ]
        
        db.add_all(default_shifts)
        db.commit()
        print("Default shift timings have been inserted successfully.")
    else:
        print("Shift timings already exist.")