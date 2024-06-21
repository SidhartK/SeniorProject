# SeniorProject

Experiments:

1. The first experiment should be a sanity check that this works. I want to set up the environment in a way that 
beating the game means getting the lowest mean finish time. 

Initially, I think I should treat it like a classification problem. What this means is that I assume 
there is an infinite supply of wokrers of each type and thus the entire objective of the scheduler 
is just to correctly assign the task to the correct type of worker

The task embedding will just end up being some sort of vector 
The entire point of embedding in some d-dimensional space is that I don't have to know how many different 
types of tasks there are and I can introduce a new task type easily

Technically, we could calculate an empirical time to complete task based on task type and thus construct a |W|
dimensional embedding for each task. That solution would work out of the box and might actually means we 
don't need to do this experiment. 

2. The follow up experiment to this would then be to frame this more as an RL task by limiting the number of workers 
of each type. Now technically the environment could be solved by having the same task embeddings as described above 
but then also accounting for the amount of time until a worker of that type is free. 

Each time step corresponds to assigning a new task in the stream. We can create queues for each type of worker and 
then we have a slightly brittle system where you can assign a task to a particular type of worker and that's it. 
You can't affect the queue order at all after assigning a task there

But could also consider a min heap structure that is geared towards the mean finish time (MFT) metric objective. Where the queue actually just pops the task that will be completed in the last amount of time (i.e. all tasks have equal priority).
The only issue is then the scheduler would need to know about the amount of time that is left in the queue when making a 
decision. 

We can get around that by passing quartile information about the values to the scheduler as a model in the heap 

So this means that the scheduler will have two iterations:
1. Scheduler that is super simple and just takes in knowledge about how fast a particular worker class is on a task type. This can be done really simply by just creating a vector that takes in the amount of 

- I could also set the neural network directly which could be one way to test that it works 
- Then try it where the neural network learns

2. Now we can do it where the 

- 

## Steps To Completion










