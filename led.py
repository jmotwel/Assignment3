from flask import Flask, request
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)#RED
GPIO.setup(23,GPIO.OUT)#GREEN
GPIO.setup(24,GPIO.OUT)#BLUE
freq=1000000;
RED = GPIO.PWM(18,freq)
GREEN = GPIO.PWM(23, freq)
BLUE = GPIO.PWM(24, freq)
RED.start(0)
GREEN.start(0)
BLUE.start(0)

app = Flask(__name__)
@app.route('/')
def index():
    return "Received general request"


@app.route('/LED', methods=['GET'])
def get_led():
    status = request.args.get('status','')
    color = request.args.get('color','')
    intensity = request.args.get('intensity','')

    duty = int(intensity)

    time.sleep(1)
    
    if (status == 'on'):
        print("Turning on ", color, " at intensity ", intensity)
        if (color == 'red'):
            RED.ChangeDutyCycle(duty)
            GREEN.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(0)
        elif (color == 'blue'):
            RED.ChangeDutyCycle(0)
            GREEN.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(duty)
        elif (color == 'green'):
            RED.ChangeDutyCycle(0)
            GREEN.ChangeDutyCycle(duty)
            BLUE.ChangeDutyCycle(0)
        elif (color == 'magenta'):
            RED.ChangeDutyCycle(duty)
            GREEN.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(duty)
        elif (color == 'cyan'):
            RED.ChangeDutyCycle(0)
            GREEN.ChangeDutyCycle(duty)
            BLUE.ChangeDutyCycle(duty)
        elif (color == 'yellow'):
            RED.ChangeDutyCycle(duty)
            GREEN.ChangeDutyCycle(duty)
            BLUE.ChangeDutyCycle(0)
        elif (color == 'white'):
            RED.ChangeDutyCycle(duty)
            GREEN.ChangeDutyCycle(duty)
            BLUE.ChangeDutyCycle(duty)        
    elif (status == 'off'):
        RED.ChangeDutyCycle(0)
        GREEN.ChangeDutyCycle(0)
        BLUE.ChangeDutyCycle(0) 
        print("Turning off LED")
    else:
        print("Unknown status command")

    time.sleep(1)
    
    toReturn = "Turning " + str(status) + str(color) + " LED at intensity " + str(intensity)
    
    return toReturn


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
