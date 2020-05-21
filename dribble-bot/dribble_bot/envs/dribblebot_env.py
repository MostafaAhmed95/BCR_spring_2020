import os
import math
import numpy as np

import gym
from gym import spaces
from gym.utils import seeding

import pybullet as p
import pybullet_data
import random

#visiualize the robot during training
#p.connect(p.GUI)

class DribblebotBulletEnv(gym.Env):
    metadata = {
    'render.modes': ['human', 'rgb_array'],
    'video.frames_per_second' : 50
        }

    def __init__(self, render=False):
        # action encodes the torque applied by the motor of the wheels
        #range of the speed of the left & right wheels
        self.action_space = spaces.Box(np.array([-10,-10]), np.array([+10,+10]), dtype='float32')
        self.observation = []
        #observe the angle and the xpose, ypose of the robot, dist bet the ball & dest, dist bet robot & ball
        #self.observation_space = spaces.Box(np.array([-math.pi, -50, -50, -50, -50]),np.array([math.pi, 50, 50, 50, 50]), dtype='float32')
        # dist between ball & goal dist between robot & ball 
        self.observation_space = spaces.Box(np.array([-50, -50]),np.array([50, 50]), dtype='float32')
        
        #todo create a goal destination variable Randomly
        self.dest_goal_x = random.randint(1, 10)
        self.dest_goal_y = random.randint(1, 10)

        self.connectmode = 0
        # starts without graphic by default
        self.physicsClient = p.connect(p.DIRECT)
        # used by loadURDF
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.seed()
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.set_actuator(action)
        p.stepSimulation()
        self.observation = self.compute_observation()
        reward = self.compute_reward()
        done = self.compute_done()
        self.envStepCounter += 1
        status = "Step " + str(self.envStepCounter) + " Reward " + '{0:.2f}'.format(reward)
        p.addUserDebugText(status, [0,-1,3], replaceItemUniqueId=1)
        return np.array(self.observation), reward, done, {}

    def reset(self):
        #make to velocity separtly on for left and another for right 
        self.vt_l = 0
        self.vt_r = 0 
        self.maxV = 24.6    # max lelocity, 235RPM = 24,609142453 rad/sec

        self.envStepCounter = 0
        p.resetSimulation()
        p.setGravity(0, 0,-10)  # m/s^2
        p.setTimeStep(0.01)  # the duration of a step in sec
        
        path = os.path.abspath(os.path.dirname(__file__))
        planeId = p.loadURDF(os.path.join(path, "plane.urdf"))
        self.ball = p.loadURDF(os.path.join(path, "sphere_small.urdf"), basePosition=[0.2,0,0])
        robotStartPos = [0,0,0.001]
        self.botId = p.loadURDF(os.path.join(path, "turtlebot.urdf"),robotStartPos)

        #the ball previous distance
        ballPos, ballOrn = p.getBasePositionAndOrientation(self.ball)
        ballPos = ballPos[0]-robotStartPos[0],ballPos[1]-robotStartPos[1],ballPos[2]-robotStartPos[2]
        
        # ball & dest initial distance
        self.ball_prev_dis =  np.sqrt((ballPos[1]-self.dest_goal_y)**2 + (ballPos[0]-self.dest_goal_x)**2)
        # robot & ball initial distance
        self.rb_prev_dis = np.sqrt(ballPos[1]**2 + ballPos[0]**2)

        self.observation = self.compute_observation()
        return np.array(self.observation)

    def render(self, mode='human', close=False):
        if (self.connectmode == 0):
            p.disconnect(self.physicsClient)
            # connect the graphic renderer
            self.physicsClient = p.connect(p.GUI)
            self.connectmode = 1
        pass

    def set_actuator(self, action):
        """Update the desired velocity of the actuators"""
        self.vt_l, self.vt_r = 100 * action[0], 100 * action[1]
        p.setJointMotorControl2(bodyUniqueId=self.botId,
        jointIndex=0,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity= self.vt_l)
        p.setJointMotorControl2(bodyUniqueId=self.botId,
        jointIndex=1,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity= self.vt_r)

    
    def compute_observation(self):
        """Compute observation depend on the current positon and velocity"""
        robotPos, robotOrn = p.getBasePositionAndOrientation(self.botId)
        robotEuler = p.getEulerFromQuaternion(robotOrn)
        # TOdo compute the observation for the ball
        ballPos, ballOrn = p.getBasePositionAndOrientation(self.ball)
        ballEuler = p.getEulerFromQuaternion(ballOrn)
        # position of th ball w.r.t the robot
        ballPos = ballPos[0]-robotPos[0],ballPos[1]-robotPos[1],ballPos[2]-robotPos[2]
        # distance between ball & destination
        ball_dist =  np.sqrt((ballPos[1]-self.dest_goal_y)**2 + (ballPos[0]-self.dest_goal_x)**2)
        #distance between the robot and the ball
        rb_dist = np.sqrt((ballPos[1])**2 + (ballPos[0])**2) 
        #return (np.array([robotEuler[2], robotPos[0], robotPos[1], ball_dist, rb_dist], dtype='float32'))
        return (np.array([ ball_dist, rb_dist], dtype='float32'))
    def compute_reward(self):
        #weights
        D = 0.7
        B = 0.3

        #the current distance bet the ball & destination
        c_b_dis = self.observation[0]
        #velocity of the ball toward the destination time step is 0.01 sec
        v_ball = (self.ball_prev_dis - c_b_dis)/0.01
        
        #the current distance bet the robot and the ball
        c_r_dis = self.observation[1]
        #velocity of robot toward the ball with time step is 0.01 sec
        v_r = (self.rb_prev_dis - c_r_dis)/0.01
        
        new_reward = D * (v_ball) + B * (v_r)
        self.prev_dis = c_b_dis
        self.rb_prev_dis = v_r
        return new_reward
        

    def compute_done(self):
        # episode ends when the ball gets near the goal or after 100 steps
        d = self.compute_observation()
        return d[0]<0.1 or self.envStepCounter >= 100

        