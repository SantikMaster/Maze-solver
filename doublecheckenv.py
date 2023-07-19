from mazeenv3 import MazeEnv

env = MazeEnv()
episodes = 50

for ep in range(episodes):
    done = False
    obs = env.reset()
    for i in range(30):
        ran_action = env.action_space.sample()
        print("action", ran_action)
        obs, reward, done, info = env.step(ran_action)
        env.render()
        print("reward", reward)
