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
import time

class Bot:
    def __init__ (self):
        self.brain = Brain()
        self.inertial = Inertial()
        self.optical = Optical(Ports.PORT7)
        self.distance = Distance(Ports.PORT5)
        self.motorFrontLeft = Motor(Ports.PORT6) # From bot's perspective
        self.motorBackLeft = Motor(Ports.PORT8)
        self.motorFrontRight = Motor(Ports.PORT10)
        self.motorBackRight = Motor(Ports.PORT9)
    
        self.baseSpeed = 30
        self.turnSpeed = 15
        self.tapeBrightnessThreshold = 30 # will needing adjusting based on testing

        self.inertial.calibrate()
        self.optical.set_light(100)

    def moveForward(self):
        self.motorFrontLeft.spin(FORWARD)
        self.motorBackLeft.spin(FORWARD)
        self.motorFrontRight.spin(REVERSE)
        self.motorBackRight.spin(REVERSE)

    def moveBackward(self):
        self.motorFrontLeft.spin(REVERSE)
        self.motorBackLeft.spin(REVERSE)
        self.motorFrontRight.spin(FORWARD)
        self.motorBackRight.spin(FORWARD)

    def stop(self):
        self.motorFrontLeft.stop()
        self.motorBackLeft.stop()
        self.motorFrontRight.stop()
        self.motorBackRight.stop()

    def turnLeft(self):
        curHeading = self.inertial.heading()
        newHeading = curHeading + 90

        while curHeading != newHeading:
            curHeading = self.inertial.heading()
            self.motorFrontLeft.spin(REVERSE)
            self.motorBackLeft.spin(REVERSE)
            self.motorFrontRight.spin(REVERSE)
            self.motorBackRight.spin(REVERSE)

    def turnRight(self):
        self.motorFrontLeft.spin(FORWARD)
        self.motorBackLeft.spin(FORWARD)
        self.motorFrontRight.spin(FORWARD)
        self.motorBackRight.spin(FORWARD)

def followPath(bot):
    while True:
        brightness = bot.optical.brightness() * 100 # Convert to percentage
        detectedDistance = bot.distance.object_distance(MM)

        if (detectedDistance > 280 or detectedDistance < 240):
            bot.stop()
            bot.moveBackward()
            time.sleep(1)
            bot.stop()
            time.sleep(0.5)
            bot.turnLeft()
            bot.brain.screen.print("Obstacle detected!")
            bot.brain.screen.next_row()
            time.sleep(1)
            continue
        else:
            bot.moveForward()

        time.sleep(0.1)

def main():
    bot = Bot()

    while True:
        curHeading = bot.optical.hue()
        bot.brain.screen.print(curHeading)
        bot.brain.screen.next_row()
        #if curDistance < 1000:
            #moveForward(motorLeft, motorRight)
        followPath(bot)

main()