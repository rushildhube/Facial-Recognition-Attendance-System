import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "enter your database url"
})
reference = db.reference('StudentsData')
data = {
    
    "963852":
        {
            "Name": "Elon Musk",
            "Major": "AI/ML",
            "Current_Year": "SE",
            "Total_Attendance": 0,
            "Last_Attendance_Time": "2024-03-08 01:54:54",
            "Standing": "A",
            "Starting_Year": "2020"
        },

    "852741":
        {
            "Name": "Emily Blunt",
            "Major": "AI/ML",
            "Current_Year": "SE",
            "Total_Attendance": 0,
            "Last_Attendance_Time": "2024-03-08 01:54:54",
            "Standing": "B",
            "Starting_Year": "2020"
        }
}

for key, value in data.items():
    reference.child(key).set(value)
