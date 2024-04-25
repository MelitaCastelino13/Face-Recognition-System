import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-recognition-b1876-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recognition-b1876.appspot.com",
})

# Open the camera (usually 0 or 1 for built-in webcams)
cap = cv2.VideoCapture(0)

# Set the desired resolution
cap.set(3, 640)  # Width
cap.set(4, 480)   # Height

imgBackground = cv2.imread('Resources/Background.png')

# importing the mode images into the list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# load the encoding file
print("Loading Encoded file ..")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)

encodeListKnown, studentsIds = encodeListKnownWithIds
print("Closing Encoded file ..")

modetype = 0
counter = 0
id = -1
break_loop = False

while not break_loop:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[62:141, 55:95] = imgModeList[0][0:79, 0:40]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print("matches", matches)
        print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        print("Macth Index", matchIndex)

        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentsIds[matchIndex]
            if counter == 0:
                counter = 1
                modetype = 1
                #break_loop = True  # Break the loop on successful recognition

    if counter != 0:
        if counter == 1:
            studentInfo = db.reference(f'Students/{id}')
            current_attendance = studentInfo.child("total_attendance").get()
            last_attendance_time_str = studentInfo.child("last_attendance_time").get()
            
            # Convert the last attendance time string to datetime
            datetimeObject = datetime.strptime(last_attendance_time_str, '%d-%m-%Y %H:%M:%S')
            
            # Calculate the time elapsed in seconds
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            
            print(studentInfo)
            print("Time elapsed since last attendance:", secondsElapsed, "seconds")
            
            # Check if the timeout (30 seconds) has passed
            if secondsElapsed >= 30:
                # Increment the attendance count
                new_attendance = current_attendance + 1
                
                # Update the "total_attendance" field in the database
                studentInfo.update({"total_attendance": new_attendance})
                
                print(f"Updated attendance for student {id} to {new_attendance}")
                
                # Update the last attendance time to the current time
                new_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                
                studentInfo.update({"last_attendance_time": new_time})
            else:
                counter = 0

        counter += 1
    
        if counter >= 20:
            counter = 0
            studentInfo = []
            imgStudent = []

    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()