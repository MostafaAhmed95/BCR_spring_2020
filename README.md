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

### Exercise 4
from comparing the original gym_locomotion file with the revised reward file we found that in the original one we compute the reward as a sum of many variables as electricity_cost, joints_at_limit_cost, feet_collision_cost which are variables that act as a penlaty so or robot take in consideration to not get high values in these terms so it maybe slower in reaching to the goal than the new revised reward function, in the revised one we change the step method so our reward now depend only on the progress that we make towards the goal so this technique is much more suitable for evolutionary strategies as it doesn't depend on the other variables and depend only on the progress so we are able to make use of the variables like electrcity_cost in our favour.

### Exercise 5
the balance-bot directory with created with the same hierarchy mentioned in the tutorial, I needed to copy the URDF from the evorobotpy/exercises to the balance-bot directory as it was giving me an error, after that I copied a .ini file from evorobotpy and change the name of the enviroment to balancebot-v0, now I was able to compile it using <br/>
cd balance-bot <br/>
pip install -e . <br/>
then I evolve it with seed 10 <br/>
python3 ../bin/es.py -f balance_bot.ini -s 10<br/>

### Exercise 6
as it is kinetic enviroment the evolution happen much faster than the dynamic one<br/>
by analyzing the robots beheviour I found that they can be divided into two families one that approach the cylinder and keep oscilating the other one keep moving around the cylinder<br/>
the behaviour depend mostly on the sensor structure in our robot so some robot try to get the most distances from the wall other group try to find the clyinder directly and keep oscilating around it<br/>
after training with the feed forward  which in terms of evolution is much faster than the LSTM one since a feedforward network has no notion of order in time, and the only input it considers is the current example it has been exposed to, which make it exposed to the vanishing gradients problem but overall if our network is not that deep so there is no problem<br/>