# Copyright 2020
# Author: Christian Leininger <info2016frei@gmail.com>
 
import time
import random
from datetime import datetime
import numpy as np
import os
from collections import deque
from torch.utils.tensorboard import SummaryWriter
import torch 
from agent_average_v1 import TD31v1
from memory import ReplayBuffer
from unityagents import UnityEnvironment


def createstate(state):
    all_states = np.array([])
    for key  in state.keys():
        all_states = np.concatenate((all_states, state[key]))
    return all_states




def mkdir(base, name):
    """
    Creates a direction if its not exist
    Args:
       param1(string): base first part of pathname
       param2(string): name second part of pathname
    Return: pathname 
    """
    path = os.path.join(base, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def evaluate_policy(policy, writer, total_timesteps, args, episode = 1):
    """
    
    
    Args:
       param1(): policy
       param2(): writer
       param3(): episode default 1 number for path to save the video
    """
    use_gym = False
    # env_e = wrappers.Monitor(env, monitor_dir, force = True)
    avg_reward = 0.
    seeds = [x for x in range(10)]
    for s in seeds:
        if use_gym:
            env.seed(s)
            obs = env.reset()
            done = False
        else:
            obs, done = env.reset(), False

        while not done:
            if not use_gym:
                obs = createstate(obs)
            action = policy.select_action(np.array(obs))
            obs, reward, done, _ = env.step(action)
            avg_reward += reward * args.reward_scalling
    avg_reward /= len(seeds)
    writer.add_scalar('Evaluation reward', avg_reward, total_timesteps)
    print ("---------------------------------------")
    print ("Average Reward over the Evaluation Step: %f" % (avg_reward))
    print ("---------------------------------------")
    return avg_reward




def write_into_file(pathname, text):
    """
    """
    with open(pathname+".txt", "a") as myfile:
        myfile.write(text)
        myfile.write('\n')

def time_format(sec):
    """
    
    Args:
        param1():

    """
    hours = sec // 3600
    rem = sec - hours * 3600
    mins = rem // 60
    secs = rem - mins * 60
    return hours, mins, round(secs,2)



def train(args, repeat_opt):
    """

    Args:
        param1(TD3): policy
        param2(Buffer):
        param3(openai env):
    """
    use_gym = False
    # in case seed experements
    args.seed = repeat_opt
    now = datetime.now()    
    dt_string = now.strftime("%d_%m_%Y_%H:%M:%S")
    #args.repeat_opt = repeat_opt
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    pathname = 'env-' + str(args.env_name) + '_update_freq: ' + str(args.target_update_freq) + "num_q_target_" + str(args.num_q_target) + "_seed_" + str(args.seed)
    text = "Star_training target_update_freq: {}  num_q_target: {}  use device {} ".format(args.target_update_freq, args.num_q_target, args.device)
    print(pathname, text)
    write_into_file('search-' + pathname, text) 
    arg_text = str(args)
    write_into_file('search-' + pathname, arg_text) 
    # tensorboard_name = 'runs' + str(dt_string) + '/' + pathname + "-Dueling"
    tensorboard_name = 'runs/' + pathname 
    writer = SummaryWriter(tensorboard_name)
    env = UnityEnvironment(file_name='Reacher_Linux/Reacher.x86_64',no_graphics=True)
    # get the default brain
    brain_name = env.brain_names[0]
    brain = env.brains[brain_name]
    # reset the environment
    env_info = env.reset(train_mode=True)[brain_name]
    # number of agents
    num_agents = len(env_info.agents)
    print('Number of agents:', num_agents)
    # size of each action
    action_dim = brain.vector_action_space_size
    states = env_info.vector_observations
    state_dim = states.shape[1]
    max_action = 1
    policy = TD31v1(state_dim, action_dim, max_action, args)
    replay_buffer = ReplayBuffer()
    save_env_vid = False
    total_timesteps = 0
    timesteps_since_eval = 0
    episode_num = 0
    done = True
    t0 = time.time()
    scores_window = deque(maxlen=100) 
    episode_reward = 0
    evaluations = []
    file_name = "%s_%s_%s" % ("TD3", args.env_name, str(args.seed))
    print ("---------------------------------------")
    print ("Settings: %s" % (file_name))
    print ("---------------------------------------")
    # We start the main loop over 500,000 timesteps
    tb_update_counter = 0
    while total_timesteps <  args.max_timesteps:
        tb_update_counter += 1
        # If the episode is done
        if done:
            episode_num += 1
            #env.seed(random.randint(0, 100))
            scores_window.append(episode_reward)
            average_mean = np.mean(scores_window)
            if tb_update_counter > args.tensorboard_freq:
                print("Write tensorboard")
                tb_update_counter = 0
                writer.add_scalar('Reward', episode_reward, total_timesteps)
                writer.add_scalar('Reward mean ', average_mean, total_timesteps)
            # If we are not at the very beginning, we start the training process of the model
            if total_timesteps != 0:
                text = "Total Timesteps: {} Episode Num: {} ".format(total_timesteps, episode_num) 
                text += "Episode steps {} ".format(episode_timesteps)
                text += "Reward: {}  Average Re: {:.2f} Time: {}".format(episode_reward, np.mean(scores_window), time_format(time.time()-t0))
                
                print(text)
                write_into_file('search-' + pathname, text)
                policy.train(replay_buffer, writer, episode_timesteps)
            # We evaluate the episode and we save the policy
            if timesteps_since_eval >= args.eval_freq:
                policy.save("%s" % (file_name), directory="./pytorch_models")
                timesteps_since_eval %= args.eval_freq
                #evaluations.append(evaluate_policy(policy, writer, total_timesteps, args, episode_num))
                save_model = file_name + '-{}'.format(episode_num)
                policy.save(save_model, directory="./pytorch_models")
                np.save("./results/%s" % (file_name), evaluations)
            # When the training step is done, we reset the state of the environment
            env_info = env.reset(train_mode=True)[brain_name]
            obs = env_info.vector_observations[0] 

            # Set the Done to False
            done = False
            # Set rewards and episode timesteps to zero
            episode_reward = 0
            episode_timesteps = 0
        # Before 10000 timesteps, we play random actions
        if total_timesteps < args.start_timesteps:
            action = np.random.randn(brain.vector_action_space_size)
        else:
            action = policy.select_action(np.array(obs))
            # If the explore_noise parameter is not 0, we add noise to the action and we clip it
            if args.expl_noise != 0:
                action = (action + np.random.normal(0, args.expl_noise, size=action_dim)).clip(-1,1)
            else:
                action = ( policy.select_action(np.array(obs)) + np.random.normal(0, max_action * args.expl_noise, size=action_dim)).clip(-max_action, max_action)

        
        if total_timesteps % args.target_update_freq == 0:
            policy.hardupdate()
        # The agent performs the action in the environment, then reaches the next state and receives the reward
        env_info = env.step(action)[brain_name]           # send all actions to tne environment
        new_obs = env_info.vector_observations[0]         # get next state (for each agent)
        reward = env_info.rewards[0]                         # get reward (for each agent)
        done = env_info.local_done[0]
        # We check if the episode is done
        #done_bool = 0 if episode_timesteps + 1 == env._max_episode_steps else float(done)
        done_bool = 0 if episode_timesteps + 1 == args.max_episode_steps else float(done)
        # We increase the total reward
        reward = reward * args.reward_scalling
        
        episode_reward += reward
        # We store the new transition into the Experience Replay memory (ReplayBuffer)
        replay_buffer.add((obs, new_obs, action, reward, done_bool))
        # We update the state, the episode timestep, the total timesteps, and the timesteps since the evaluation of the policy
        obs = new_obs
        
        episode_timesteps += 1
        total_timesteps += 1
        timesteps_since_eval += 1


    # We add the last policy evaluation to our list of evaluations and we save our model
    if args.save_model: policy.save("%s" % (file_name), directory="./pytorch_models")
    np.save("./results/%s" % (file_name), evaluations)

