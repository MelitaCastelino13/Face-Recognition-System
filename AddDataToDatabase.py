import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-b1876-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
print(ref.get())
data = {
    "1046":
        {
            "name": "Abhishek N Parmar",
            "major": "AI/ML",
            "starting_year": 2022,
            "total_attendance": 10,
            "year": 4,
            "last_attendance_time": "07-10-2023 18:23:46",
        },
    "1111":
        {
            "name": "Ronit Kothari",
            "major": "AI/ML",
            "starting_year": 2022,
            "total_attendance": 20,
            "year": 5,
            "last_attendance_time": "07-10-2023 18:23:46",
        },
    "2222":
        {
            "name": "Raj Shah",
            "major": "Full Stack",
            "starting_year": 2022,
            "total_attendance": 0,

            "year": 8,
            "last_attendance_time": "07-10-2023 18:23:46",
        },
    "16545":
        {
            "name": "Param ",
            "major": "Full Stack",
            "starting_year": 2022,
            "total_attendance": 0,
            "year": 8,
            "last_attendance_time": "07-10-2023 18:23:46",
        },
    "3333":
        {
            "name": "Rizwan ",
            "major": "Full Stack",
            "starting_year": 2022,
            "total_attendance": 5,

            "year": 8,
            "last_attendance_time": "07-10-2023 18:23:46",
        },

}
for key, value in data.items():
    ref.child(key).set(value)
