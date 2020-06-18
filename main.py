import __future__

import gym
from stable_baselines.common.vec_env import DummyVecEnv, VecCheckNan
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO1
from env.CMuRLEnv import CMuRLEnv

env = DummyVecEnv([lambda: CMuRLEnv()])
env = VecCheckNan(env, raise_exception=True)

model = PPO1(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=25000)

obs = env.reset()
for _ in range(10000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()