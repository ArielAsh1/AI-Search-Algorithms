'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''
from RoutingProblem import Routing_Problem
from bestFirstGraphSearch import best_first_graph_search
from Helper import get_link_time

from ways import load_map_from_csv, compute_distance

roads = load_map_from_csv()

MAXIMAL_ROAD_SPEED = 110


# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

def huristic_function(lat1, lon1, lat2, lon2):
    return compute_distance(lat1, lon1, lat2, lon2) / MAXIMAL_ROAD_SPEED


def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    def f(node): return node.path_cost
    paths = best_first_graph_search(Routing_Problem(roads, source, target), f)
    # converts each link to its source index, and adds target at the end
    path_indices = list(map(lambda link: link.source, paths)) + [target]
    return path_indices


def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    def g(node):
        return node.path_cost
    paths = best_first_graph_search(
        Routing_Problem(roads, source, target),
        f=lambda n: g(n) + huristic_function(roads[n.state].lat, roads[n.state].lon,
                                             roads[target].lat, roads[target].lon))
    # converts each link to it's source index, and adds target at the end
    path_indices = list(map(lambda link: link.source, paths)) + [target]
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
        next_junc = roads[link.target]
        solution = DFS_f(next_junc, g + get_link_time(link), path + [next_junc.index], f_limit, target)
        if solution is not None:
            return solution
    return None


def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
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


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
