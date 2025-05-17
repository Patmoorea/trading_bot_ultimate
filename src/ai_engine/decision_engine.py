import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3.common.vec_env import DummyVecEnv
from ppo_transformer import create_ppo_model

class TradingEnv(gym.Env):
    def __init__(self):
        self.observation_space = spaces.Box(low=-10, high=10, shape=(256,))
        self.action_space = spaces.Discrete(3)  # 0=hold, 1=buy, 2=sell
        
    def reset(self, seed=None, options=None):
        return np.random.rand(256), {}
        
    def step(self, action):
        obs = np.random.rand(256)
        reward = 0.1 if action == 1 else -0.1 if action == 2 else 0
        terminated = False
        truncated = False
        info = {}
        return obs, reward, terminated, truncated, info

class DecisionEngine:
    def __init__(self):
        self.technical_model = None  # Initialisé plus tard
        env = DummyVecEnv([lambda: TradingEnv()])
        self.strategy_model = create_ppo_model(env)
        
    def make_decision(self, market_data):
        obs = np.random.rand(256)  # Simulation
        action, _ = self.strategy_model.predict(obs)
        return {
            'action': ['hold', 'buy', 'sell'][action],
            'confidence': 0.8
        }

if __name__ == '__main__':
    engine = DecisionEngine()
    print(engine.make_decision({}))
