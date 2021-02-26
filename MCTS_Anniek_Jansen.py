from binarytree import tree
from binarytree import build 
from binarytree import Node
import numpy as np 
import random

depth = 12
number_leafnodes = 2 ** depth

def random_leafnodes(depth, number_leafnodes):
    leafnodes = np.random.uniform(low = 0, high = 100, size= number_leafnodes) 
    return leafnodes

leafnodes = random_leafnodes(depth, number_leafnodes)

def create_tree(leafnodes, number_leafnodes):
    number_total_nodes = 2 ** (depth + 1) -1
    numberWithoutLeafnodes = number_total_nodes - number_leafnodes
    nodes = list(range(1, numberWithoutLeafnodes + 1))
    nodes.extend(leafnodes)
    binary_tree = build(nodes) 
    return binary_tree, nodes

binary_tree, nodes = create_tree(leafnodes, number_leafnodes)
print(binary_tree)

def create_sample_tree():
    sample_nodes = list(range(1,32))
    sample_tree = build(sample_nodes)
    return sample_tree

sample_tree = create_sample_tree()
print(sample_tree)

c = 2
nr_iterations = 10

UCBvalue = []
rewards = []
visits = []

for i in range(0,16):
    UCBvalue.append(0)
    rewards.append(0)
    visits.append(0)

