from inputs import get_gamepad
from adafruit_motorkit import MotorKit
import pigpio

pi = pigpio.pi() #Initialize pigpio

kit = MotorKit() #adafruit library for dc motor bonnet
controller_input = {'ABS_RZ': 0, 'BTN_NORTH': 0, 'BTN_SOUTH': 0, 'ABS_Z': 0, 'BTN_WEST': 0, 'ABS_HAT0X': 0, 'ABS_HAT0Y': 0}

panPin = 18
tiltPin = 13
pi.set_servo_pulsewidth(panPin, 1500)
pi.set_servo_pulsewidth(tiltPin, 1500)

panDuty = 1500
tiltDuty = 1500

def gamepad_update():
    # Code execution stops at the following line until gamepad event occurs.
    events = get_gamepad()
    return_code = 'No Match'
    for event in events:
        event_test = controller_input.get(event.code, 'No Match')
        if event_test != 'No Match':
            controller_input[event.code] = event.state
            return_code = event.code
        else:
            return_code = 'No Match'
 
    return return_code

def forward():
    if controller_input['BTN_SOUTH'] == 1:
        #print("forward")
        kit.motor1.throttle = -1
        kit.motor2.throttle = 1
        kit.motor3.throttle = -1
        kit.motor4.throttle = 1
    elif controller_input['BTN_SOUTH'] == 0:
        #print("stop")
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0

def backward():
    if controller_input['BTN_NORTH'] == 1:
        #print("backward")
        kit.motor1.throttle = 1
        kit.motor2.throttle = -1
        kit.motor3.throttle = 1
        kit.motor4.throttle = -1
    elif controller_input['BTN_NORTH'] == 0:
        #print("stop")
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0

def right():
    if controller_input['ABS_RZ'] == 255:
        #print("right")
        kit.motor1.throttle = -1
        kit.motor2.throttle = -1
        kit.motor3.throttle = -1
        kit.motor4.throttle = -1
    elif controller_input['ABS_RZ'] == 0:
        #print("stop")
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0

def left():
    if controller_input['ABS_Z'] == 255:
        #print("left")
        kit.motor1.throttle = 1
        kit.motor2.throttle = 1
        kit.motor3.throttle = 1
        kit.motor4.throttle = 1
    elif controller_input['ABS_Z'] == 0:
        #print("stop")
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0
        
def panMove(a):
    
    if controller_input['ABS_HAT0X'] == 1:
        if a < 2500:
            a += 100
            pi.set_servo_pulsewidth(panPin, a)
    elif controller_input['ABS_HAT0X'] == -1:
        if a > 500:
            a -= 100
            pi.set_servo_pulsewidth(panPin, a)
    return (a)
        
def tiltMove(b):
    if controller_input['ABS_HAT0Y'] == 1:
        if b < 2500:
            b += 100
            pi.set_servo_pulsewidth(tiltPin, b)
    elif controller_input['ABS_HAT0Y'] == -1:
        if b > 500:
            b -= 100
            pi.set_servo_pulsewidth(tiltPin, b)
    return (b)
    
def main():
    """ Main entry point of the app """

#led.on()
try:
    while 1:
        # Get next controller Input
        control_code = gamepad_update()        
        # Gamepad button filter
        if control_code == 'BTN_SOUTH':
            forward()
        elif control_code == 'BTN_NORTH':
            backward()
        elif control_code == 'ABS_RZ':
            right()
        elif control_code == 'ABS_Z':
            left()
        elif control_code == 'ABS_HAT0X':
            panDuty = panMove(panDuty)
        elif control_code == 'ABS_HAT0Y':
            tiltDuty = tiltMove(tiltDuty)

except KeyboardInterrupt:
  pi.set_servo_pulsewidth(tiltPin, 0)
  pi.set_servo_pulsewidth(panPin, 0)
  pi.stop()


 
#-----------------------------------------------------------
 
if __name__ == "__main__":
#     """ This is executed when run from the command line """
     main()
