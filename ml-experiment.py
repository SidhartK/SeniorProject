import gym
from gym import spaces
import numpy as np
import random
from collections import deque

class Task:
    def __init__(self, assignment_time, duration, reward):
        self.assignment_time = assignment_time
        self.duration = duration
        self.time_left = duration
        self.reward = reward

class SimpleEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}
    
    def __init__(self, num_worker_modes=3, time_increment=1.0, schedule=None):
        super(SimpleEnv, self).__init__()
        
        self.num_worker_modes = num_worker_modes
        self.time_increment = time_increment
        self.schedule = schedule if schedule is not None else []
        self.schedule_idx = 0
        self.current_time = 0.0
        
        # Define action and observation space
        self.action_space = spaces.MultiDiscrete([num_worker_modes] * len(self.schedule))
        self.observation_space = spaces.Discrete(1)  # Dummy observation space
        
        # Initialize task queues and worker state
        self.task_queues = [deque() for _ in range(num_worker_modes)]
        self.worker_state = random.randint(0, num_worker_modes - 1)
    
    def step(self, action):
        reward = 0.0
        
        # Queue tasks based on the action
        for i in action:
            if self.schedule_idx < len(self.schedule):
                task = self.schedule[self.schedule_idx]
                self.task_queues[i].append(task)
                self.schedule_idx += 1
        
        # Update worker state randomly
        self.worker_state = random.randint(0, self.num_worker_modes - 1)
        
        # Process tasks in the current worker state queue
        time_budget
