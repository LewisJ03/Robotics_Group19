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
        self.turnSpeed = 5
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
        newHeading = round(curHeading - 90)
        if newHeading<0:
            newHeading+=360 

        self.motorFrontLeft.spin(REVERSE)
        self.motorBackLeft.spin(REVERSE)
        self.motorFrontRight.spin(REVERSE)
        self.motorBackRight.spin(REVERSE)
            
    def turnRight(self):
        curHeading = self.inertial.heading()
        newHeading = round(curHeading + 90)
        if newHeading<360:
            newHeading-=360 
        
        self.motorFrontLeft.spin(FORWARD)
        self.motorBackLeft.spin(FORWARD)
        self.motorFrontRight.spin(FORWARD)
        self.motorBackRight.spin(FORWARD)

def followPath(bot,trackingArr,coordX,coordY):
    while True:
        brightness = bot.optical.brightness() * 100 # Convert to percentage
        detectedDistance = bot.distance.object_distance(MM)
        curHeading=bot.brain.inertial.heading()
        if curHeading<45:
            trackingArr.append(["-","-"])#adds y dimension to array
        elif curHeading>45:
            for i in range(len(trackingArr)):
                trackingArr[(len(trackingArr))-i].append("-")#adds x dimension to array

        if (detectedDistance > 280 or detectedDistance < 240):#stops bot if object in way or edge
            bot.stop()
            bot.moveBackward()
            time.sleep(1)
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()

            bot.brain.screen.print("Obstacle detected!")
            bot.brain.screen.next_row()
            time.sleep(1)
            trackingArr[coordX][coordY]="!"
            continue
        
        elif (curHeading>315 or curHeading < 45) and trackingArr[coordX][coordY+1]=="!":#tracks for already taken
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()
        elif (curHeading>45 and curHeading < 135) and trackingArr[coordX+1][coordY]=="!":
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()
        elif (curHeading>135 and curHeading < 225) and trackingArr[coordX][coordY-1]=="!":
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()
        elif (curHeading>225 or curHeading < 315) and trackingArr[coordX-1][coordY]=="!":
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()

        else:
            bot.moveForward()
            trackingArr[coordX][coordY]="!"

            if curHeading>315 or curHeading < 45:#sets x&y for next movement
                coordY+=1
            elif curHeading>45 and curHeading < 135:
                coordX+=1
            elif curHeading>135 and curHeading < 225:
                coordY-=1
            elif curHeading>225 and curHeading < 315:
                coordX-=1
        time.sleep(0.1)
        


    

def main():
    bot = Bot()

    x ,y =2,2
    trackArr=[['-'for i in range(x)]for j in range(y)]#initalise array for tracking
    coordX=0
    coordY=0

    while True:
        curHeading = bot.optical.hue()
        bot.brain.screen.print(curHeading)
        bot.brain.screen.next_row()
        #if curDistance < 1000:
            #moveForward(motorLeft, motorRight)
        followPath(bot,trackArr,coordX,coordY)

main()