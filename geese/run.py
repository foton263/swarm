from swarms.model import EnvironmentModel
from swarms.agent import SwarmAgent

import argparse

import os, sys

## Global variables for width and height
width = 1600
height = 800

def main():
    
    env = EnvironmentModel(100, width, height, 10)

    #exit()
    for i in range(1000):
        env.step()

    for agent in env.schedule.agents:
        print (agent.name, agent.wealth)

if __name__ == '__main__':
    main()