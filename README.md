# Real Time Facial Tracking Security Camera

A realtime facial tracking security camera that integrates computer vision, embedded system, and stepper motor control into a front to back system.

The project uses OpenCV running on a Raspberry Pi to detect human faces in a live camera feed and dynamically control a stepper motor driven camera mount via an Arduino based motor control subsystem.


## Overview

The system is split into two primary components:

1. **Vision & Decision Layer (Raspberry Pi)**
   - Processes live video using OpenCV
   - Detects faces using a Haar cascade classifier
   - Computes positional offset of detected faces
   - Sends directional commands over serial communication

2. **Motion Control Layer (Arduino Nano)**
   - Receives commands via UART
   - Generates step and direction signals
   - Controls a TMC2209 stepper motor driver
   - Actuates a NEMA 17 stepper motor for camera panning

Separating vision processing from real time motor control improves responsiveness and system stability.



## System Architecture / Requirements 

* **Raspberry pi 4 with at least 8gb of ram**
* **Arduino Nano or equivalent MCU**
* **TMC2209 Motor driver**
* **NEMA 17 stepper motor**
* **5-12v DC power cable & Barrel Jack connector**
* **Protoboard(s) and 22awg wires**

## Installation & Assembly 

Assembly is relatively straightforward provided the Raspberry Pi has an OS installed capable of running a python script. 
Limitations are you must locate the exact external USB webcam you are using in the kernel. Typically, you can do so by running these following command on linux/debian: 
    - ls /dev/video*

Once you see them listed, usually it may be either /dev/video0 or /dev/video1, the index corresponds to the number in the "cap = cv2.VideoCapture(#)" portion of the python script, this is where you'd change the # with your webcam device. 

The next issue, is once you have flashed your MCU (for example an arduino nano) with the .ino script on your respective IDE, you need to connect it to the pi via one of the USB 3.0 ports capable of sending/recieving data. Once you do this, you must run one of these, as they correspond to common Arduino devices: 
    - ls /dev/ttyUSB* 
    - ls /dev/ttyACM* 

This will give you a list of external devices, you must locate the one that corresponds to your device. 
If you are not sure which corresponds to which, you can do the following: 
    - sudo apt install v4l-utils
    - v4l2-ctl --list-devices
You may get something like this: 

    USB Camera (046d:0825):
         /dev/video1

    Integrated Webcam:
        /dev/video0

And from there, it is simply a matter of wiring it all together. 
You are free to change the pins that map to the EN/STEP/DIR for the stepper as you see fit, and make note of whatever you choose to wire the TMC2209 to on the MCU as well, as they all must handeled carefully assuming you aim to solder it together. Otherwise it is fairly trivial to do with a breadboard. 
Be sure to connect the ground from the arduino to the TMC2209, and connect the 5v from the MCU to the VI0 of the TMC for logic. Additionally, you must separate power, the arduino is powered via USB from the Pi where it also receives Serial commands, and the TMC motor driver needs a stable external DC power supply rated up to whatever amperage matches your specific stepper motor. 




## License

This project is licensed under the MIT License. 
