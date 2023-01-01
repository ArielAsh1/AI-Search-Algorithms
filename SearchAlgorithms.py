# name: Ariel Ashkenazy
# ID: 208465085

""" this file holds the implementation of the 3 search algorithms."""
from Helper import get_link_time
from bestFirstGraphSearch import best_first_graph_search
from ways import load_map_from_csv, compute_distance
from ways.info import SPEED_RANGES

roads = load_map_from_csv()
MAXIMAL_ROAD_SPEED = 110


def huristic_function(lat1, lon1, lat2, lon2):
    return compute_distance(lat1, lon1, lat2, lon2) / MAXIMAL_ROAD_SPEED


# creates a new routing problem for USC and A* algorithms
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


# calculates path from source to target using UCS Algorithm
def ucs_rout(source, target):
    def f(node): return node.path_cost
    paths = best_first_graph_search(Routing_Problem(roads, source, target), f)
    # converts each link to its source index, and adds target at the end
    path_indices = list(map(lambda link: link.source, paths)) + [target]
    return path_indices


# calculates path from source to target using A* Algorithm
def astar_route(source, target):
    def g(node):
        return node.path_cost
    paths = best_first_graph_search(
        Routing_Problem(roads, source, target),
        f=lambda n: g(n) + huristic_function(roads[n.state].lat, roads[n.state].lon,
                                             roads[target].lat, roads[target].lon))
    # converts each link to its source index, and adds target at the end
    path_indices = list(map(lambda link: link.source, paths)) + [target]
    return path_indices


# inits new_limit to be used globally in idastar algorithm.
new_limit = None


def h(source, target):
    return huristic_function(source.lat, source.lon, target.lat, target.lon)


def DFS_f(source, g, path, f_limit, target):
    global new_limit
    new_f = g + h(source, target)
    if new_f > f_limit:
        new_limit = min(new_limit, new_f)
        return None
    # reached target so return path to here
    if target.index == source.index:
        return path
    for link in source.links:
        next_junc = roads[link.target]
        solution = DFS_f(next_junc, g + get_link_time(link), path + [next_junc.index], f_limit, target)
        if solution is not None:
            return solution
    return None


# calculates path from source to target using IDA* Algorithm
def idastar_route(source, target):
    global new_limit
    target_junc = roads[target]
    source_junc = roads[source]

    new_limit = h(source_junc, target_junc)
    while True:
        f_limit = new_limit
        new_limit = float("inf")
        solution = DFS_f(source_junc, 0, [source], f_limit, target_junc)
        if solution is not None:
            return solution
