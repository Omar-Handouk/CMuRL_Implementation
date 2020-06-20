import __future__

import gym

env = gym.make('CMuRL_Env:CMuRL-Env-v0')

action = env.action_space.sample()

env.step(action)
