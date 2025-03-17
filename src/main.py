# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Lewis                                                        #
# 	Created:      3/17/2025, 4:44:36 PM                                        #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default

def moveForward(motorLeft, motorRight):
    motorLeft.spin(FORWARD)
    motorRight.spin(REVERSE)

def stopForward(motorLeft, motorRight):
    motorLeft.stop()
    motorRight.stop()

def moveBackward(motorLeft, motorRight):
    motorLeft.spin(REVERSE)
    motorRight.spin(FORWARD)

def stopBackward(motorLeft, motorRight):
    motorLeft.stop()
    motorRight.stop()

def turnLeft(motorLeft, motorRight, inertial):
    curHeading = inertial.heading()
    newHeading = curHeading + 90

    while curHeading != newHeading:
        curHeading = inertial.heading()
        motorLeft.spin(REVERSE)
        motorRight.spin(REVERSE)

def turnRight(motorLeft, motorRight, inertial):
    motorLeft.spin(FORWARD)
    motorRight.spin(FORWARD)

def main():
    brain=Brain()
    inertial = Inertial()
    optical = Optical(Ports.PORT6)
    distance = Distance(Ports.PORT3)
    motorLeft = Motor(Ports.PORT1) # From bot perspective
    motorRight = Motor(Ports.PORT2) # From bot perspective
    
    inertial.calibrate()

    while True:
        curHeading = inertial.heading()
        brain.screen.print(curHeading)
        brain.screen.next_row()
        #if curDistance < 1000:
            #moveForward(motorLeft, motorRight)
        turnLeft(motorLeft, motorRight, inertial)

main()