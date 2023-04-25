"""
Our main application logic
"""

from database import init_db, db_session
from models import *
from sqlalchemy import func

"""
This function assumes the user makes 
no mistakes and that there are no duplicates
"""
def update_appt():
    # Get user information
    name = input("What is your pet's name?\n")
    date = input("When is the appointment you would like to change? (YYYY-MM-DD)\n")

    # TODO: Get all the necessary information for line 24
    # Hint: You may need more than the 2 queries to accomplish this

    # Query 1:
    results = db_session.query(appts.)
    db_session.flush()

    # Query 2:
    time = db_session.query(time)
    db_session.flush()

    appt = None
    vet = None

    print("Great! I have the following appointment:")
    print(appt.date + " at " + appt.time + " with " + str(vet))

    # Reschedule or Cancel the Appointment
    response = input("Would you like to reschedule or cancel this appointment?\n")

    if response == "cancel":
        # TODO: Cancel the appointment
        print("Your appointment has been cancelled. Thank you!")
    else:
        new_date = input("When would you like to change your appointment to? (YYYY-MM-DD)\n")
        # TODO: Reschedule the appointment
        
        print("Great! You now have the following appointment:")
        print(appt.date + " at " + appt.time + " with " + str(vet))

        # Verify the new appointment before saving
        verify = input("Is that correct? (Y/N)\n")
        if(verify == "N"):
            # TODO: What should happen here?
            print("Oh well. Better luck next time.")
        else:
            # TODO: What should happen here?
            print("Your appointment has been updated")

# Initialize our database
init_db()

update_appt()

# Remove the session at the very end
db_session.remove()
