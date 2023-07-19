import gym
from gym import spaces
import numpy as np
import cv2
from collections import deque
from collapsed import *

N_DISCRETE_ACTIONS = 4
MAX_MOVES = 5000
SIZE = 60
OBSTACLES = 550
REMEMBER_MOVES = 150


class MazeEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(MazeEnv, self).__init__()
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Box(low=0, high=255, shape=(4 + 4 + REMEMBER_MOVES,),
                                            dtype=np.float32)
        self.prev_actions = deque(maxlen=REMEMBER_MOVES)

    def collide(self, new_char_x, new_char_y, tiles):
        if tiles[new_char_x][new_char_y] == '@':
            return True
        else:
            return False

    def step(self, action):
        self.prev_actions.append(action)
        self.total_actions += 1

        new_char_x = self.char_x
        new_char_y = self.char_y

        if action == 0:
            new_char_x -= 1
        elif action == 1:
            new_char_x += 1
        elif action == 2:
            new_char_y -= 1
        elif action == 3:
            new_char_y += 1


        if not self.collide(new_char_x, new_char_y, self.tiles):
            self.char_x = new_char_x
            self.char_y = new_char_y
            self.reward = -0.5
        else:
            self.reward = -4

        deltax = self.end_x - self.char_x
        deltay = self.end_y - self.char_y
        dist = (deltax * deltax) + (deltay * deltay)

        if dist<self.mindist:
            self.mindist = dist
            self.reward = 50

        if self.char_x == self.end_x and self.char_y == self.end_y:
            print('done')
            self.reward = 10000 - self.total_actions
            self.done = True

        if self.total_actions > MAX_MOVES:
            self.reward = -1000
            self.done = True

        Act1 = 0
        Act2 = 0
        Act3 = 0
        Act4 = 0
        if self.tiles[self.char_x-1][self.char_y]  == ' ':
            Act1 = 1
        if self.tiles[self.char_x+1][self.char_y]  == ' ':
            Act2 = 1
        if self.tiles[self.char_x][self.char_y-1] == ' ':
            Act3 = 1
        if self.tiles[self.char_x][self.char_y+1] == ' ':
            Act4 = 1

        self.observation = [self.char_x, self.char_y, deltax, deltay] \
            +[Act1, Act2, Act3, Act4]+ list(self.prev_actions)

        self.observation = np.array(self.observation)
        info = {}

        return self.observation, self.reward, self.done, info

    def reset(self, **kwargs):
        self.reward = 0
        self.done = False
        self.tiles = [['@' if x == 0 or x == SIZE - 1 or y == 0 or y == SIZE - 1 else ' ' for y in range(SIZE)] for x in range(SIZE)]
        self.total_actions = 0
        self.start_init = False
        self.end_init = False
        self.char_x = 0
        self.char_y = 0
        self.end_x = 0
        self.end_y = 0
        self.mindist = SIZE*SIZE

        self.obst_list = []
        for _ in range(OBSTACLES):
            while True:
                x = random.randint(1, SIZE - 1)
                y = random.randint(1, SIZE - 1)
                if self.tiles[x][y] == ' ':
                    self.tiles[x][y] = '@'
                    self.obst_list.append(x)
                    self.obst_list.append(y)
                    break

        while not self.start_init:
            x = random.randint(1, SIZE-1)
            y = random.randint(1, SIZE-1)
            if self.tiles[x][y] == ' ':
                self.char_x = x
                self.char_y = y
                self.start_init = True

        while not self.end_init:
            x = random.randint(1, SIZE - 1)
            y = random.randint(1, SIZE - 1)
            if self.tiles[x][y] == ' ':
                self.end_x = x
                self.end_y = y
                self.end_init = True

        self.prev_actions.clear()
        self.prev_actions.extend([-1] * REMEMBER_MOVES)
        deltax = self.end_x - self.char_x
        deltay = self.end_y - self.char_y

        Act1 = 0
        Act2 = 0
        Act3 = 0
        Act4 = 0
        if self.tiles[self.char_x - 1][self.char_y] == '@':
            Act1 = 1
        if self.tiles[self.char_x + 1][self.char_y] == '@':
            Act2 = 1
        if self.tiles[self.char_x][self.char_y - 1] == '@':
            Act3 = 1
        if self.tiles[self.char_x][self.char_y + 1] == '@':
            Act4 = 1

        self.observation = [self.char_x, self.char_y, deltax, deltay] \
                           + [Act1, Act2, Act3, Act4] + list(self.prev_actions)
        self.observation = np.array(self.observation)
        return self.observation

    def render(self, mode='human'):
        img = np.zeros((SIZE*10, SIZE*10, 3), dtype='uint8')
        for x in range(SIZE):
            for y in range(SIZE):
                if self.tiles[x][y] == '@':
                    cv2.rectangle(img, (x * 10, y * 10), (x * 10 + 10, y * 10 + 10), (255, 255, 255), 3)
        cv2.rectangle(img, (self.char_x * 10, self.char_y * 10), (self.char_x * 10 + 10, self.char_y * 10 + 10), (0, 255, 0), 3)
        cv2.rectangle(img, (self.end_x * 10, self.end_y * 10), (self.end_x * 10 + 10, self.end_y * 10 + 10), (255, 0, 0), 3)

        cv2.imshow('a', img)
        cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()
