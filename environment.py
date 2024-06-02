from enum import Enum
from collections import deque
from typing import Dict
import numpy as np
import heapq

class TaskType(Enum):
    pass

class Task:
    def __init__(self, task_type: TaskType, base_duration: float, dependencies: list = []):
        self._completed = False
        self.task_type = task_type
        self.base_duration = base_duration
        self.dependencies = dependencies

    @property
    def completed(self):
        return self._completed
    
    @completed.setter
    def completed(self, value):
        if value:
            if not self.dependencies_completed:
                raise ValueError("Cannot complete task until all dependencies are completed")
        self._completed = value

    @property
    def dependencies_completed(self):
        return all([task.completed for task in self.dependencies])

    def compute_task_time(self, skill: float) -> float:
        if skill < 0:
            raise ValueError("Skill level must be at least 0")
        return self.base_duration * (2 ** (-skill))

    def __repr__(self):
        return f"<Task(type={self.task_type}, base_duration={self.base_duration}, completed={self.completed})>"

class WorkerType(Enum):
    pass

class Worker:
    DEFAULT_SKILL = 0.0

    def __init__(self, skill_map: Dict[TaskType, float], save_history=False):
        self.tasks = deque()
        self.skill_map = skill_map
        self.history = [] if save_history else None

    @property
    def can_add_task(self):
        for task in self.tasks:
            if task.completed:
                self.tasks.popleft()
            else:
                break

        return not self.tasks

    def add_task(self, task: Task):
        self.tasks.append(task)

    def complete_next_task(self):
        if self.tasks:
            task = self.tasks[0]
            if task.dependencies_completed:
                task.completed = True
                if self.history is not None:
                    self.history.append(task)
                self.tasks.popleft()
            return task
        return None

    def compute_task_time(self, task: Task) -> float:
        skill = self.skill_map.get(task.task_type, self.DEFAULT_SKILL) 
        return task.compute_task_time(skill)

    def __repr__(self):
        return f"<Worker(skill_map={self.skill_map}, tasks={list(self.tasks)})>"


def run_simulation(workers: list[Worker], task_list: list[Task], scheduler, verbose=False):
    if verbose:
        for i, worker in enumerate(workers):
            print(i, ": ", worker)
            for task in worker.tasks:
                print(f"\t{task}")

    jobs = []
    task_list = []
    t = 0
    while True:
        if all([task.completed for worker in workers for task in worker.tasks]):
            break

        for i, worker in enumerate(workers):
            if worker.tasks:
                task = worker.tasks[0]
                if task.dependencies_completed:
                    heapq.heappush(jobs, (t + worker.compute_task_time(task), (len(task_list), i)))
                    task_list.append(task)
                    worker.tasks.popleft()
        
        if jobs:
            t, (task_idx, worker_idx) = heapq.heappop(jobs)
            task, worker = task_list[task_idx], workers[worker_idx]
            task.completed = True
            if verbose:
                print(f"Task {task.task_type} completed by Worker {worker}")
                print("Time t =", t)
    
    if verbose:
        print("Simulation complete at time t =", t)

    return t

    

# Example usage
# if __name__ == "__main__":
#     class SMTTaskType(TaskType):
#         GRADING = 1
#         RUNNING = 2
#         PROCTORING = 3


#     # Create a task to run the tests to each of the individual rooms each of equal distance. There are 3 tests to run so create 3 tasks.
#     task1 = Task(SMTTaskType.RUNNING, 100)
#     task2 = Task(SMTTaskType.RUNNING, 100)
#     task3 = Task(SMTTaskType.RUNNING, 100)

#     # Create a 3 proctoring tasks with the same amount of time needed to complete each task. But the proctoring tasks are dependent on the running tasks.
#     proctor1 = Task(SMTTaskType.PROCTORING, 100, [task1])
#     proctor2 = Task(SMTTaskType.PROCTORING, 100, [task2])
#     proctor3 = Task(SMTTaskType.PROCTORING, 200, [task3])

#     # Create 3 grading tasks with the same amount of time needed to complete each task. But the grading tasks are dependent on the proctoring tasks.
#     grading1 = Task(SMTTaskType.GRADING, 100, [proctor1])
#     grading2 = Task(SMTTaskType.GRADING, 100, [proctor2])
#     grading3 = Task(SMTTaskType.GRADING, 150, [proctor3])

    
#     # Create 3 workers. One is extremely fast in running but slow at grading and proctoring. The second is extremely fast at grading but slow at running and proctoring. The third is extremely fast at proctoring but slow at running and grading.
#     class SMTRunner(Worker):
#         DEFAULT_SKILL_MAP = {SMTTaskType.RUNNING: 1, SMTTaskType.PROCTORING: 0, SMTTaskType.GRADING: 0}
#         def __init__(self, skill_map: dict = DEFAULT_SKILL_MAP):
#             super().__init__(skill_map)

#     class SMTGrader(Worker):
#         DEFAULT_SKILL_MAP = {SMTTaskType.RUNNING: 0, SMTTaskType.PROCTORING: 0, SMTTaskType.GRADING: 2}
#         def __init__(self, skill_map: dict = DEFAULT_SKILL_MAP):
#             super().__init__(skill_map)

#     class SMTProctor(Worker):
#         DEFAULT_SKILL_MAP = {SMTTaskType.RUNNING: 0, SMTTaskType.PROCTORING: 0.5, SMTTaskType.GRADING: 1}
#         def __init__(self, skill_map: dict = DEFAULT_SKILL_MAP):
#             super().__init__(skill_map)

#     # Create a pool of workers: 2 runners, 2 graders, and 2 proctors 
#     workers = [SMTRunner(), SMTRunner(), SMTGrader(), SMTGrader(), SMTProctor(), SMTProctor()]

#     # Assign the tasks to the workers randomly
#     all_tasks = [task1, task2, task3, proctor1, proctor2, proctor3, grading1, grading2, grading3]
#     for task in all_tasks:
#         np.random.choice(workers).add_task(task)

#     for worker in workers:
#         print(worker)

#     t = 0
#     tmax = 20

#     while t < tmax:
#         print("\n\nTime t = ", t)
#         for i, worker in enumerate(workers):
#             task = worker.complete_next_task()
#             if task is not None:
#                 if task.completed:
#                     print(f"Task {task.task_type} completed by Worker {i}")
#                 else:
#                     print(f"Task {task.task_type} attempted by Worker {i}")
#             else:
#                 print(f"Worker {i} has no tasks to complete")
#         if all([task.completed for task in all_tasks]):
#             break
#         t += 1

#     print("Simulation complete at time t = ", t)
    
    



