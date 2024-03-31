Voice-Controlled ESP32 Robot
This project features a voice-controlled robot powered by an ESP32 microcontroller. The robot is equipped with two motors, allowing it to move forward, backward, turn left, and turn right. Additionally, the robot can be stopped using voice commands.

Requirements
Arduino IDE
ESP32 board
WiFi network
Installation
Clone this repository to your local machine.
Open the Arduino IDE.
Install the required libraries (WiFi.h).
Connect your ESP32 board to your computer.
Upload the code to your ESP32 board.
Usage
Connect the ESP32 board to a power source.
Ensure that the ESP32 is connected to your WiFi network.
Use a terminal or serial monitor to view the IP address of the ESP32.
Connect to the ESP32's IP address using a client (e.g., smartphone or computer) over the same WiFi network.
Send commands to control the robot using the following format:
"STOP": Stop the robot.
"RUN_FORWARD": Move the robot forward.
"RUN_BACKWARD": Move the robot backward.
"RIGHT": Turn the robot right.
"LEFT": Turn the robot left.
