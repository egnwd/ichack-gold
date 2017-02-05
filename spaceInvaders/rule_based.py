import argparse
import logging
import sys

import numpy as np
import gym
from gym import wrappers


class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

def isPink(cell):
    correctRed = cell[0] == 200
    correctGreen = cell[1] == 72
    correctBlue = cell[2] == 72
    return correctRed and correctGreen and correctBlue
    
def findBall(ob):
    for i in range(210):
        for j in range(160):
            if isPink(ob[i][j]):
                if not isPink(ob[i][j-2]):
                    if not isPink(ob[i][j+2]):
                        return i, j
                        #if i >= 56 and i <= 64:
                         #   if (not (isPink(ob[i][j - 2]))) and (not (isPink(ob[i][j + 2]))):
                          #       return i, j
                           #      print fail
    return 0, 0

def findPaddle(ob):
    for i in range(40):
        for j in range(8, 151):
            if isPink(ob[210 - i - 1][j]):
                if isPink(ob[210 - i - 1][j + 6]):
                    if isPink(ob[210 - i - 1][j -6]):
#                        print "Found the paddle at (i, j, k): (" + str(210 - i - 1) + ", " + str(j) + ")"
                        return 210 - i - 1, j + 1
    return 0, 0


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', nargs='?', default='Breakout-v0', help='Select the environment to run')
    args = parser.parse_args()

    gym.scoreboard.api_key = "sk_Kez82tzQoif98qws45z3g"
    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = './dqn/rule_based'
    env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 50
    done = False

    target = open("ob.txt", 'w')
    # set the last positions originally to be in the centre
    right_barrier = 152
    left_barrier = 7
    paddle_barrier = 189
    grid_width = right_barrier - left_barrier
    x_target = -1
    max = 0
    
    for i in range(episode_count):
        ob = env.reset()
        last_paddle_i, last_paddle_j = 189, 42
        last_ball_i, last_ball_j = 5, 80
        ball_going_down = True
        num_renders = 0
        while True:
            #action = agent.act(ob, reward, done)
            # find the ball and the paddle
            ball_i, ball_j = findBall(ob)
            if ball_i == ball_j == 0:
                action = 1
                ob, reward, done, _ = env.step(action)
            
            paddle_i, paddle_j = findPaddle(ob)
            ball_going_right = last_ball_j <= ball_j
            if ball_i > last_ball_i:
                ball_going_down = True
            else:
                ball_going_down = False
            if ball_going_down:
                #print "going down"
                dummy_ball_j = ball_j
                dummy_ball_i = ball_i
                diff_i = paddle_barrier - ball_i
                i_speed = dummy_ball_i - last_ball_i
                j_speed = dummy_ball_j - last_ball_j
                if i_speed != 0:
                    to_move = (diff_i * j_speed) / i_speed
                else:
                    to_move = 0
                if not ball_going_right:
                    
                    x = ball_j + to_move
                    if x > left_barrier:
                        x_target = x
                    else:
                        diff = ball_j - left_barrier                        
                        dummy_ball_i = diff * i_speed / j_speed
                        dummy_ball_j = left_barrier
                        ball_going_right = True
                        to_move -= diff
                        
                if ball_going_right:
                    x = dummy_ball_j + to_move
                    if x < right_barrier:
                        x_target = x
                    else:
                        num_grids, x_remainder = divmod(x, grid_width)
                        if num_grids % 2 == 0:
                            x_target = left_barrier + x_remainder
                        else:
                            x_target = right_barrier - x_remainder                
                if paddle_j - 5 <= x_target <= paddle_j + 5:
                    action = 0
                elif x_target < paddle_j:
                    action = 3
                elif x_target > paddle_j:
                    action = 2                    
            else:                               
                # The ball is going up so we should go to the centre
                #TODO: Do we need to reset the last positions?
                action = 0
            if ball_i > 145 and ball_i < 175:
                action = 0
            last_ball_i = ball_i
            last_ball_j = ball_j
            
            ob, reward, done, _ = env.step(action)
            if not ball_going_down:
                got_there = False
            #env.render()

            if done:
                if reward > max:
                    max = reward
                    print "The new max is iteration: " + str(i) + "with score: " + str(reward)
                break
            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.

    # Close the env and write monitor result info to disk
    env.close()

    # Upload to the scoreboard. We could also do this from another
    # process if we wanted.
    # gym.upload(outdir)
