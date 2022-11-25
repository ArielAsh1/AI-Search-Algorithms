'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

from bestFirstGraphSearch import best_first_graph_search
from ways.info import SPEED_RANGES
from Helper import get_link_time
from ways import load_map_from_csv, compute_distance
roads = load_map_from_csv()

MAXIMAL_ROAD_SPEED = 110

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

def huristic_function(lat1, lon1, lat2, lon2):
    return compute_distance(lat1, lon1, lat2, lon2) / MAXIMAL_ROAD_SPEED


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


#TODO ucs 0-7 returns 0-6 and not 0-7!!!!!
def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    def f(node): return node.path_cost
    # TODO: paths returns 0-6 and not 0-7 (doesn't include last index=target)
    paths = best_first_graph_search(Routing_Problem(roads, source, target), f)
    path_indices = list(map(lambda link: link.source, paths))  # converts each link to it's source index
    return path_indices


#TODO ucs 0-7 returns 0-6!!!
def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    def g(node):
        return node.path_cost
    paths = best_first_graph_search(
        Routing_Problem(roads, source, target),
        f=lambda n: g(n) + huristic_function(roads[n.state].lat, roads[n.state].lon,
                                             roads[target].lat, roads[target].lon))
    path_indices = list(map(lambda link: link.source, paths))  # converts each link to it's source index
    return path_indices


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
        c = roads[link.target]
        solution = DFS_f(c, g + get_link_time(link), path + [c.index], f_limit, target)
        if solution is not None:
            return solution
    return None


# TODO: and here 0-7 returns 1-7 and not 0-7!!!!!@@@@@@@@@@@@@
def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
    global new_limit
    target_junc = roads[target]
    source_junc = roads[source]

    new_limit = h(source_junc, target_junc)
    while True:
        f_limit = new_limit
        new_limit = float("inf")
        solution = DFS_f(source_junc, 0, [], f_limit, target_junc)
        if solution is not None:
            return solution

def generate_drawings():
    #import random
    from ways.draw import plot_path
    with open('problems.csv') as problems_file:
        #problems = problems_file.readlines()
        #selected_problems = random.sample(problems, 10)

        # lines: 2, 3, 10, 14, 23, 38, 48, 56, 87, 89
        line_numbers = [1, 2, 11, 13, 22, 37, 47, 55, 86, 88]
        selected_problems = []

        for i, line in enumerate(problems_file):
            if i in line_numbers:
                selected_problems.append(line.strip())

        for problem in selected_problems:
            source, target = int(problem[0]), int(problem[1])
            path = find_idastar_route(source, target)
            plot_path(roads, path)

def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


def make_plot(solution):
    target = solution[-1].target

    def h(source):
        curr = roads[source]
        goal = roads[target]
        return huristic_function(curr.lat, curr.lon, goal.lat, goal.lon)

    # x represents what we thought would be the time cost, so we use the heuristic function for each source to goal
    # each element i holds the heuristic time cost value from node i to the goal
    # we also append 0 at the end, to represent the time cost from the goal to itself (for sure 0 so no need to compute)
    x = [h(link.source) for link in solution] + [0]
    y = [0]
    # list is reversed so we can move from goal to source and add only one link time at a time
    for link in reversed(solution):
        # holds the time cost from the next node to the goal
        next_junc_time = y[0]
        y.insert(0, get_link_time(link) + next_junc_time)

    import matplotlib.pyplot as plt
    plt.scatter(x, y)
    plt.show()


# if __name__ == '__main__':
#     from sys import argv  # TODO remove comment after finished
#     dispatch(argv)  # TODO: remove comment after finished

    # TODO delete these after as well:
    generate_drawings()

    #solutions = find_astar_route(30, 55)
    #make_plot(solution)


'''
alg_times = []
foreach problem:
    foreach algorithm:
        start_time = get_time()
        run_algorithm()
        end_time = get_time()
        duration = end_time - start_time
        alg_times.append(duration)
avg_time = sum(alg_times) / len(alg_times)
'''