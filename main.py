import __future__

import gym
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO1
from env.CMuRLEnv import CMuRLEnv

env = DummyVecEnv([lambda: CMuRLEnv()])

model = PPO1(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=25000)
model.save('tester')

del model
