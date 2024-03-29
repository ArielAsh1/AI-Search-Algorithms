from Node import Node
from PriorityQueue import PriorityQueue


def best_first_graph_search(problem, f):
    node = Node(problem.s_start)
    frontier = PriorityQueue(f)
    frontier.append(node)
    closed_list = set()
    while frontier:
       # if len(closed_list) % 1000 == 0:
            # print(f'size of closed list:{len(closed_list)}')
        node = frontier.pop()  # here it adds a new link to node.solutions() list
        if problem.is_goal(node.state):
            return node.solution()

        closed_list.add(node.state)
        for child in node.expand(problem):
            if child.state not in closed_list and child not in frontier:
                frontier.append(child)
            elif child in frontier and f(child) < frontier[child]:
                del frontier[child]
                frontier.append(child)
    return None
