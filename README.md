# Robotics Group 19 - Astromech
Assessment 2

- Lewis James - c2067150
- Lewis Worton - c1014451

Video demonstration - https://youtu.be/UEaqtQ_dPZY

## Bot Process
The bot's aim is to move through an area and clear up any items within this area. In our demo we use lego bricks.
To achieve this it follows the below process:

1. From it's start location, it will move forward until it encounters an obstacle or a distance > 350mm.
2a. If the robot encounters a distance of more that 350mm, such as the edge of a table, it will turn and attempt to move forward again.
2b. If the robot encounters an obstacle, an object within 240mm, it will turn to avoid the obstacle and attempt to find a way around it.
3. The robot will continue to do this until it has completed it's area or cannot move due to obstacles blocking every path.

While it is moving, it will be using the front scoop to pick up any items it comes across. In our demo, we used lego bricks.

## Bot Limitations

- During our demo, we used the slowest speed we tested with as this gives the robot the most stability. However, this makes it significantly harder for the bot to scoop items up and the reduced speed tends to cause the bot to push items instead.
- When turning, the back right wheel will sometimes come off, we believe this is due to the motor shaft housing as when we tried moving the wheels to different motors, it was always the back right wheel which would fall off.

## How to build the program
### Prerequisites
- The fully assembled EXP robot
- A laptop with Visual Studio Code and the VEX Robotics extension or the VEX EXP IDE
- 1x USB-A to USB-C cable

### Copying the code
- Create a new folder for the project by going to the VEX Robotics extension tab and selecting 'New Project'.
- Select EXP -> Python -> EXP Empty Template Project and give it a name, choose the location to save it to and optionally give it a description.
- Once created, go to src/main.py, copy the code from GitHub and save it.

### Building and downloading to VEX Brain
- Plug the laptop into the VEX brain and wait for the VEX Robotics extension to detect the brain.
- Once it is detected, at the bottom of VSCode, you will be able to see a Slot # and a download icon.
- Choose the slot you would like to save the program to and then click download icon labeled 'Build and Download'
- Now on the VEX EXP brain, go to Programs and choose the slot that you saved it to.
- You should now be able to select run which will start the program. ENSURE TO UNPLUG THE LAPTOP BEFORE PRESSING RUN

## Resources Used
- [Vex EXP documentation for Python](https://api.vex.com/exp/home/python/index.html)