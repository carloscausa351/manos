import cv2
import mediapipe as mp
import numpy as np
import uuid
import os
import time
import datetime

start = time.time()
print("hello")

detectomano = 0
redBajo1 = np.array([0, 40, 20], np.uint8)
redAlto1 = np.array([3, 255, 255], np.uint8)
redBajo2 = np.array([170, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)
verdeAlto = np.array([140, 50, 50], np.uint8)
verdeBajo = np.array([150, 200, 70], np.uint8)
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX
mp_draw.DrawingSpec
# EMPIEZO=time.time()
# print(EMPIEZO)
EMPIEZO = 0.00
referencia = 0

mp_hands.HandLandmark.WRIST


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))
            # print (text)
            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output


import matplotlib

from matplotlib import pyplot as plt

joint_list = [[4, 3, 2], [8, 7, 6], [12, 11, 10], [16, 15, 14], [20, 19, 18]]

joint_list[3]


def draw_finger_angles(image, results, joint_list):
    # Loop through hands
    for hand in results.multi_hand_landmarks:
        # Loop through joint sets
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])  # Second coord
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])  # Third coord

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)

            if angle > 180.0:
                angle = 360 - angle

            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image


# In[13]:


# results.multi_hand_landmarks


# In[ ]:

cap = cv2.VideoCapture(0)

fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

