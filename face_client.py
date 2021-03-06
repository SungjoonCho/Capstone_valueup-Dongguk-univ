import os
import sys
import cv2
import numpy as np

import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyrebase import pyrebase

import time
import threading
from threading import Thread
import socket


global video_capture

# firebase storage db

config = {
    "apiKey" : "",
    "authDomain": "",
    "databaseURL" : "",
    "storageBucket" : ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage() 

HOST = '' 
PORT = 9009 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("server connected") 

#Firebase database 인증 및 앱 초기화

cred = credentials.Certificate("")

firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://.firebaseio.com/"
})

def rcvMsg(sock):
 while True:
    try:
       data = sock.recv(1024)
       data = data.decode()
       print(data)
       msg_list = data.split(',')
       
       if 'face_append' in msg_list[0]:
           time.sleep(3)
           print('appending face encoding & opening face recog program again')
           name = msg_list[1]         
           storage.child('pic_'+ name).download(name + ".jpg","")
           time.sleep(7)
           print("New person save complete")
 
           break

       elif 'del' in msg_list[0]:
           print('deleting face encoding & opening face recog program again')    
           name = msg_list[1]
           try:
               os.remove('pic_' + name +'.jpg')
               print(name + "delete complete")

           except:
               print("file remove failed")
           time.sleep(3)
           break

       if not data:
           break

    except:
       pass
 

def face_recog(t):
    count = {"Unknown" : 0} 
    video_capture= cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    print('Encoding for new person')
    ref = db.reference('face/') 
    people = ref.get().keys() 
    known_face_encodings = []
    known_face_names = []

    for i in people:
        known_face_names.append(i)
        count[i] = 0
        tem = face_recognition.load_image_file(i+'.jpg')
        known_face_encodings.append(face_recognition.face_encodings(tem)[0])

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True 

    print('Program Start')

    while True:
        ret, frame = video_capture.read() 

        if not t.is_alive():
            video_capture.release()
            cv2.destroyAllWindows()
            time.sleep(1)
            args = sys.argv[:] 
            args.insert(0, sys.executable) 

            if sys.platform == 'win32':
              args = ['"%s"' % arg for arg in args] 
            os.execv(sys.executable, args) 
            sys.exit()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame: 

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):

            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            count[name] += 1

            if count[name] == 5:
                msg = 'enter,' + name                
                sock.send(msg.encode())
                sock.send('\n'.encode())
                time.sleep(0.5) 

                for i in count.keys():
                   count[i] = 0

                time.sleep(10)
                video_capture.release()
                cv2.destroyAllWindows()
                time.sleep(1)
                args = sys.argv[:] 
                args.insert(0, sys.executable) 

                if sys.platform == 'win32':
                  args = ['"%s"' % arg for arg in args] 

                os.execv(sys.executable, args) 
                sys.exit()
    
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

 
# Release handle to the webcam
t1 = Thread(target=rcvMsg, args=(sock,))
t2 = Thread(target=face_recog, args=(t1,))
t1.start()
