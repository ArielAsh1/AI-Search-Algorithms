# name: Ariel Ashkenazy
# ID: 208465085

""" receives input source and target and the selected search algorithm, and runs accordingly."""

from SearchAlgorithms import ucs_rout, astar_route, idastar_route


def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    return ucs_rout(source, target)


def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    return astar_route(source, target)


def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
    return idastar_route(source, target)


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
