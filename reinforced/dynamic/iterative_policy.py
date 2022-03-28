from grid_world import standard_grid, negative_grid, ACTION_SPACE
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

    grid = standard_grid()
    for i in range(grid.rows):
        for j in range(grid.cols):
            s = (i, j)
            if not grid.is_terminal(s):
                for a in ACTION_SPACE:
                    s2 = grid.get_next_state(s, a)
                    transition_probs[(s, a, s2)] = 1
                    if s2 in grid.rewards:
                        rewards[(s, a, s2)] = grid.rewards[s2]

    ### fixed policy ###
    policy = {
        (2, 0): 'U',
        (1, 0): 'U',
        (0, 0): 'R',
        (0, 1): 'R',
        (0, 2): 'R',
        (1, 2): 'U',
        (2, 1): 'R',
        (2, 2): 'U',
        (2, 3): 'L',
    }
    print_policy(policy, grid)

    def bellman(s,gamma,V):
        new = 0
        for a in ACTION_SPACE:
            for s2 in grid.all_states():
                #action probability is deterministic
                action_prob = 1 if policy.get(s) == a else 0
                # reward is a function of (s, a, s'), 0 if not specified
                r = rewards.get((s, a, s2), 0)
                new += action_prob * transition_probs.get((s, a, s2), 0) * (r + gamma * V[s2])
        return new

    #implement policy evaluation
    V = {}
    #initialize 
    for s in grid.all_states():
        V[s]= 0 

    gamma = 0.9
    lam = 0.001
    i = 0
    while True:
        i += 1
        change = 0.0
        for s in grid.all_states():
            if not grid.is_terminal(s):
                v_old = V[s]
                new = bellman(s,gamma,V)
            # after done getting the new value, update the value table
            V[s] = new
            change = max(change, np.abs(v_old - V[s]))
            print('\n')
            print_values(V, grid)
            print(f'Iteration {i}\n')
        if change < lam:
            break



    
                
