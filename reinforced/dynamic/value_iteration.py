#It is the optimized approach to find an optimal approach

import numpy as np
from windy_grid import windy_grid, ACTION_SPACE
from utils import *

SMALL_ENOUGH = 1e-3
GAMMA = 0.9


def get_transition_probs_and_rewards(grid):
  transition_probs = {}
  rewards = {}

  for (s, a), v in grid.probs.items():
        for s2, p in v.items():
            transition_probs[(s, a, s2)] = p
            rewards[(s, a, s2)] = grid.rewards.get(s2, 0)

  return transition_probs, rewards


if __name__ == '__main__':
    grid = windy_grid()
    transition_probs, rewards = get_transition_probs_and_rewards(grid)
    #PRINT REWARDS
    #
    print_values(grid.rewards,grid)
    #INITIALIZE V FUNCTION
    V = {}
    for s in grid.all_states():
        V[s] = 0.0
    print('\n')
    # repeat until convergence
    # V[s] = max[a]{ sum[s',r] { p(s',r|s,a)[r + gamma*V[s']] } }
    it = 0
    while True:
        biggest_change = 0
        for s in grid.all_states():
            if not grid.is_terminal(s):
                old_v = V[s]
                new_v = float('-inf')

                for a in ACTION_SPACE:
                    v = 0
                    for s2 in grid.all_states():
                        # reward is a function of (s, a, s'), 0 if not specified
                        r = rewards.get((s, a, s2), 0)
                        v += transition_probs.get((s, a, s2), 0) * (r + GAMMA * V[s2])

                    # keep v if it's better
                    if v > new_v:
                        new_v = v

                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))

        it += 1
        if biggest_change < SMALL_ENOUGH:
            break

    #Find optimal policys
    policy = {}
    for s in grid.actions.keys():
        best_a = None
        best_value = float('-inf')
        # loop through all possible actions to find the best current action
        for a in ACTION_SPACE:
            v = 0
            for s2 in grid.all_states():
                # reward is a function of (s, a, s'), 0 if not specified
                r = rewards.get((s, a, s2), 0)
                v += transition_probs.get((s, a, s2), 0) * (r + GAMMA * V[s2])

        # best_a is the action associated with best_value
        if v > best_value:
            best_value = v
            best_a = a
        policy[s] = best_a
    #We have found the optimal value function
    print_values(V,grid)
    #We have found the optimal policy
    print('\n')
    print_policy(policy,grid)
        

