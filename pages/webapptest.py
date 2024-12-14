import cv2 
import mediapipe as mp 
import os
import time 
import numpy as np
import streamlit as st

# Set webcam của máy
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set chiều dài màn hình 
cap.set(4, 720)  # Set chiều rộng màn hình
cap.set(10, 150)  # Set độ sáng

st.title("Test web painter")

frame_holder = st.image([])
stop_button =st.button("Stop")

# Sử dụng Mediapipe để track khung skeleton
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

pasttime = 0

# Define the folder where the color images are stored
folder = 'colors'
mylist = os.listdir(folder)
overlist = []
col = [0, 0, 255]  # Default color (red)

# Load images from the folder and append them to the list
for i in mylist:
    image = cv2.imread(f'{folder}/{i}')
    print(image.shape)
    overlist.append(image)

# Set the initial header image from the first image in the list
header = overlist[0]

print(mylist)
xp, yp = 0, 0

# Create a blank canvas to draw on
canvas = np.zeros((720, 1280, 3), np.uint8)

while cap.isOpened() and not stop_button:
    # Read a frame from the webcam and flip it horizontally
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    if not ret:
        st.write("Video Capture stopped")
        break

    # Convert the frame to RGB color space for hand tracking
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hand landmarks
    results = hands.process(img)
    lanmark = []

    if results.multi_hand_landmarks:
        for hn in results.multi_hand_landmarks:
            for id, lm in enumerate(hn.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lanmark.append([id, cx, cy])
            mpdraw.draw_landmarks(frame, hn, mpHands.HAND_CONNECTIONS)
    
    if len(lanmark) != 0:
        # Check if the hand is in "selection mode" or "drawing mode"
        x1, y1 = lanmark[8][1], lanmark[8][2]
        x2, y2 = lanmark[12][1], lanmark[12][2]

        if lanmark[8][2] < lanmark[6][2] and lanmark[12][2] < lanmark[10][2]:
            xp, yp = 0, 0
            print('Selection mode')

            # Detect the color chosen by the hand position
            if y1 < 100:
                if 0 < x1 < 71:
                    header = overlist[1]
                    col = (0, 0, 0)
                if 71 < x1 < 142:
                    header = overlist[2]
                    col = (0,165,255)
                if 142 < x1 < 213:
                    header = overlist[3]
                    col = (226, 43, 138)
                if 213 < x1 < 284:
                    header =overlist[4]
                    col = (255, 255, 255)
                if 284 < x1 < 355:
                    header =overlist[5]
                    col = (0, 128, 0)
                if 355 < x1 < 426:
                    header =overlist[6]
                    col = (0, 255, 255)
                if 426 < x1 < 497:
                    header =overlist[7]
                    col = (255, 128, 0)
                if 497 < x1 < 568:
                    header =overlist[8]
                    col = (0, 0, 255)     
            # Draw a rectangle representing the selected color
            cv2.rectangle(frame, (x1, y1), (x2, y2), col, cv2.FILLED)

        elif lanmark[8][2] < lanmark[6][2]:
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Draw lines on the canvas when in "drawing mode"
            if col == (0, 0, 0):
                cv2.line(frame, (xp, yp), (x1, y1), col, 100, cv2.FILLED)
                cv2.line(canvas, (xp, yp), (x1, y1), col, 100, cv2.FILLED)
            cv2.line(frame, (xp, yp), (x1, y1), col, 25, cv2.FILLED)
            cv2.line(canvas, (xp, yp), (x1, y1), col, 25, cv2.FILLED)
            print('Drawing mode')
            xp, yp = x1, y1

    # Prepare the canvas for blending with the frame
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Use bitwise operations to blend the frame with the canvas
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, canvas)

    # Add the header (color selection) at the top of the frame
    frame[0:100, 0:640] = header

    # Calculate and display the frames per second (FPS) on the frame
    ctime = time.time()
    fps = 1 / (ctime - pasttime)
    pasttime = ctime
    cv2.putText(frame, f'FPS: {int(fps)}', (1150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    # Show the webcam frame and the canvas
    frame_holder.image(frame, channels="BGR")
    cv2.imshow('canvas', canvas)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q') or stop_button:
        break

cap.release()
cv2.destroyAllWindows()