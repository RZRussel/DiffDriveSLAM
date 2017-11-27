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

![img](https://s17.postimg.org/hu9f03d1r/map.png)

# Algorithm

Main idea of the algorithm is based on PID controller and average filter. While moving through the labirynth algorithm reads data from the side sonars and tries to correct position of the robot to be in the middle of the corridor relatively opposite walls. To achive this difference between distances to the left and right walls considered and correction angle is calculated as ```atan2``` of this difference. To obtain stable process this angle is filtered using PID controller with parameters ```kp=0.25 ki=0.0 kd=0.1```. However data from the sonars are influenced by 3 types of errors: gaussian white noise, failures (fails to detect obstacle and return max value) and random measurement (returns unexplained measurements due to reflection of the signal or cross-talk with others). To overcome this problems the data was smoothed with average filter (n=3 - found using experements) and none-zero differential coefficient was applied to produce high response to steering.

Based on the angle returned by PID controller new angular velocity is obtained. So robot moves with constant linear velocity and dynamic angular velocities. This pair of velocities are transformed to wheels rotation velocities and robot continue trip. Time between updates of velocities is picked ```0.1```. Using pair of velocities and time between updates new position of the robot and angle (orientaion) relatively initial one can be estimated from previous position and orientation (consider ```odometry.py``` for more information). Moreover knowing position, orientation of the robot  and distance to the obstacles from the sonar position of the obstacles can be estimated (consider ```controller.py``` for more information).
