from environment import TaskType, Task, Worker

class MLTaskType(TaskType):
    DATA_PREPROCESSING = 1
    MODEL_TRAINING = 2
    MODEL_EVALUATION = 3

class MLTask(Task):
    def __init__(self, task_type: MLTaskType, base_duration: float):
        super().__init__(task_type, base_duration)

    def task_time(self, skill: float) -> float:
        if skill < 0:
            raise ValueError("Skill level must be at least 0")
        
        return self.base_duration * (10 ** (-skill))

    def __repr__(self):
        return f"<MLTask(type={self.task_type}, base_duration={self.base_duration}, completed={self.completed})>"
    
class MLWorker(Worker):
    def __init__(self, skill_map: dict):
        super().__init__(skill_map)

    def calculate_task_time(self, task: MLTask) -> float:
        skill = self.skill_map.get(task.task_type, self.DEFAULT_SKILL)
        return task.task_time(skill)

    def __repr__(self):
        return f"<MLWorker(skill_map={self.skill_map}, tasks={list(self.tasks)})>"
    

def test1():
    preprocessing = MLTask(MLTaskType.DATA_PREPROCESSING, 1e6)
    training = MLTask(MLTaskType.MODEL_TRAINING, 1e8)
    evaluation = MLTask(MLTaskType.MODEL_EVALUATION, 50)

    #Create 3 workers. 
    # One which is extremely good at matrix operations meaning it is best at model evaluation, and it is ok at model training but it is terrible at data preprocessing, 
    # one which is hyper optimized for model training but is terrible at data preprocerssing and ok at model evlaution. 
    # The final worker should be super good at data preprocessing (i.e. a scientific computer with a lot of numerical tricks built in for preprocessing) but is terrible at both model evluation and model training

    lpu = MLWorker({MLTaskType.DATA_PREPROCESSING: 0, MLTaskType.MODEL_TRAINING: 2, MLTaskType.MODEL_EVALUATION: 4})
    gpu = MLWorker({MLTaskType.DATA_PREPROCESSING: 0, MLTaskType.MODEL_TRAINING: 3, MLTaskType.MODEL_EVALUATION: 10})
    cpu = MLWorker({MLTaskType.DATA_PREPROCESSING: 1, MLTaskType.MODEL_TRAINING: 0, MLTaskType.MODEL_EVALUATION: 0})