for i in range(0,nr_iterations):
    if max(UCBvalue) == 0:
        current_node = nodes[1]
        index = nodes.index(current_node)
        parent_node = nodes[0]    
    elif UCBvalue[2] == 0:
        current_node = nodes[2]
        index = nodes.index(current_node)
        parent_node = nodes[0]
    else:
        index = UCBvalue.index(max(UCBvalue))
        if index == 1:
            parent_node = nodes[index]
            index += 2
            current_node = nodes[index]
            if visits[current_node -1] >= visits[current_node]:
                index += 1
                current_node = nodes[index]
        elif index == 2:
            parent_node = nodes[index]
            index += 3
            current_node = nodes[index]
            if visits[current_node -1] >= visits[current_node]:
                index += 1
                current_node = nodes[index]
        elif index == 3:
            parent_node = nodes[index]
            index += 4
            current_node = nodes[index]
            if visits[current_node -1] >= visits[current_node]:
                index += 1
                current_node = nodes[index]
        elif index == 4:
            parent_node = nodes[index]
            index += 5
            current_node = nodes[index]
            if visits[current_node -1] >= visits[current_node]:
                index += 1
                current_node = nodes[index]
        elif index == 5:
            parent_node = nodes[index]
            index += 6
            current_node = nodes[index]
            if visits[current_node -1] >= visits[current_node]:
                index += 1
                current_node = nodes[index]
        elif index == 6:
            parent_node = nodes[index]
            index += 7
            current_node = nodes[index]
            if visits[current_node -1] >= visits[current_node]:
                index += 1
                current_node = nodes[index]
        else:
            print("Maximum number of iterations reached for this specific tree search.")
            print("The optimal value found: ", max(UCBvalue))
            break

    print("The current node:", current_node)
    print("The parent node:", parent_node)
    print("The hyperparameter c: ", c)

    rollout_reward = 0
    nr_rollouts = 1
    print("Number of roll outs per node: ", nr_rollouts)

    for i in range(0,nr_rollouts):
        if current_node == 2:
            rollout = random.choice(leafnodes[0:int(number_leafnodes/2) +1])
            rollout_reward += rollout
        elif current_node == 3:
            rollout = random.choice(leafnodes[int(number_leafnodes/2):])
            rollout_reward += rollout
        elif current_node == 4:
            rollout = random.choice(leafnodes[0:int(number_leafnodes/4) +1])
            rollout_reward += rollout
        elif current_node == 5:
            rollout = random.choice(leafnodes[int(number_leafnodes/4): int(number_leafnodes/2) +1])
            rollout_reward += rollout
        elif current_node == 6:
            rollout = random.choice(leafnodes[int(number_leafnodes/2): int(number_leafnodes/4*3) + 1])
            rollout_reward += rollout
        elif current_node == 7:
            rollout = random.choice(leafnodes[int(number_leafnodes/4*3):])
            rollout_reward += rollout
        elif current_node == 8:
            rollout = random.choice(leafnodes[:int(number_leafnodes/8) +1])
            rollout_reward += rollout
        elif current_node == 9:
            rollout = random.choice(leafnodes[int(number_leafnodes/8): int(number_leafnodes/4) +1])
            rollout_reward += rollout
        elif current_node == 10:
            rollout = random.choice(leafnodes[int(number_leafnodes/4): int(number_leafnodes/8*3) + 1])
            rollout_reward += rollout
        elif current_node == 11:
            rollout = random.choice(leafnodes[int(number_leafnodes/8*3): int(number_leafnodes/2) + 1])
            rollout_reward += rollout
        elif current_node == 12:
            rollout = random.choice(leafnodes[int(number_leafnodes/2): int(number_leafnodes/8*5) + 1])
            rollout_reward += rollout
        elif current_node == 13:
            rollout = random.choice(leafnodes[int(number_leafnodes/8*5): int(number_leafnodes/8*6) + 1])
            rollout_reward += rollout
        elif current_node == 14:
            rollout = random.choice(leafnodes[int(number_leafnodes/8*6): int(number_leafnodes/8*7) + 1])
            rollout_reward += rollout
        elif current_node == 15:
            rollout = random.choice(leafnodes[int(number_leafnodes/8*7): ])
            rollout_reward += rollout

        i = i + 1

    print("Total roll out reward of current node:", rollout_reward)
    rewards[index] += rollout_reward
    print("Overview of rewards:", rewards)

    visits[nodes.index(current_node)] += 1 * nr_rollouts
    visits[nodes.index(parent_node)] += 1 * nr_rollouts
    if parent_node == nodes[0]: 
        visits = visits
    elif parent_node == nodes[1] or parent_node == nodes[2]:
        visits[0] += 1 * nr_rollouts  
    elif parent_node == nodes[3] or parent_node == nodes[4]:
        visits[0] += 1 * nr_rollouts
        visits[1] += 1 * nr_rollouts
    elif parent_node == nodes[5] or parent_node == nodes[6]:
        visits[0] += 1 * nr_rollouts
        visits[2] += 1 * nr_rollouts
        
    print("Overview of visists:", visits)
    
    if rewards[1] > 0:
        UCBvalue[1] = (rewards[1]/visits[1]) + c * np.sqrt(np.log(visits[0])/visits[1]) 
    if rewards[2] > 0:    
        UCBvalue[2] = (rewards[2]/visits[2]) + c * np.sqrt(np.log(visits[0])/visits[2]) 
    if rewards[3] > 0:     
        UCBvalue[3] = (rewards[3]/visits[3]) + c * np.sqrt(np.log(visits[1])/visits[3]) 
    if rewards[4] > 0:     
        UCBvalue[4] = (rewards[4]/visits[4]) + c * np.sqrt(np.log(visits[1])/visits[4]) 
    if rewards[5] > 0: 
        UCBvalue[5] = (rewards[5]/visits[5]) + c * np.sqrt(np.log(visits[2])/visits[5]) 
    if rewards[6] > 0:     
        UCBvalue[6] = (rewards[6]/visits[6]) + c * np.sqrt(np.log(visits[2])/visits[6]) 
    if rewards[7] > 0:     
        UCBvalue[7] = (rewards[7]/visits[7]) + c * np.sqrt(np.log(visits[3])/visits[7])
    if rewards[8] > 0:     
        UCBvalue[8] = (rewards[8]/visits[8]) + c * np.sqrt(np.log(visits[3])/visits[8])
    if rewards[9] > 0:     
        UCBvalue[9] = (rewards[9]/visits[9]) + c * np.sqrt(np.log(visits[4])/visits[9])
    if rewards[10] > 0:     
        UCBvalue[10] = (rewards[10]/visits[10]) + c * np.sqrt(np.log(visits[4])/visits[10])
    if rewards[11] > 0:     
        UCBvalue[11] = (rewards[11]/visits[11]) + c * np.sqrt(np.log(visits[5])/visits[11])
    if rewards[12] > 0:     
        UCBvalue[12] = (rewards[12]/visits[12]) + c * np.sqrt(np.log(visits[5])/visits[12])
    if rewards[13] > 0:     
        UCBvalue[13] = (rewards[13]/visits[13]) + c * np.sqrt(np.log(visits[6])/visits[13])
    if rewards[14] > 0:     
        UCBvalue[14] = (rewards[14]/visits[14]) + c * np.sqrt(np.log(visits[6])/visits[14])

    print("Overview of UCB values:", UCBvalue)
    print("The maximum UCB value:", max(UCBvalue))
    print("-----")

    i = i + 1
