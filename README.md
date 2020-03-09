# BCR_spring_2020
All exercises and assignments in Innopolis University Course Behavioural and Cognitive

### exercise 2
the robot manage to solve the problem at every time.<br/>

**changing the popultion size from 4 to 10**<br/>
observation: obiously slower training process but if in our first generation there was an individual with high sum of reward we will have higher rate of getting better rewards<br/>
conclusion: increasing number of population will get us better reward for our final parameters

**changing hidden units from 5 to 50**<br/>
observation: there is no such huge difference from 5 to 50 but maybe I get better sum of reward<br/> 
Conclusion: I guess that more hidden units supposed to give more stable results?

**changing ppvariance from 0.02 to 0.2**<br/>
observation: the rate of change to a higher sum reward is very high
conclusion: I think this because we take more aggresive steps to the better solution<br/>
thought: why we can't make this ppvarince a variable that start with a very high value and decrease gradually with each generation to be able to convarege to the best parameters with least number of generation
**changing number of episodes from 100 to 10**<br/>
thought: I think number as we increase the number of epsiodes we give more chance to the better parameters to show as we give to chance to face different initials of pole position 

### exercise 3
**STATE:**
The state consists of the sin() and cos() of the two rotational joint
angles and the joint angular velocities<br/>
A state of [1, 0, 1, 0, ..., ...] means that both links point downwards<br/>

**ACTIONS:**
The action is either applying +1, 0 or -1 torque on the joint between the two pendulum links.

**Reward**
reward = -1 (as long as our arm didn't reach the line)<br/>
reward = 0 (when our arm reach the line)<br/>


note we should be at /opt/evorobotpy/xacrobot to be able to use acrobot.ini in the following<br/>
```python3  
python3 ../bin/es.py -f acrobot.ini -s 11
```
we will try diffrent number of seeds and show the results <br/>





##### seed 11 (the example default)
trying with the initial parameters at acrobot.ini and with seed 11<br/>
**Results**<br/> 

##### seed 100
the best fitness obtained to date (start with much higher value nagtive )
best fitness obtained during post evaluation tests to date #difference between this and the previous point (the same here but both start to decrease at high rate)
but after around 25% we start to be near 60 or 70
##### seed 3
also start with high negatives and there was no distinctive difference for me as least for first couple of iterations