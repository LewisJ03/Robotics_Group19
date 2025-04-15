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

        self.inertial.calibrate()
        self.optical.set_light(100)

        x , y = 2, 2
        self.trackArr=[['-'for i in range(x)]for j in range(y)]#initalise array for tracking
        self.coordX=0
        self.coordY=0

    def moveForward(self):
        self.motorFrontLeft.spin(FORWARD, self.baseSpeed)
        self.motorBackLeft.spin(FORWARD, self.baseSpeed)
        self.motorFrontRight.spin(REVERSE, self.baseSpeed)
        self.motorBackRight.spin(REVERSE, self.baseSpeed)

    def moveBackward(self):
        self.motorFrontLeft.spin(REVERSE, self.baseSpeed)
        self.motorBackLeft.spin(REVERSE, self.baseSpeed)
        self.motorFrontRight.spin(FORWARD, self.baseSpeed)
        self.motorBackRight.spin(FORWARD, self.baseSpeed)

    def stop(self):
        self.motorFrontLeft.stop()
        self.motorBackLeft.stop()
        self.motorFrontRight.stop()
        self.motorBackRight.stop()

    def turnLeft(self):
        targetHeading = (self.inertial.heading() - 90) % 360

        self.motorFrontLeft.spin(REVERSE, self.turnSpeed)
        self.motorBackLeft.spin(REVERSE, self.turnSpeed)
        self.motorFrontRight.spin(REVERSE, self.turnSpeed)
        self.motorBackRight.spin(REVERSE, self.turnSpeed)

        while abs(self.inertial.heading() - targetHeading) > 5:
            time.sleep(0.01)

        self.stop()
            
    def turnRight(self):
        targetHeading = (self.inertial.heading() + 90) % 360
        
        self.motorFrontLeft.spin(FORWARD, self.turnSpeed)
        self.motorBackLeft.spin(FORWARD, self.turnSpeed)
        self.motorFrontRight.spin(FORWARD, self.turnSpeed)
        self.motorBackRight.spin(FORWARD, self.turnSpeed)

        while abs(self.inertial.heading() - targetHeading) > 5:
            time.sleep(0.01)

        self.stop()

def followPath(bot):
    while True:
        detectedDistance = bot.distance.object_distance(MM)
        curHeading=bot.inertial.heading()
        if curHeading<45:
            bot.trackArr.append(["-","-"])#adds y dimension to array
        elif curHeading>45:
            for i in range(len(bot.trackArr)):
                bot.trackArr[(len(bot.trackArr))-i].append("-")#adds x dimension to array

        if (detectedDistance > 280 or detectedDistance < 240):#stops bot if object in way or edge
            x, y = bot.coordX, bot.coordY
            bot.trackArr[x][y] = "!"

            bot.brain.screen.print("Obstacle detected, attempting to avoid.")
            bot.brain.screen.next_row()

            if not avoidObstacle(bot):
                bot.brain.screen.print("Unable to avoid obstacle.")
                return
            continue
        
        elif (curHeading >= 315 or curHeading < 45) and bot.trackArr[bot.coordX][bot.coordY+1]=="!":#tracks for already taken
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()
        elif (curHeading >= 45 and curHeading < 135) and bot.trackArr[bot.coordX+1][bot.coordY]=="!":
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()
        elif (curHeading >= 135 and curHeading < 225) and bot.trackArr[bot.coordX][bot.coordY-1]=="!":
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()
        elif (curHeading >= 225 or curHeading < 315) and bot.trackArr[bot.coordX-1][bot.coordY]=="!":
            bot.stop()
            time.sleep(0.5)
            bot.turnRight()

        else:
            bot.moveForward()
            bot.trackArr[bot.coordX][bot.coordY]="!"

            if curHeading >= 315 or curHeading < 45:#sets x&y for next movement
                bot.coordY+=1
            elif curHeading >= 45 and curHeading < 135:
                bot.coordX+=1
            elif curHeading >= 135 and curHeading < 225:
                bot.coordY-=1
            elif curHeading >= 225 and curHeading < 315:
                bot.coordX-=1
        time.sleep(0.1)

def avoidObstacle(bot):
    # Move back from object
    bot.stop()
    bot.moveBackward()
    time.sleep(0.5)
    bot.stop()
    time.sleep(0.2)

    # Try 4 directions, left, right, behind and original heading
    for i in range(4):
        bot.turnRight()
        time.sleep(0.2)

        curHeading = bot.inertial.heading()
        x, y = bot.coordX, bot.coordY

        if curHeading >= 315 or curHeading < 45:
            newX, newY = x, y + 1
        elif 45 <= curHeading < 135:
            newX, newY = x + 1, y
        elif 135 <= curHeading < 225:
            newX, newY = x, y - 1
        else: # 225 <= curHeading < 315
            newX, newY = x - 1, y

        # Check if an adjacent mapped area is save to move to
        if bot.trackArr[newX][newY] != "!":
            return True
    
    bot.brain.screen.print("All directions blocked.")
    return False
        
def main():
    bot = Bot()

    while True:
        followPath(bot)

main()