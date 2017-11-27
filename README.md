# Description
Project is designed to allow Lego Mainstorm differential drive robot equiped with sonars navigate in unknown labyrinth and build it's map.

# Installation

Be sure that you have installed Python 3.x on your computer.

Install ev3dev version of Linux on the micro SD card following [instructions](http://www.ev3dev.org/docs/getting-started/#step-2-flash-the-sd-card).

Plug micro SD to the robot's main block, turn it on and establish connection by ssh following [instructions](http://www.ev3dev.org/docs/networking/).

Download code and copy it to the sd card via ssh connection.

Install python requirements both on your computer and on the sd card:

```pip install -r requirements.pip```

# Usage

Firstly, differential drive robot with 3 sonars must be constructed. One sonar is placed along the main axes of the robot and two others - to both sides 
 perpendicularly to first one. Side sonars are responsible for detecting distance to walls and forward sonars just detects finish wall for now. 
 Check that wheel radius and half of the distance between wheels match those provided in ```run_controller.py```. Place robot 
 to the labyrinth, connect to it and execute:
 
 ```python run_controller.py```
 
 When the robot reaches finish wall map file will be generated in ```resources/``` directory. Download the file and place it 
 into the same folder on your computer. To visualize built map execute:
 
 ```python run_visualizer.py```
 
During the [experiment](https://www.youtube.com/watch?v=TkHmNSkewWQ) robot started from the position (0, 0) and 
built the following map:

![img](https://ibb.co/kLjeyR)

# Algorithm
