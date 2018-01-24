from unittest import TestCase
from lib.agent import Agent
from lib.model import Model
from lib.time import SimultaneousActivation
from lib.space import Grid
from swarms.sbehaviors import (
    GoTo, RandomWalk,
    Move
    )
from swarms.objects import Sites
import py_trees
import numpy as np


# Class to tets GoTo behavior for agents
class SwarmAgentGoTo(Agent):
    """ An minimalistic behavior tree for swarm agent implementing goto behavior"""
    def __init__(self, name, model):
        super().__init__(name, model)
        self.location = ()

        self.direction = model.random.rand() * (2 * np.pi)
        self.speed = 2
        self.radius = 3

        root = py_trees.composites.Sequence("Sequence")
        low = GoTo('1')
        low.setup(0, self, model.target)
        high = Move('2')
        high.setup(0, self)
        root.add_children([low, high])
        self.behaviour_tree = py_trees.trees.BehaviourTree(root)

    def step(self):
        self.behaviour_tree.tick()

    def advance(self):
        pass


# class to test random walk behavior
class SwarmAgentRandomWalk(Agent):
    """ An minimalistic behavior tree for swarm agent implementing Random walk"""
    def __init__(self, name, model):
        super().__init__(name, model)
        self.wealth = 1
        self.location = ()

        self.direction = model.random.rand() * (2 * np.pi)
        self.speed = 2
        self.radius = 3

        root = py_trees.composites.Sequence("Sequence")
        low = RandomWalk('1')
        low.setup(0, self)
        high = Move('2')
        high.setup(0, self)
        root.add_children([low, high])
        self.behaviour_tree = py_trees.trees.BehaviourTree(root)

    def step(self):
        self.behaviour_tree.tick()

    def advance(self):
        pass


class GoToSwarmEnvironmentModel(Model):
    """ A environemnt to model swarms """
    def __init__(self, N, width, height, grid=10, seed=None):
        if seed is None:
            super(GoToSwarmEnvironmentModel, self).__init__(seed=None)
        else:
            super(GoToSwarmEnvironmentModel, self).__init__(seed)

        self.num_agents = N

        self.grid = Grid(width, height, grid)

        self.schedule = SimultaneousActivation(self)
        
        self.target = Sites(id=1, location=(45, 45), radius=5, q_value=0.5)

        for i in range(self.num_agents):
            a = SwarmAgentGoTo(i, self)
            self.schedule.add(a)
            x = -45
            y = -45
            a.location = (x, y)
            a.direction = -2.3561944901923448
            self.grid.add_object_to_grid((x, y), a)

        self.agent = a

    def step(self):
        self.schedule.step()


class RandomWalkSwarmEnvironmentModel(Model):
    """ A environemnt to model swarms """
    def __init__(self, N, width, height, grid=10, seed=None):
        if seed is None:
            super(RandomWalkSwarmEnvironmentModel, self).__init__(seed=None)
        else:
            super(RandomWalkSwarmEnvironmentModel, self).__init__(seed)

        self.num_agents = N

        self.grid = Grid(width, height, grid)

        self.schedule = SimultaneousActivation(self)
        
        self.target = Sites(id=1, location=(45, 45), radius=5, q_value=0.5)

        for i in range(self.num_agents):
            a = SwarmAgentRandomWalk(i, self)
            self.schedule.add(a)
            x = -45
            y = -45
            a.location = (x, y)
            a.direction = -2.3561944901923448
            self.grid.add_object_to_grid((x, y), a)

        self.agent = a

    def step(self):
        self.schedule.step()


class TestGoToSwarmSmallGrid(TestCase):
    
    def setUp(self):
        self.environment = GoToSwarmEnvironmentModel(1, 100, 100, 10, 123)
        # Set up behaviors trees

        # print(self.environment.agent.behaviour_tree.tick())
        for i in range(50):
            self.environment.step()

    def test_agent_path(self):
        self.assertEqual(self.environment.agent.location, (27, 27))


class TestRandomWalkSwarmSmallGrid(TestCase):
    
    def setUp(self):
        self.environment = RandomWalkSwarmEnvironmentModel(1, 100, 100, 10, 123)
        # Set up behaviors trees

        # print(self.environment.agent.behaviour_tree.tick())
        for i in range(50):
            print(self.environment.agent.location)
            self.environment.step()

    def test_agent_path(self):
        self.assertEqual(self.environment.agent.location, (27, 27))        

