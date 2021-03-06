[image1]: https://user-images.githubusercontent.com/10624937/42135623-e770e354-7d12-11e8-998d-29fc74429ca2.gif "Trained Agent"
[image2]: https://user-images.githubusercontent.com/10624937/42135622-e55fb586-7d12-11e8-8a54-3c31da15a90a.gif "Soccer"


# Project 3: Collaboration and Competition

### Introduction

For this project, you will work with the [Tennis](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Learning-Environment-Examples.md#tennis) environment.

![Trained Agent][image1]

In this environment, two agents control rackets to bounce a ball over a net. If an agent hits the ball over the net, it receives a reward of +0.1.  If an agent lets a ball hit the ground or hits the ball out of bounds, it receives a reward of -0.01.  Thus, the goal of each agent is to keep the ball in play.

The observation space consists of 8 variables corresponding to the position and velocity of the ball and racket. Each agent receives its own, local observation.  Two continuous actions are available, corresponding to movement toward (or away from) the net, and jumping. 

The task is episodic, and in order to solve the environment, your agents must get an average score of +0.5 (over 100 consecutive episodes, after taking the maximum over both agents). Specifically,

- After each episode, we add up the rewards that each agent received (without discounting), to get a score for each agent. This yields 2 (potentially different) scores. We then take the maximum of these 2 scores.
- This yields a single **score** for each episode.

The environment is considered solved, when the average (over 100 episodes) of those **scores** is at least +0.5.

### Getting Started

1. Download the environment from one of the links below.  You need only select the environment that matches your operating system:
    - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P3/Tennis/Tennis_Linux.zip)
    
    
### Instructions
1. Clone the repository and navigate to the downloaded folder.
```	
     git clone https://github.com/ChrisProgramming2018/DeepReinforcementLearningProjects.git
     cd DeepReinforcementLearningProjects
```	
2. Create a virtual enviroment 
```	
     virtualenv -p python3 p3_collab-compet
```
3. Activate the Enviroment
```
	source p3_collab-compet/bin/activate
	cd p3_collab-compet
```

4.  **Install all dependencies**, use the requirements.txt file

```
	pip3 install -r requirements.txt
```
5.  Download the environment for linux 
```
	click on the link
```
```
     download it to the same folder p3_collab-compet
     unzip Tennis_Linux.zip
     rm Tennis_Linux.zip
```
6.  Use  different  hyper parameter values to find the best 
```
	python3  hyperparametersearch.py
```
7. Train agent with the "best" hyper parameter   
```
	python3  main.py
```
8. Watch smart agent (load trained network weights) in the environment collecting the yellows bananas   
```
	python3 watch_smart_agents.py
```
9. Issues
    In case of any problem check if the correct parameters are set and the pathnames are correct
