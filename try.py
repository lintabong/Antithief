import cv2
import mediapipe as mp
import numpy
import pyrebase
import time

from datetime import datetime

firebaseConfig = {
    'apiKey': "AIzaSyAFUpKuRWlC2rCIKSEd9pWP9ULgpCDAaLU",
    'authDomain': "antithiefdb.firebaseapp.com",
    'databaseURL': "https://antithiefdb-default-rtdb.firebaseio.com",
    'projectId': "antithiefdb",
    'storageBucket': "antithiefdb.appspot.com",
    'messagingSenderId': "191607734669",
    'appId': "1:191607734669:web:3286b29294e8b105047dc4",
    'measurementId': "G-XWWZNJ7SCJ"
}

firebase    = pyrebase.initialize_app(firebaseConfig)
storage     = firebase.storage()
db          = firebase.database()

scale_percent   = 25
width           = int(640*scale_percent/100)
height          = int(480*scale_percent/100)
dsize = (width, height)

pushnotif = 'no'

cam = cv2.VideoCapture(0)
i = 0
while True:
    ret, img = cam.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.flip(img, 1)
    img = cv2.resize(img, dsize)

    cv2.imshow("frame", img)
    cv2.imwrite("myAct.jpg", img)
    storage.child("images/example.jpg").put("myAct.jpg")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    currentTime = datetime.now().strftime("%H:%M:%S")
    print(i, currentTime)

    i += 1
    if i == 10:
        i = 0
        pushnotif = 'active'
    else:
        pushnotif = 'no'

    if (i%2) == 0:
        img_address = 'https://firebasestorage.googleapis.com/v0/b/antithiefdb.appspot.com/o/images%2Fexample.jpg?alt=media' \
              '&token=66dbe5bc-4cac-4c30-a97c-986a29bdbdb5'
    else:
        img_address = 'https://firebasestorage.googleapis.com/v0/b/antithiefdb.appspot.com/o/images%2Fexample.jpg?alt=media' \
              '&token=66dbe5bc-4cac-4c30-a97c-986a29bdbdb5b'

    data = {
        'activity': 'berdiri',
        'status': 'aman',
        'pushnotif': pushnotif,
        'image': img_address,
        'time' : str(currentTime),
    }
    db.update(data)

    time.sleep(0.5)

cam.release()
cv2.destroyAllWindows()
