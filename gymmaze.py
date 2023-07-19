import os.path
from stable_baselines3 import PPO
from mazeenv3 import MazeEnv
import time

env = MazeEnv()
env.reset()

#model_load_dir = f"models/PPO-1689712353/125000.zip"
#model = PPO.load(model_load_dir, env=env)

models_dir = f"models/PPO-{int(time.time())}"
log_dir = f"logs/PPO-{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
if not os.path.exists(log_dir):
        os.makedirs(log_dir)

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)

TIMESTEPS = 20000  # Modify the number of timesteps

for i in range(1, 10000000000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")

    episodes = 1
    for ep in range(episodes):
        obs = env.reset()
        done = False
        for i in range(200):
            env.render()
            action = model.predict(obs)
            obs, reward, done, info = env.step(action[0])

            if done:
                break

env.close()