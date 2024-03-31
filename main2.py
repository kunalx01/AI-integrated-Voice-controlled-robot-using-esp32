import speech_recognition as sr
import cv2
from threading import Thread
import time
import google.generativeai as genai
import PIL.Image
import pyttsx3
import socket

esp32_ip = "192.168.0.100"
esp32_port = 8002 

esp32_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
esp32_socket.connect((esp32_ip, esp32_port))


global text
text = '' 
global command 
command = ''
l1 = ["forward", "backward", "right direction", "left direction" , "stop"]
a = None

cap = cv2.VideoCapture(0)

def send_command(command):
    esp32_socket.sendall((command + "\n").encode())


# Set up Google GenerativeAI
genai.configure(api_key="AIzaSyCc2CdfNLqxXOPl2Y_2imi09TBOaPnavpc")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]


model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


model2 = genai.GenerativeModel(model_name="gemini-1.0-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def save_frame(frame):
    # Save the captured frame as an image file
    file_name = "frame.jpg"
    cv2.imwrite(file_name, frame)
    print(f"Frame saved as {file_name}")
    return file_name

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Get list of available voices
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)  # Change the index as needed
    engine.setProperty('rate', 140)

    # Convert text to speech
    engine.say(text) 

    # Wait for the speech to finish
    engine.runAndWait()

def cam():
    global text
    while True:
        ret ,frame = cap.read()
        cv2.imshow('window',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()    
    
def sound():
    global text
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source :
            print("Listening...")
            audio = r.listen(source)
            time.sleep(2)
            try:
                
                text = r.recognize(audio)
                print("You Said : {}".format(text))
                
                if 'stop listening' in text or 'off the device' in text:
                    text_to_speech("Switching off")
                    break
                
                
                elif  'hello' in text or 'how' in text:                 
                    text_to_speech("i am fine how can i help you ?")
                       
                elif text == "I have a question":
                    text_to_speech("How may I help you?")
                    print("Listening...")
                    audio = r.listen(source)
                    time.sleep(2)
                    text2 = r.recognize(audio)
                    print("You Said : {}".format(text2))
                    convo = model2.start_chat(history=[])
                    convo.send_message("summarize in 40 words {}".format(text2))
                    generate = convo.last.text
                    print(generate)
                    text_to_speech(generate)
            
                elif text == "what is this" :
                    ret ,frame = cap.read()                  
                    image_file = save_frame(frame)
                    image = PIL.Image.open(image_file)
                    prompt = ("Describe image: \n", image)
                    response = model.generate_content(prompt)
                    print(response.text)
                    text_to_speech(response.text)
                    
                elif any(word in text for word in l1):
                    text3 = " ".join(word for word in l1 if word in text)
                    
                    if text3== 'forward':  
                         send_command("RUN_FORWARD")
                         text_to_speech("Going Forward")
                    elif text3 == 'backward':
                         send_command("RUN_BACKWARD")
                         text_to_speech("going backward")
                    elif text3 == 'right direction': 
                         send_command("RIGHT")
                         text_to_speech("turning right")
                    elif text3 == 'left direction':
                         send_command("LEFT")
                         text_to_speech("turning left")
                    elif text3 == 'stop': 
                         send_command("STOP") 
                         text_to_speech("bot is stopped")
                    
                    
          # Reset text after processing
                    time.sleep(0.5)
                           
            except LookupError:
                text_to_speech("Unable to listen, say something")
                  
                        
if __name__ == '__main__':
    Thread(target = cam).start()
    Thread(target = sound).start()