print('fps = ' + str(fps))
print('number of frames = ' + str(frame_count))
print('duration (S) = ' + str(duration))
minutes = int(duration / 60)
seconds = duration % 60
print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.3) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX

        if ret:
            dt = str(datetime.datetime.now())
            frame = cv2.putText(frame, dt,
                                (10, 100),
                                font, 1,
                                (210, 0, 155),
                                4, cv2.LINE_8)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagenHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Flip on horizontal
        # image = cv2.flip(image, 1)
        # frame = cv2.flip(frame, 1)
        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        maskRed1 = cv2.inRange(imagenHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(imagenHSV, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1, maskRed2)
        maskRed2 = cv2.add(maskRed1, maskRed2)
        maskVerde = cv2.add(verdeBajo, verdeAlto)
        area_pts = np.array([[0, 145], [640, 145], [640, 300], [0, 300]])
        area_pts2 = np.array([[31, 145], [600, 145], [600, 290], [31, 290]])
        noimAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
        noimAux = cv2.drawContours(noimAux, [area_pts2], -1, (255), -1)
        area_negra = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
        imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
        imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
        # imAux = cv2.bitwise_not(frame,frame, mask=maskRed)
        area_pts2 = cv2.bitwise_and(frame, frame, mask=imAux)
        area_pts2 = cv2.bitwise_and(frame, frame, mask=maskRed)
        image_area = cv2.bitwise_and(frame, frame, mask=maskRed)
        image2 = cv2.cvtColor(area_negra, cv2.COLOR_RGB2BGR)
        frame2 = cv2.add(frame, area_pts2)
        frame3 = cv2.add(image, image, mask=maskRed)
        # image_area= cv2.bitwise_and(frame,frame, mask=imAux)
        # noimAux = cv2.bitwise_not(imAux,imAux, mask=area_pts2)
        maskRed = cv2.bitwise_and(noimAux, maskRed)
        # frame2=cv2.add(frame,frame, mask=imAux)
        # image= cv2.bitwise_and(image, frame2) #pone el cuadro negro en la mitad

        cnts = cv2.findContours(maskRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # Detections
        # print(results)
        print(detectomano)
        if results.multi_hand_landmarks:
            if detectomano == 0:
                EMPIEZO = time.time()
                detectomano = 1

        # Rendering results
        if results.multi_hand_landmarks:

            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_draw.draw_landmarks(frame2, hand, mp_hands.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec(color=(121, 22, 76), thickness=1, circle_radius=4),
                                       mp_draw.DrawingSpec(color=(250, 44, 250), thickness=1, circle_radius=2),
                                       )
                mp_draw.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec(color=(250, 44, 250), thickness=1, circle_radius=2),
                                       )
                mp_draw.draw_landmarks(frame3, hand, mp_hands.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec(color=(121, 22, 76), thickness=1, circle_radius=4),
                                       mp_draw.DrawingSpec(color=(250, 44, 250), thickness=1, circle_radius=2),
                                       )

                # if get_label(num, hand, results):
                # text, coord = get_label(num, hand, results)
                # print(text)
                # if  text=="Left 1.0":
                ## text="izquierda"
                # else:
                # text="derecha"

                # Render left or right detection
                if get_label(num, hand, results):

                    text, coord = get_label(num, hand, results)
                    if text == "Left 1.0":
                        text = "izquierda"
                    else:
                        text = "derecha"
                    cv2.putText(frame2, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame3, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)

                    cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)

            # Draw angles to image from joint list
            draw_finger_angles(frame2, results, joint_list)
            draw_finger_angles(image, results, joint_list)
            i = 0
            m = 60

            for cnt in cnts:

                if cv2.contourArea(cnt) > 100:
                    # aqui esta el controlador de cantidad

                    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
                    mensaje = str(i + 1)
                    # print(mensaje)
                    cv2.putText(frame2, mensaje, (x, y), font, 0.75, (255, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame2, str(m), (320, 320), font, 1, (255, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(imAux, str(duration), (100, 100), font, 1, (255, 200, 0), 1, cv2.LINE_AA)
                    # print(end-start)
                    # end = time.time()
                    print(m)

                    m = m - 1
                    i = i + 1
                    referencia = time.time()

            cv2.drawContours(frame2, [area_pts], -1, (255, 0, 255), 2)
            # cv2.drawContours(frame,[area_pts],-1,(255,0,255),2)
            # viene del rectangulo [[30,145],[550,145],[550,300],[30,300]])
            cv2.line(frame2, (0, 145), (650, 145), (0, 255, 255), 1)
            # cv2.rectangle(frame2, (image.shape[1]-70, 215), (image.shape[1]-5,270),(0,255,0),2)

            # cv2.rectangle(frame, (image.shape[1]-70, 215), (image.shape[1]-5,270),(0,255,0),2)
        # Save our image
        # cv2.imwrite(os.path.join('Output Images', '{}.jpg'.format(uuid.uuid1())), image)
        else:
            cv2.putText(frame2, 'no detecto', (100, 215), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
            espera = (time.time() - referencia)
            print(espera)
            if espera > 2:
                termino = time.time()
                file = open("C:/Users/Falabella san diego/Downloads/conteo/Eureka.txt", "w")
                file.write(str(espera))
                tiempo = '{:,.2f}'.format(termino - EMPIEZO)
                file.write(str(tiempo))
                file.close()

        frame3 = cv2.resize(frame3, (426, 240))
        frame2 = cv2.resize(frame2, (426, 240))
        image = cv2.resize(image, (426, 240))
        image_area = cv2.resize(image_area, (426, 240))
        frame = cv2.resize(frame, (426, 240))
        termino = time.time()
        tiempo = '{:,.2f}'.format(termino - EMPIEZO)
        # print('El area es: {:,.2f}'.format(area))
        cv2.putText(image, str(tiempo), (30, 30), font, 1, (255, 200, 255), 1, cv2.LINE_AA)
        cv2.putText(frame2, u'tiempo: ' + str(tiempo), (50, 215), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        # imAux=cv2.resize(imAux,(426,240))
        # concat_h1 = cv2.hconcat([image_area,image,frame])
        # concat_h2 = cv2.hconcat([frame2,frame3,imAux])
        # concat_v = cv2.vconcat([concat_h1, concat_h2])
        cv2.imshow('Destreza fina de la mano', image)
        cv2.imshow('maskRed', image_area)
        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)
        # cv2.imshow('mask',maskRed2)
        cv2.imshow('image', image)

        # cv2.imshow('IA CAUSA & EFECTO',concat_v)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# In[ ]:




