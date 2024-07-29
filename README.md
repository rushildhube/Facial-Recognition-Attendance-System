# Face Recognition Attendance System

This project is a Face Recognition Attendance System that uses OpenCV and Firebase for real-time face recognition and attendance tracking. The system captures a video stream, recognizes faces, and logs attendance data in a Firebase Realtime Database. It also displays the attendance information on a custom background.

## Features

- Real-time face recognition using OpenCV and face_recognition library
- Attendance tracking and logging using Firebase Realtime Database
- Storage of student images in Firebase Storage
- Customizable background for the display

## Requirements

- Python 3.x
- OpenCV
- face_recognition
- Firebase Admin SDK
- cvzone
- Numpy

## Setup

### Firebase Setup

1. **Create a Firebase Project**

   - Go to [Firebase Console](https://console.firebase.google.com/).
   - Click on "Add Project" and follow the steps to create a new project.

2. **Set Up Firebase Realtime Database**

   - In the Firebase Console, go to "Database" and then "Realtime Database".
   - Click on "Create Database" and follow the steps to set up the database.
   - Set the database rules to:
     ```json
     {
       "rules": {
         ".read": "auth != null",
         ".write": "auth != null"
       }
     }
     ```

   - Get the Realtime Database URL:
     - Click on the "Data" tab under "Realtime Database".
     - Copy the database URL from the top of the page (e.g., `https://your-database-url.firebaseio.com`).

3. **Set Up Firebase Storage**

   - In the Firebase Console, go to "Storage".
   - Click on "Get Started" and follow the steps to set up Firebase Storage.
   - Set the storage rules to:
     ```json
     rules_version = '2';
     service firebase.storage {
       match /b/{bucket}/o {
         match /{allPaths=**} {
           allow read, write: if request.auth != null;
         }
       }
     }
     ```

   - Get the Storage Bucket URL:
     - Click on the "Files" tab under "Storage".
     - Copy the storage bucket URL from the top of the page (e.g., `your-storage-bucket-url.appspot.com`).

4. **Download the Firebase Admin SDK**

   - In the Firebase Console, go to "Project Settings" and then "Service accounts".
   - Click on "Generate new private key" and download the `serviceAccountKey.json` file.
   - Save the `serviceAccountKey.json` file in your project directory.

### Python Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/face-recognition-attendance.git
   cd face-recognition-attendance
   ```

2. **Install Dependencies**

   ```bash
   pip install opencv-python
   pip install face_recognition
   pip install firebase-admin
   pip install cvzone
   pip install numpy
   ```

3. **Configure Firebase Credentials**

   - Replace `"enter your database url"` and `"enter your storage bucket url from firebase"` in `main.py` and `Encode Generator File` with your Firebase Realtime Database URL and Storage Bucket URL respectively.
   - Example:
     ```python
     firebase_admin.initialize_app(cred, {
         'databaseURL': "https://your-database-url.firebaseio.com",
         'storageBucket': "your-storage-bucket-url.appspot.com"
     })
     ```

### Running the Project

1. **Add Student Data to Firebase**

   - Run the `AddDataToDatabase.py` script to add initial student data to Firebase Realtime Database.
     ```bash
     python AddDataToDatabase.py
     ```

2. **Generate Face Encodings**

   - Run the `EncodeGenerator.py` script to generate face encodings and save them to a file.
     ```bash
     python EncodeGenerator.py
     ```

3. **Start the Face Recognition Attendance System**

   - Run the `main.py` script to start the face recognition attendance system.
     ```bash
     python main.py
     ```

## Project Structure

- `main.py`: Main script to run the face recognition attendance system.
- `EncodeGenerator.py`: Script to generate face encodings and save them to a file.
- `AddDataToDatabase.py`: Script to add initial student data to Firebase Realtime Database.
- `serviceAccountKey.json`: Firebase Admin SDK private key (downloaded from Firebase Console).
- `Images/`: Folder containing student images.
- `Resources/`: Folder containing background and mode images.

## Notes

- Ensure all student images are 216x216 pixels in a 1:1 aspect ratio.
- The system uses a USB webcam to capture video. If using a different camera, adjust the `webcam` variable in `main.py`.

## Troubleshooting

- **No face found in image**: Ensure the image has a clear, front-facing face.
- **Invalid face encoding found in image**: Ensure the image resolution is sufficient for face recognition.
- **Database connection issues**: Verify your Firebase credentials and database URL.
- **Storage upload issues**: Verify your Firebase Storage rules and bucket URL.

## Conclusion

This project demonstrates how to build a simple face recognition attendance system using Python, OpenCV, and Firebase. It covers the basics of setting up Firebase, capturing and processing images, and logging attendance data. Feel free to customize and extend the project to fit your specific needs.

---
