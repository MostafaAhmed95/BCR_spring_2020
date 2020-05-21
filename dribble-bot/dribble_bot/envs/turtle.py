import pybullet as p
import time

p.connect(p.GUI)
offset = [0, 0, 0]

import pybullet_data

turtle = p.loadURDF("turtlebot.urdf", offset)
plane = p.loadURDF("plane.urdf")
ball = p.loadURDF("sphere_small.urdf", basePosition=[0.2,0,0])
p.setRealTimeSimulation(1)

for j in range(p.getNumJoints(turtle)):
    print(p.getJointInfo(turtle, j))
forward = 0
turn = 0
while (1):
    p.setGravity(0, 0, -10)
    time.sleep(1. / 240.)
    keys = p.getKeyboardEvents()
    leftWheelVelocity = 0
    rightWheelVelocity = 0
    speed = 10

    for k, v in keys.items():

        if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            turn = -0.5
        if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_RELEASED)):
            turn = 0
        if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            turn = 0.5
        if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_RELEASED)):
            turn = 0

        if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            forward = 1
        if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED)):
            forward = 0
        if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_TRIGGERED)):
            forward = -1
        if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_RELEASED)):
            forward = 0

    rightWheelVelocity += (forward + turn) * speed
    leftWheelVelocity += (forward - turn) * speed

    p.setJointMotorControl2(turtle, 0, p.VELOCITY_CONTROL, targetVelocity=leftWheelVelocity, force=1000)
    p.setJointMotorControl2(turtle, 1, p.VELOCITY_CONTROL, targetVelocity=rightWheelVelocity, force=1000)