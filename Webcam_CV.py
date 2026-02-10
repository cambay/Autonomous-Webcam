import serial 
import cv2
import time


#pyserial setup
arduino = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=0.3) #/dev/ttyUSB1 refers to the arduino nano clone that was used

#Import the classifier 
face_cascade = cv2.CascadeClassifier("/home/admin/Downloads/haarcascade_frontalface_default.xml") #This version is for the raspberry pi's path 

cap = cv2.VideoCapture(0) #attach to the webcam 

prev = time.time()
face_color = (0,0,255) #default color placed outside of the main loop 
    
if not cap.isOpened():
    print("Error")
    exit()

while 1: 
    ret, frame = cap.read() 

    if not ret:
        print("Error")
        continue
    

    #Haar Cascade Detection 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))


    #Center rectangle visual representation and aesthetics 
    top_left     = (160, 120) 
    bottom_right = (480, 360)
    center_divider = cv2.rectangle(frame, top_left, bottom_right, (19,190,216), 2) #Bounding box
    cv2.circle(frame, (320,240), 3, (0,0,0), 2)
    
    #FPS display 
    now = time.time()
    fps = (1 / (now - prev))
    prev = now
    cv2.putText(frame, f"Fps:{int(fps)}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (19,190,216), 2)
    
    for (x,y,w,h) in faces:
        face = cv2.rectangle(frame, (x,y), (x+w, y+h), face_color, 2)        
        
        #Get dynamic coordinates of the classified faces from the Haar Cascade, and map 
        #logic intentionally tracks the first detected face (faces[0]) 
        x_left = faces[0][0]
        y_top = faces[0][1]
        face_width = faces[0][2]
        face_height = faces[0][3]
        x_right = x_left + face_width 
        y_bottom = y_top + face_height
        
        #dynamically change the position of the text once the face is centered 
        coordinates = (x_right, y_top) 
        
        #Handle the logic to determine if a detected face is outside of the bounds to align 
        if x_left < 160: 
            print("Move right")
            moveLeft = 'R'
            arduino.write(bytes(moveLeft, 'utf-8'))
            face_color = (0,0,255)
        elif x_right > 480:
            print("Move left")
            moveRight = 'L'
            arduino.write(bytes(moveRight, 'utf-8'))
            face_color = (0,0,255)
        else:
            print("In center")
            #If face is centered, change frame color & add text
            face_color = (0,255,0) 
            cv2.putText(frame, "Locked", coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2) 
             


    #break if 'q' is clicked
    cv2.imshow('Face detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
