from windy_grid import windy_grid, negative_grid, ACTION_SPACE
from utils import print_values, print_policy
import numpy as np

if __name__ == '__main__':
    #create dictionaries for state transition probabilities and policy

    # the key is (s, a, s'), the value is the probability
    # that is, transition_probs[(s, a, s')] = p(s' | s, a)
    # any key NOT present will considered to be impossible (i.e. probability 0)
    transition_probs = {}
    # to reduce the dimensionality of the dictionary, we'll use deterministic
    # rewards, r(s, a, s')
    # note: you could make it simpler by using r(s') since the reward doesn't
    # actually depend on (s, a)
    rewards = {}

    grid = windy_grid()
    for (s, a), v in grid.probs.items():
        for s2, p in v.items():
            transition_probs[(s, a, s2)] = p
            rewards[(s, a, s2)] = grid.rewards.get(s2, 0)

    ### probabilitic policy ###
    policy = {
    (2, 0): {'U': 0.5, 'R': 0.5},
    (1, 0): {'U': 1.0},
    (0, 0): {'R': 1.0},
    (0, 1): {'R': 1.0},
    (0, 2): {'R': 1.0},
    (1, 2): {'U': 1.0},
    (2, 1): {'R': 1.0},
    (2, 2): {'U': 1.0},
    (2, 3): {'L': 1.0},
    }
    print_policy(policy, grid)

    def bellman(s,gamma,V):
        new = 0
        for a in ACTION_SPACE:
            for s2 in grid.all_states():
                #action probability is probabilistic
                action_prob = policy[s].get(a,0)
                # reward is a function of (s, a, s'), 0 if not specified
                r = rewards.get((s, a, s2), 0)
                new += action_prob * transition_probs.get((s, a, s2), 0) * (r + gamma * V[s2])
        return new

    #implement policy evaluation
    V = {}
    #initialize 
    for s in grid.all_states():
        V[s] = 0 

    gamma = 0.9
    lam = 0.0001
    i = 0
    while True:
        biggest_change = 0
        for s in grid.all_states():
            if not grid.is_terminal(s):
                old_v = V[s]
                new_v = bellman(s,gamma,V)
                 # after done getting the new value, update the value table
                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))
        print(f'{biggest_change}\n')
        print_values(V, grid)
        print('\n')

        if biggest_change < lam:
            break
    print(V)