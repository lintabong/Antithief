import cv2
import mediapipe as mp
import numpy
from tensorflow.keras.models import load_model
import pyrebase
import time

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

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

model = load_model('model.h5')
CAT = ['berdiri', 'mengetuk pintu','jongkok','','']

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
db = firebase.database()

scale_percent = 25
width = int(640*scale_percent/100)
height = int(480*scale_percent/100)
print(height, width)

dsize = (width, height)

arrayAct        = [""]*5
currentAct      = ""
currentStat     = ""
cond            = "true"
urlImg          = "https://firebasestorage.googleapis.com/v0/b/antithiefdb.appspot.com/o/images%2Fexample.jpg?alt=media&token=66dbe5bc-4cac-4c30-a97c-986a29bdbdb5"

cam = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    i = 0
    while True:
        ret, img = cam.read()
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = image.shape
                myL = results.pose_landmarks.landmark

        blank = numpy.zeros(shape=[img.shape[0], img.shape[1], img.shape[2]], dtype=numpy.uint8)
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        img = cv2.flip(img, 1)

        copImg = img.copy()
        try:
            crop_img = cv2.resize(blank, (100, 100))
            crop_img = numpy.expand_dims(crop_img, axis=0)

            prediction = model.predict(crop_img)
            index = numpy.argmax(prediction)
            currentAct = CAT[index]
            print(currentAct)
        except:
            pass

        i = i + 1
        if i == 4:
            i = 0

        arrayAct[i] = currentAct

        if arrayAct[0] == CAT[0] and arrayAct[1] == CAT[0] and arrayAct[2] == CAT[0] and arrayAct[3] == CAT[0]:
            currentStat = "aman"
        if arrayAct[0] == CAT[1] and arrayAct[1] == CAT[0] and arrayAct[2] == CAT[0] and arrayAct[3] == CAT[0]:
            currentStat = "aman"
        if arrayAct[0] == CAT[1] and arrayAct[1] == CAT[1] and arrayAct[2] == CAT[0] and arrayAct[3] == CAT[0]:
            currentStat = "aman"
        if arrayAct[0] == CAT[1] and arrayAct[1] == CAT[1] and arrayAct[2] == CAT[1] and arrayAct[3] == CAT[0]:
            currentStat = "aman"
        if arrayAct[0] == CAT[1] and arrayAct[1] == CAT[1] and arrayAct[2] == CAT[1] and arrayAct[3] == CAT[0]:
            currentStat = "aman"
        if arrayAct[0] == CAT[1] and arrayAct[1] == CAT[1] and arrayAct[2] == CAT[1] and arrayAct[3] == CAT[1]:
            currentStat = "aman"
            
        if arrayAct[0] == CAT[4] and arrayAct[1] == CAT[4] and arrayAct[2] == CAT[4] and arrayAct[3] == CAT[4]:
            currentStat = "tidak aman"
        if arrayAct[0] == CAT[5] and arrayAct[1] == CAT[4] and arrayAct[2] == CAT[4] and arrayAct[3] == CAT[4]:
            currentStat = "tidak aman"
        if arrayAct[0] == CAT[5] and arrayAct[1] == CAT[5] and arrayAct[2] == CAT[4] and arrayAct[3] == CAT[4]:
            currentStat = "tidak aman"
        if arrayAct[0] == CAT[5] and arrayAct[1] == CAT[5] and arrayAct[2] == CAT[5] and arrayAct[3] == CAT[4]:
            currentStat = "tidak aman"
        if arrayAct[0] == CAT[5] and arrayAct[1] == CAT[5] and arrayAct[2] == CAT[5] and arrayAct[3] == CAT[5]:
            currentStat = "tidak aman"
        if arrayAct[0] == CAT[5] and arrayAct[1] == CAT[5] and arrayAct[2] == CAT[5] and arrayAct[3] == CAT[5]:
            currentStat = "tidak aman"
            
        if currentStat == "tidak aman":
            cond = "active"
        else:
            cond = "passive"

        data = {
            "pushnotif": cond,
            "activity": currentAct,
            "status": currentStat,
            "image": urlImg
        }

        img2 = cv2.resize(img, dsize)

        cv2.imwrite("myAct.jpg", img2)
        storage.child("images/example.jpg").put("myAct.jpg")
        db.update(data)

        cv2.imshow("frame", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.2)

cam.release()
cv2.destroyAllWindows()
