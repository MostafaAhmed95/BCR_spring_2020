import gym 
import numpy as np
import collections
env = gym.make('CartPole-v0')

pvariance = 0.1
ppvariance = 0.02
nhiddens = 5

ninputs = env.observation_space.shape[0]
if (isinstance(env.action_space, gym.spaces.box.Box)):
    noutputs = env.action_space.shape[0]
else:
    noutputs = env.action_space.n  

W1 = np.random.randn(nhiddens,ninputs) * pvariance
W2 = np.random.randn(noutputs, nhiddens) * pvariance
b1 = np.zeros(shape=(nhiddens, 1))
b2 = np.zeros(shape=(noutputs, 1))

def feed(observation,w1,w2,b1,b2):
    observation.resize(ninputs,1)
    Z1 = np.dot(W1, observation) + b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = np.tanh(Z2)

    if (isinstance(env.action_space, gym.spaces.box.Box)):
        action = A2
    else:
        action = np.argmax(A2)

    return action

def reward(w1,w2,b1,b2,x=False):
    sum_reward = 0
    for _ in range(10):
        observation=env.reset()
        done = False
        while(not done):
            if x:
                env.render()
            action=feed(observation,w1,w2,b1,b2)
            observation, reward, done, info = env.step(action)
            sum_reward = sum_reward + reward

    #print("the total reward",sum_reward)
    #env.close()
    #print(sum_reward)
    return sum_reward
#reward(W1,W2,b1,b2)

rank={}
order_rank=collections.OrderedDict()
no_of_parameters = nhiddens*ninputs+ noutputs*nhiddens + nhiddens + noutputs
popluation_size = 4
population_matrix = np.random.randn(popluation_size,no_of_parameters)
#print(population_matrix.shape)

#generation iteration
for _ in range (100):
    for i in range(popluation_size):
        w1 = population_matrix[i,:nhiddens*ninputs]
        #print(w1.shape)
        w1=w1.reshape((nhiddens,ninputs))
        w2 = population_matrix[i,nhiddens*ninputs:nhiddens*ninputs+noutputs*nhiddens]
        #print(w2.shape)
        w2=w2.reshape((noutputs,nhiddens))
        x=nhiddens*ninputs+noutputs*nhiddens
        b1 = population_matrix[i, x:x+nhiddens]
        #print(b1.shape)
        b1=b1.reshape((nhiddens,1))
        x=x+nhiddens
        b2 = population_matrix[i, x:]
        #print(b2.shape)
        b2=b2.reshape((noutputs,1))

        #print("nodsfahf",w1.shape,w2.shape,b1,b2)
        #call for feed 
        rank[i] = reward(w1,w2,b1,b2)
    #print(rank)
    #print("before",rank)
    #sort the dictonary by value
    print(max(rank.values()))
    lsty=list()
    #d=0
    for key, value in sorted(rank.items(), key=lambda item: item[1]):
        #print(key,value)
        #rank[key]=value
        order_rank[key] = value
        #d+=1
        lsty.append(key)
    #print(rank)
    #print(order_rank)
    #print(lsty)
    #print(len(lsty))
    

    for i in range(int(len(lsty)/2)):
        noise = np.random.randn(1,no_of_parameters) * ppvariance
        #print(lsty[i],"change to",lsty[i+int(len(lsty)/2)])
        population_matrix[lsty[i],:] = population_matrix[lsty[i+int(len(lsty)/2)],:] + noise

w1 = population_matrix[i,:nhiddens*ninputs]
w1=w1.reshape((nhiddens,ninputs))
w2 = population_matrix[i,nhiddens*ninputs:nhiddens*ninputs+noutputs*nhiddens]
w2=w2.reshape((noutputs,nhiddens))
x=nhiddens*ninputs+noutputs*nhiddens
b1 = population_matrix[i, x:x+nhiddens]
b1=b1.reshape((nhiddens,1))
x=x+nhiddens
b2 = population_matrix[i, x:]
b2=b2.reshape((noutputs,1))
reward(w1,w2,b1,b2,True)



env.close()