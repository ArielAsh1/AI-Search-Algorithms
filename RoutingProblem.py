
from ways.info import SPEED_RANGES

'creates a new routing problem for USC and A* algorithms'

class Routing_Problem:
    def __init__(self, roads, s_start, s_goal):
        self.s_start = s_start
        self.goal = s_goal
        self.roads = roads

    def actions(self, s):
        junc = self.roads[s]
        return junc.links

    def is_goal(self, s):
        return s == self.goal

    def succ(self, source, a):
        return a.target

    def step_cost(self, source, link):
        # divide by 1000 cause speed in km/minute and distance is meters
        return (link.distance / 1000) / SPEED_RANGES[link.highway_type][1]
