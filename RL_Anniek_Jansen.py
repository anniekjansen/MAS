import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import matplotlib

gridsize = 9
termination_states = [[8,8],[6,5]]
walls = [[1,2],[1,3],[1,4],[1,5],[1,6],[2,6],[3,6],[4,6],[5,6],[7,1],[7,2],[7,3],[7,4]]
actions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
nr_iterations = 1000
gamma = 1 

reward_values = np.zeros((gridsize,gridsize)) -1
reward_values[6,5]= -50
reward_values[8,8]= 50
print("The reward values are:", "\n", reward_values)

def action_value(initial_position,action):
    if initial_position in termination_states or initial_position in walls:
        final_position = initial_position
        reward = 0   
    else:
        final_position = np.array(initial_position) + np.array(action)
        if -1 in final_position or gridsize in final_position:
                final_position = initial_position
                reward = reward_values[final_position[0],final_position[1]]
        elif list(final_position) in walls:
                final_position = initial_position
                reward = reward_values[final_position[0],final_position[1]]
        else:
            reward = reward_values[final_position[0],final_position[1]]
    
    return final_position, reward

values = np.zeros((gridsize, gridsize))
values1 = np.zeros((gridsize, gridsize))
states = [[i, j] for i in range(gridsize) for j in range(gridsize)]

def policy_evaluation(nr_iterations,gamma,values):
    for i in range(nr_iterations):
        for state in states:
            weighted_rewards = 0
            for action in actions:
                final_position, reward = action_value(state,action)
                weighted_rewards += 0.25 * (reward + gamma * values[final_position[0],final_position[1]])
            values1[state[0],state[1]] = weighted_rewards
        values = np.copy(values1)
        state_values = values
    return state_values

state_values = []    
state_values = policy_evaluation(nr_iterations,gamma,values)
print("The state value functions are:", "\n", np.round(state_values,2))

def heat_map(state_values):
    grid = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    fig, ax = plt.subplots()
    im = ax.imshow(state_values)
    sns.set(font_scale=0.7)
    ax.set_xticks(np.arange(len(grid)))
    ax.set_yticks(np.arange(len(grid)))
    ax.set_xticklabels(grid)
    ax.set_yticklabels(grid)

    for i in range(len(grid)):
        for j in range(len(grid)):
            text = ax.text(j, i, round(state_values[i, j],2),
                        ha="center", va="center", color="w")

    ax.set_title("Heat Map State Values")
    fig.tight_layout()
    plt.show()

heat_map = heat_map(state_values)

######

pi = np.ones((gridsize,gridsize))/4
pi1 = np.chararray((gridsize, gridsize))
pi1[:] = ''

def argmax(q_values):
    idx=np.argmax(q_values)
    return(np.random.choice(np.where(a==a[idx])[0].tolist()))

pit = [6,5]
treasure = [8,8]    

def greedify_policy(state,pi,pi1,gamma,values):  
        q_values=np.zeros(len(actions))
        for idx,action in enumerate(actions):
            final_position,reward = action_value(state,action)
            q_values[idx] += 1/4* (reward + gamma * values[final_position[0],final_position][1])
        idx=q_values.argmax()
        
        pi[state[0],state[1]]=idx 
        if list(final_position) in walls:
            pi1[state[0],state[1]]= 'wall'
        elif list(final_position) == treasure:
            pi1[state[0],state[1]] = 'treasure' 
        # elif list(final_position) == pit:
        #     pi1[state[0],state[1]] = 'pit'
        elif(idx == 0):
            pi1[state[0],state[1]]='up'
        elif(idx == 1):
            pi1[state[0],state[1]]= 'down'
        elif(idx == 2):
            pi1[state[0],state[1]]= 'right'
        elif(idx == 3):
            pi1[state[0],state[1]]='left'
               
def improve_policy(pi, pi1,gamma,values):
    policy_stable = True
    for state in states:
        old = pi[state].copy()
        greedify_policy(state,pi,pi1,gamma,values)
        if not np.array_equal(pi[state], old):
            policy_stable = False
    return pi, pi1, policy_stable

def policy_iteration(gamma, theta):
    values = np.zeros((gridsize, gridsize))
    pi = np.ones((gridsize,gridsize))/4
    pi1 = np.chararray((gridsize, gridsize), itemsize=1)
    pi1[:] = ''
    policy_stable = False
    while not policy_stable:
        values = policy_evaluation(nr_iterations,gamma,values)
        pi,pi1, policy_stable = improve_policy(pi,pi1, gamma,values)
    return values, pi,pi1

theta=0.1
values, pi,pi1 = policy_iteration(gamma, theta)

def update(values, state, gamma):
    q_values=np.zeros(len(actions))
    
    for idx,action in enumerate(actions):
        final_position,reward = action_value(state,action)
        q_values[idx] += 1/4* (reward + gamma * values[final_position[0],final_position][1])
    idx=q_values.argmax()
            
    max = np.argmax(q_values)
    values[state[0],state[1]] = q_values[max]    

def value_iteration(gamma, theta):
    values = np.zeros((gridsize, gridsize))
    while True:
        delta = 0
        for state in states:
            v_old=values[state[0],state[1]]
            update(values, state, gamma)
            delta = max(delta, abs(v_old - values[state[0],state[1]]))
        if delta < theta:
            break
    pi = np.ones((gridsize,gridsize))/4
    for state in states:
        greedify_policy(state,pi,pi1,gamma,values)
    return values, pi,pi1

gamma = 1
theta = 0.000001
values,pi,pi1 = value_iteration(gamma, theta)

optimal_policy = pi1.decode("utf-8")
optimal_policy[6,5] = 'p'

print("Policy:", "\n", optimal_policy)
