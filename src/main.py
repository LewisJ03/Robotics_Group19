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
        self.turnSpeed = 10

        self.inertial.calibrate()
        self.optical.set_light(100)

    def moveForward(self):
        self.motorFrontLeft.spin(FORWARD, self.baseSpeed)
        self.motorBackLeft.spin(FORWARD, self.baseSpeed)
        self.motorFrontRight.spin(REVERSE, self.baseSpeed)
        self.motorBackRight.spin(REVERSE, self.baseSpeed)

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
        self.motorFrontLeft.spin(REVERSE, self.turnSpeed)
        self.motorBackLeft.spin(REVERSE, self.turnSpeed)
        self.motorFrontRight.spin(REVERSE, self.turnSpeed)
        self.motorBackRight.spin(REVERSE, self.turnSpeed)

        time.sleep(4.50)

        self.stop()
            
    def turnRight(self):
        self.motorFrontLeft.spin(FORWARD, self.turnSpeed)
        self.motorBackLeft.spin(FORWARD, self.turnSpeed)
        self.motorFrontRight.spin(FORWARD, self.turnSpeed)
        self.motorBackRight.spin(FORWARD, self.turnSpeed)

        time.sleep(4.50)

        self.stop()

def followPath(bot,direction):
    while True:#main loop
        detectedDistance = bot.distance.object_distance(MM)

        if (detectedDistance < 240):#stops bot if object in way
            
            bot.brain.screen.print("Obstacle detected, attempting to avoid.")
            bot.brain.screen.next_row()

            bot.stop()
            time.sleep(0.5)
            bot.moveBackward()
            time.sleep(0.5)
            if direction==1:#switch for left right turn
                avoidLeft(bot,detectedDistance)
            elif direction==0:
                avoidRight(bot,detectedDistance)

        if (detectedDistance>350):#over edge stop
            bot.brain.screen.print("Edge detected, attempting to avoid.")
            bot.brain.screen.next_row()

            bot.stop()
            if direction==0:#switch for left right turn
                avoidEdgeRight(bot,detectedDistance)
                direction=1
            elif direction==1:
                avoidEdgeLeft(bot,detectedDistance)
                direction=0
            time.sleep(0.2)

        else:
            bot.moveForward()
        time.sleep(0.1)#waits 0.1 seconds before looping

def avoidEdgeLeft(bot,detectedDistance):
    bot.turnLeft()
    bot.stop()
    if (detectedDistance>350 or detectedDistance < 240):# distances allow for sensor to mess up distance and not crash program
        bot.moveForward()
        time.sleep(2)#length of robot
        bot.stop()
        bot.turnLeft()
    else:
        bot.turnRight()#code for abort move
        

def avoidEdgeRight(bot,detectedDistance):
    bot.turnRight()
    bot.stop()
    if (detectedDistance>350 or detectedDistance < 240):        
        bot.moveForward()
        time.sleep(2)
        bot.stop()
        bot.turnRight()

    else:    
        bot.turnLeft()#code for abort move

        
def avoidLeft(bot,detectedDistance):
        #step1
        bot.turnRight()
        bot.stop()
        bot.moveForward()#does not need to check for edge as alrady been at this point 
        time.sleep(2)
        bot.stop()

        #step2
        bot.turnLeft()
        bot.stop()
        if (detectedDistance>350):#revserse code
            avoidLeftRev(bot)
        else:
            bot.moveForward()#need check here as can drive further than alrady covered track
            time.sleep(5)
            bot.stop()

        #step3
        bot.turnLeft()
        bot.stop()
        if (detectedDistance>350):
            bot.turnRight()
            bot.stop
            bot.moveForward()
            time.sleep(5)#time needed to pass object with current angle of eye
            bot.stop()
            avoidLeftRev(bot)
        else:
            bot.moveForward()#need check here as unknown area
            time.sleep(2)
            bot.stop()
            bot.turnRight()
            bot.stop()

def avoidLeftRev(bot):#code for if an avoid needs to be aborted
    bot.turnRight()
    bot.stop()
    bot.moveForward() 
    time.sleep(2)
    bot.stop()
    bot.turnLeft()
    bot.stop()
    for i in range(2):
        bot.turnLeft()
        bot.stop()

    

def avoidRight(bot,detectedDistance):#avoid object on the right
    #step1
    bot.turnLeft()
    bot.stop()
    bot.moveForward()
    time.sleep(2)
    bot.stop()
    
    #step2
    bot.turnRight()
    bot.stop()
    if (detectedDistance>350):
        avoidRightRev(bot)
    else:
        bot.moveForward()
        time.sleep(5)
        bot.stop()

        #step3
        bot.turnRight()
        bot.stop()
        if (detectedDistance>350):
            bot.turnLeft()
            bot.stop
            bot.moveForward()
            time.sleep(5)
            bot.stop()
            avoidRightRev(bot)
        else:
            bot.moveForward()
            time.sleep(2)
            bot.stop()
            bot.turnLeft()
            bot.stop()

def avoidRightRev(bot):#code for if an avoid needs to be aborted
    bot.turnRight()
    bot.stop()
    bot.moveForward() 
    time.sleep(2)
    bot.stop()
    bot.turnLeft()
    bot.stop()
    for i in range(2):
        bot.turnRight()
        bot.stop()

def main():
    bot = Bot()
    direction=1
    while True:
        followPath(bot,direction)

main()