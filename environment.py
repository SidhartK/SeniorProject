import gym
from gym import spaces
from collections import deque
from enum import Enum
import matplotlib.pyplot as plt

class TaskTypes(Enum):
    SCHOOL = 0
    WORK = 1
    HOBBY = 2

class WorkModes(Enum):
    SCHOLAR = 0
    WORKER = 1
    HOBBYIST = 2

SCORE_TABLE = [
    [0.5, 0.0, 0.0],
    [0.0, 0.5, 0.0],
    [0.0, 0.0, 0.5],
]

class Task:
    def __init__(self, task_type: TaskTypes, release_time, base_duration, reward=1.0):
        self.task_type = task_type
        self.release_time = release_time
        self.base_duration = base_duration
        self.time_left = None
        self.reward = reward

class TaskEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}
    
    def __init__(self, mode_switch_frequency=1.0, num_tasks_per_action=1, schedule=None):
        super(TaskEnv, self).__init__()
        
        self.mode_switch_frequency = mode_switch_frequency
        self.t = 0.0
        self.num_tasks_per_action = num_tasks_per_action

        # Task queues
        self.task_queues = [deque() for _ in list(WorkModes)]
        self.num_work_modes = len(self.task_queues)
        
        # Worker state
        self.work_mode = 0
        
        # Schedule
        self.schedule = schedule if schedule else []
        self.schedule_idx = 0
        self._available_tasks = deque()
        
        # Define action and observation space
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete([self.num_work_modes] * self.num_tasks_per_action)
        
        # Example for using image as input:
        # self.observation_space = spaces.Discrete(5)  # Example, need to define properly

    @property
    def available_tasks(self):
        while (self.schedule_idx < len(self.schedule)) and (len(self._available_tasks) < self.num_tasks_per_action):
            if self.schedule[self.schedule_idx].release_time <= self.t:
                self._available_tasks.append(self.schedule[self.schedule_idx])
                self.schedule_idx += 1
            else:
                break
        return self._available_tasks
        
    def step(self, action):
        reward = 0.0

        # Queue tasks based on action
        for i in range(len(action)):
            if self.available_tasks:
                task = self.available_tasks.popleft()
                task.time_left = task.base_duration * self._task_worker_score(task.task_type.value, action[i])
                # print(f"\n[TASK STARTED]: Work Mode: {WorkModes(action[i]).name}, Task Type = {task.task_type}, Time Left: {task.time_left}, Score: {self._task_worker_score(task.task_type.value, action[i])}\n")
                self.task_queues[action[i]].append(task)
        
        done = (self.schedule_idx >= len(self.schedule)) and len(self.available_tasks) == 0 and all([(len(q) == 0) for q in self.task_queues])
        while len(self.available_tasks) == 0:
            
            # Time budget for this step
            self.end_time = self.t + 1.0

            # Process tasks in the current worker mode
            while self.task_queues[self.work_mode]:
                task = self.task_queues[self.work_mode].popleft()
                if self.t + task.time_left <= self.end_time:
                    # print(f"\n[TASK DONE]: Work Mode = {WorkModes(self.work_mode).name}, Completion Time: {self.t + task.time_left}, Release Time: {task.release_time}\n")
                    delay_factor = (self.t + task.time_left - task.release_time) / (self.mode_switch_frequency * self.num_work_modes)
                    reward += task.reward * (0.99 ** delay_factor)
                    self.t += task.time_left
                else:
                    task.time_left -= self.end_time - self.t
                    self.task_queues[self.work_mode].appendleft(task)
                    break
            
            # Increment current time
            self.t = self.end_time

            if self.t % self.mode_switch_frequency == 0.0:
                self.work_mode += 1
                self.work_mode = self.work_mode % self.num_work_modes

            # Check if done
            done = (self.schedule_idx >= len(self.schedule)) and len(self.available_tasks) == 0 and all([(len(q) == 0) for q in self.task_queues])
            if done:
                break
        
        return self._state(), reward, done, {}
    
    def reset(self):
        self.t = 0.0
        self.task_queues = [deque() for _ in list(WorkModes)]
        self.work_mode = 0
        self.schedule_idx = 0
        self._available_tasks = deque()
        for task in self.schedule:
            task.time_left = None
        return self._state()
    
    def render(self, mode='human', close=False):
        print(f"Work Mode: {WorkModes(self.work_mode).name}")
        print(f"Task queues:")
        for i, q in enumerate(self.task_queues):
            print(f"\t- Worker {WorkModes(i).name}: Time = {sum([task.time_left for task in q])}, Next Reward = {q[0].reward if q else 0.0}")
        
        print(f"Available tasks:")
        for task in self.available_tasks:
            print(f"\t- Task({task.task_type}, {task.base_duration}, {task.reward})")
        print(f"Schedule Index: {self.schedule_idx} / {len(self.schedule)}")
        print(f"Time: {self.t}")
    
    def _state(self):
        task_state = []
        available_tasks_idx = 0
        while len(task_state) < self.num_tasks_per_action:
            if available_tasks_idx < len(self.available_tasks):
                task = self.available_tasks[available_tasks_idx]
                task_state.append(task)
                available_tasks_idx += 1
            else:
                task_state.append(None)
        return self.t, task_state, [sum([task.time_left for task in q]) for q in self.task_queues]
    
    def _task_worker_score(self, task_type: int, work_mode: int):
        return 1 - SCORE_TABLE[task_type][work_mode]
    
