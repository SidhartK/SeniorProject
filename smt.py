from task import TaskType, Task, WorkerType, Worker, run_simulation
import numpy as np

class SMTTaskType(TaskType):
    RUNNING = 1
    PROCTORING = 2
    GRADING = 3
    

class SMTWorkerType(WorkerType):
    RUNNER = 1
    PROCTOR = 2
    GRADER = 3
    

class SMTRunner(Worker):
    DEFAULT_SKILL_MAP = {
        SMTTaskType.RUNNING: 1, 
        SMTTaskType.PROCTORING: 0, 
        SMTTaskType.GRADING: 0
    }
    def __init__(self, skill_map: dict = DEFAULT_SKILL_MAP):
        super().__init__(skill_map)

    def __repr__(self):
        return f"<SMTRunner>"
    
class SMTProctor(Worker):
    DEFAULT_SKILL_MAP = {
        SMTTaskType.RUNNING: 0, 
        SMTTaskType.PROCTORING: 0.5, 
        SMTTaskType.GRADING: 0.5
    }
    def __init__(self, skill_map: dict = DEFAULT_SKILL_MAP):
        super().__init__(skill_map)

    def __repr__(self):
        return f"<SMTProctor>"

class SMTGrader(Worker):
    DEFAULT_SKILL_MAP = {
        SMTTaskType.RUNNING: 0, 
        SMTTaskType.PROCTORING: 0, 
        SMTTaskType.GRADING: 1
    }
    def __init__(self, skill_map: dict = DEFAULT_SKILL_MAP):
        super().__init__(skill_map)

    def __repr__(self):
        return f"<SMTProctor>"
    
def smt_setup():
    """
    Create 3 tests that need to be ran to their rooms, proctored and then graded. 
    Create 6 workers: 2 runners, 2 graders, and 2 proctors.
    Assign the tasks to the workers randomly.
    """

    task1 = Task(SMTTaskType.RUNNING, 100)
    task2 = Task(SMTTaskType.RUNNING, 100)
    task3 = Task(SMTTaskType.RUNNING, 100)

    # Create a 3 proctoring tasks with the same amount of time needed to complete each task. But the proctoring tasks are dependent on the running tasks.
    proctor1 = Task(SMTTaskType.PROCTORING, 100, [task1])
    proctor2 = Task(SMTTaskType.PROCTORING, 100, [task2])
    proctor3 = Task(SMTTaskType.PROCTORING, 200, [task3])

    # Create 3 grading tasks with the same amount of time needed to complete each task. But the grading tasks are dependent on the proctoring tasks.
    grading1 = Task(SMTTaskType.GRADING, 100, [proctor1])
    grading2 = Task(SMTTaskType.GRADING, 100, [proctor2])
    grading3 = Task(SMTTaskType.GRADING, 150, [proctor3])

    # Assign the tasks to the workers randomly
    task_list = [task1, task2, task3, proctor1, proctor2, proctor3, grading1, grading2, grading3]


    # Create a pool of workers: 2 runners, 2 graders, and 2 proctors 
    workers = [SMTRunner(), SMTRunner(), SMTProctor(), SMTProctor(), SMTGrader(), SMTGrader()]

    return task_list, workers


def random_strat(verbose=False):
    all_tasks, workers = smt_setup()

    for task in all_tasks:
        np.random.choice(workers).add_task(task)

    if verbose:
        for i, worker in enumerate(workers):
            print(i, ": ", worker)
            for task in worker.tasks:
                print(f"\t{task}")

    run_simulation(workers, verbose=verbose)

def oracle_scheduler(workers, task):
    """
    Assign tasks to workers in a way that minimizes the total time to complete all tasks.
    """
    for worker in workers:
        if worker.can_add_task(task):
            worker.add_task(task)
            return


def oracle_strat(verbose=False):
    all_tasks, workers = smt_setup()
    for task in all_tasks:
        print(task)

    workers[0].add_task(all_tasks[0])
    workers[1].add_task(all_tasks[1])
    workers[5].add_task(all_tasks[2])
    workers[0].add_task(all_tasks[3])
    workers[2].add_task(all_tasks[4])
    workers[3].add_task(all_tasks[5])
    workers[4].add_task(all_tasks[6])
    workers[2].add_task(all_tasks[7])
    workers[5].add_task(all_tasks[8])


    run_simulation(workers, verbose=verbose)

if __name__ == "__main__":
    random_strat(verbose=True)
    print("\n\n", "-"*50, "\n\n")
    oracle_strat(verbose=True)

    
    

# If the power wants 10 power graders
# interface where person assigning tasks can 10 graders

# would expect proctors to be in room (ideally) before runners get tests there 
# proctors still in the room but runners grab tests and run them back to the grading room
# graders have to be different people

# want proctors to be grading (during grading crunch) while they are proctoring 
# normal grading done before tie breakers start
# tie breakers need to happen and be graded before they finish award slides
# award slide before ceremony

# room dependencies (if a test is being proctored in a room then room can't be used)


