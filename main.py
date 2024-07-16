# please keep all the image size as 216 x 216 in 1:1 aspect ratio
from _datetime import datetime
import os
import pickle
import numpy as np
import cvzone
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "enter your database url",
    'storageBucket': "enter your storage bucket url from firebase"
})

bucket = storage.bucket()
webcam = cv2.VideoCapture(0)
webcam.set(3, 640)
webcam.set(4, 480)

img_background = cv2.imread("Resources/background.png")

# Importing Mode Images In A List
foldermodepath = "Resources/Modes"
modepathlist = os.listdir(foldermodepath)
imagemodelist = []
for path in modepathlist:
    imagemodelist.append(cv2.imread(os.path.join(foldermodepath, path)))
# print(len(imagemodelist))


# loading the encodings
print("Loading Encode File")
file = open('EncodeFile.p', 'rb')
encodeListknowmwithIDs = pickle.load(file)
file.close()
encodeListknowm, StudentIDs = encodeListknowmwithIDs
# for encode in encodeListknowm:
#     print("Shape of encode in list:", len(encode))
# print("Length of encodeListknowm:", len(encodeListknowm))
# print(StudentIDs)
print("Encode File Loaded Successfully")

modeType = 1
counter = 0
id = -1
imgstudent = []

# A While Loop To Display Everything
while True:
    isTrue, web_img = webcam.read()

    imgsmall = cv2.resize(web_img, (0, 0), None, 0.25, 0.25)
    imgsmall = cv2.cvtColor(imgsmall, cv2.COLOR_BGR2RGB)

    facecurrentframe = face_recognition.face_locations(imgsmall)
    encodecurrentframe = face_recognition.face_encodings(imgsmall, facecurrentframe)

    img_background[162:162 + 480, 55:55 + 640] = web_img
    img_background[44:44 + 633, 808:808 + 414] = imagemodelist[modeType]

    if facecurrentframe:

        for encodeface, facelocation in zip(encodecurrentframe, facecurrentframe):
            # print("Shape of encodeface:", encodeface.shape)
            matches = face_recognition.compare_faces(encodeListknowm, encodeface)
            facedistance = face_recognition.face_distance(encodeListknowm, encodeface)
            # print("matches :", matches)
            # print("face distance", facedistance)

            matchIndex = np.argmin(facedistance)
            # print(matchIndex)
            if matches[matchIndex]:
                # print("Known Face Detected.")
                # print("Roll No: - ", StudentIDs[matchIndex])
                y1, x2, y2, x1 = facelocation
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                img_background = cvzone.cornerRect(img_background, bbox, rt=0)
                id = StudentIDs[matchIndex]
                # print(id)
                if counter == 0:
                    cvzone.putTextRect(img_background, "Loading", (275, 400))
                    cv2.imshow("FACE RECOGNITION ATTENDANCE SYSTEM", img_background)
                    cv2.waitKey(1)
                    counter = 1
                    ModeType = 1

        if counter != 0:

            if counter == 1:
                # getting data
                studentinfo = db.reference(f'StudentsData/{id}').get()
                print(studentinfo)

                # get image from storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgstudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update attendance data
                datetimeObject = datetime.strptime(studentinfo['Last_Attendance_Time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 10:  # put hours in seconds for full attendance system
                    ref = db.reference(f'StudentsData/{id}')
                    studentinfo['Total_Attendance'] += 1
                    ref.child('Total_Attendance').set(studentinfo['Total_Attendance'])
                    ref.child('Last_Attendance_Time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    img_background[44:44 + 633, 808:808 + 414] = imagemodelist[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                img_background[44:44 + 633, 808:808 + 414] = imagemodelist[modeType]

                if counter <= 10:
                    cv2.putText(img_background, str(studentinfo['Total_Attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)

                    cv2.putText(img_background, str(studentinfo['Major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)

                    cv2.putText(img_background, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)

                    cv2.putText(img_background, str(studentinfo['Standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)

                    cv2.putText(img_background, str(studentinfo['Current_Year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX,
                                0.6,
                                (100, 100, 100), 1)

                    cv2.putText(img_background, str(studentinfo['Starting_Year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentinfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2

                    cv2.putText(img_background, str(studentinfo['Name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX,
                                1,
                                (50, 50, 50), 1)

                    img_background[175:175 + 216, 909:909 + 216] = imgstudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentinfo = 0
                    imgstudent = []
                    img_background[44:44 + 633, 808:808 + 414] = imagemodelist[modeType]
    else:
        modeType = 0
        counter = 0

    # cv2.imshow("WEBCAM", web_img)
    cv2.imshow("FACE RECOGNITION ATTENDANCE SYSTEM", img_background)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord("x"):
        break