def simulation(verbose=False):
    schedule = [
        Task(TaskTypes.SCHOOL, 0.0, 1, 100.0),
        Task(TaskTypes.WORK, 0.0, 2, 200.0),
        Task(TaskTypes.HOBBY, 0.0, 3, 50.0),
    ]
    env = TaskEnv(schedule=schedule)
    observation = env.reset()
    done = False
    if verbose:
        print("Starting simulation ...")
        print("-" * 50)
        env.render()
        print(f"Observation: {observation}")
        print("-" * 50)
    total_reward = 0.0
    action_history = []
    while not done:
        action = env.action_space.sample()
        action_history.append(action[0])
        # action = [1, 0, 2]
        observation, reward, done, _ = env.step(action)
        if verbose:
            print(f"Action: {action}")
            env.render()
            print(f"Observation: {observation}")
            print(f"Reward: {reward}")
            print(f"Done: {done}")
            print("-" * 50)
        total_reward += reward

    env.close()
    if verbose:
        print("Simulation done.")
        print(f"Total Reward: {total_reward}")
    return total_reward, {"actions": action_history, "final_observation": observation}

if __name__ == "__main__":
    num_simulations = 50000
    rewards = []
    simulation_lengths = []
    best_info, worst_info = None, None
    for i in range(num_simulations):
        if (i + 1) % 1000 == 0:
            print(f"Simulation {i + 1} / {num_simulations}")
        r, info = simulation()
        rewards.append(r)
        simulation_lengths.append(info["final_observation"][0])
        if r == max(rewards):
            best_info = info
        if r == min(rewards):
            worst_info = info
    print(best_info, max(rewards))
    print(worst_info, min(rewards))
    print(sum(rewards) / num_simulations)
    print(sum(simulation_lengths) / num_simulations)

    # Plot histogram
    plt.clf()
    plt.hist(rewards, bins=20)
    plt.xlabel('Reward')
    plt.ylabel('Frequency')
    plt.title('Reward Distribution')
    plt.savefig('reward_distribution.png')

    # Plot histogram
    plt.clf()
    plt.hist(simulation_lengths, bins=20)
    plt.xlabel('Simulation Length')
    plt.ylabel('Frequency')
    plt.title('Simulation Length Distribution')
    plt.savefig('simulation_length_distribution.png')

    # simulation(verbose=True)
    


        
    
   
