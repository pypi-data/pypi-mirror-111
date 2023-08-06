def default_reward_func(env):
    # make span reward (a.k.a completion time)
    reward = 0 if not env.done else env.manager.time
    return reward
