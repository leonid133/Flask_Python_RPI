from RPIO import PWM 
import time
import atexit
from flask import Flask, render_template, request
app = Flask(__name__)

def angleMap(angle):
	return int((round((1950.0/180.0),0)*angle) +550)

pins = {
    23 : {'name' : 'roll', 'angle' : 90},
    22 : {'name' : 'pitch', 'angle' : 90},
    21 : {'name' : 'yaw', 'angle' : 90}
    }

servoRoll = PWM.Servo()
servoPitch = PWM.Servo()
servoYaw = PWM.Servo()

servoRoll.set_servo(23, angleMap(90))
servoPitch.set_servo(22, angleMap(90))
servoYaw.set_servo(21, angleMap(90))

def cleanup():
    servo.stop_servo(23)
    servo.stop_servo(22)
    servo.stop_servo(21)

@app.route("/")
def main():

    templateData = {
        'title' : 'PiCam'
        }
    return render_template('picam.html', **templateData)

@app.route("/<direction>", methods=['GET', 'POST'])
def move(direction):
    if direction == 'left':
        na = pins[23]['angle'] + 10
        if int(na) <= 180:
            servorRoll.set_servo(23, angleMap(na))
            pins[23]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'right':
        na = pins[23]['angle'] - 10
        if na >= 0:
            servoRoll.set_servo(23, angleMap(na))
            pins[23]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'up':
        na = pins[22]['angle'] + 10
        if na <= 180:
            servoPitch.set_servo(22, angleMap(na))
            pins[22]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'down':
        na = pins[22]['angle'] - 10
        if na >= 0:
            servoPitch.set_servo(22, angleMap(na))
            pins[22]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'spin':
        na = pins[21]['angle'] + 10
        if na <= 180:
            servoYaw.set_servo(22, angleMap(na))
            pins[21]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'counterspin':
        na = pins[21]['angle'] - 10
        if na >= 0:
            servoYaw.set_servo(21, angleMap(na))
            pins[21]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    return str(direction)

@app.route("/<motor>/<pulsewidth>", methods=['GET', 'POST'])
def manual(motor,pulsewidth):
    if motor == "roll":
        servoRoll.set_servo(23, int(pulsewidth))
    elif motor == "pitch":
        servoPitch.set_servo(22, int(pulsewidth))
    elif motor == "yaw":
        servoYaw.set_servo(21, int(pulsewidth))
    return "Moved"

# Clean everything up when the app exits
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


