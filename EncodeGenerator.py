import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "enter your database url",
    'storageBucket': "enter your bucket database url"
})

# Importing Student Images
imagefolderpath = "Images"
imagePathlist = os.listdir(imagefolderpath)
# print(imagePathlist)
Studentimglist = []
StudentIDs = []

for path in imagePathlist:
    Studentimglist.append(cv2.imread(os.path.join(imagefolderpath, path)))
    StudentIDs.append(os.path.splitext(path)[0])

    fileName = f'{imagefolderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print("Files Uploaded Successfully")


# print(path)
# print(os.path.splitext(path)[0])

# print(len(Studentimglist))
# print(StudentIDs)


def findEncodings(ImgList):
    encodelist = []
    for img in ImgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode) > 0:
            # print("Shape of encode:", len(encode[0]))  # Check the shape of the encoding
            if len(encode[0]) == 128:
                encodelist.append(encode[0])  # Append only if a valid 128-dimensional encoding is found
            else:
                print("Invalid face encoding found in image.")
        else:
            print("No face found in image.")
    return encodelist


print("Encoding Started ...")
encodeListknowm = findEncodings(Studentimglist)
encodeListknowmwithIDs = [encodeListknowm, StudentIDs]
# print(encodeListknowm)
print("Encoding Completed")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListknowmwithIDs, file)
file.close()
print("File Saved SuccessFully")
