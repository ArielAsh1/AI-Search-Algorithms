# name: Ariel Ashkenazy
# ID: 208465085

""" this file creates txt files with the outputs of UCS and A* runs.
in addition, it can create the plot for the A* 100 runs, as requested in question 9 in the report"""

from matplotlib import pyplot as plt

from SearchAlgorithms import roads, huristic_function
from main import find_ucs_rout, find_astar_route
from Helper import get_link_time
import csv


def get_link(source, target):
    source_junc = roads[source]
    for link in source_junc.links:
        if link.target == target:
            return link
    return None


time_list = []
huristic_time_list = []


def run_from_problems(search_algo, filename, add_estimated_time=False):
    res_list = []
    with open('problems.csv') as probs_file:
        csvreader = csv.reader(probs_file)
        for problem in csvreader:
            source, target = int(problem[0]), int(problem[1])
            path = search_algo(source, target)  # returns links indices
            res_links = [get_link(path[i], path[i + 1]) for i in range(len(path) - 1)]

            time = 0
            for link in res_links:
                time += get_link_time(link)

            if add_estimated_time:
                time_list.append(time)  # builds a list to be used for make_plot() later

            res_junctions = [source] + [link.target for link in res_links]
            res_junctions_str = list(map(lambda x: str(x), res_junctions))  # converts each to a string
            # combine all strings to one big string, with space between each string:
            res_junctions_spaces = " ".join(res_junctions_str)
            line = f'{res_junctions_spaces} - {time}'
            # if we run AStar algo we want to print estimated time as well
            if add_estimated_time:
                source_junc = roads[source]
                target_junc = roads[target]
                estimated_time = huristic_function(source_junc.lat, source_junc.lon, target_junc.lat, target_junc.lon)
                line += f' - {estimated_time}'
                huristic_time_list.append(estimated_time)  # builds a list to be used for make_plot() later
            res_list.append(line + '\n')

    with open(f'results/{filename}.txt', "w") as file:
        file.writelines(res_list)


# question 9 in the report
# creates plot for 100 astar runs
def create_astar_plot():
    plt.scatter(huristic_time_list, time_list)
    plt.xlabel("Heuristic time")
    plt.ylabel("Real time")
    plt.title("A* Plot")
    plt.xlim(0, max(huristic_time_list) + 0.010)
    plt.ylim(0, max(time_list) - 0.003)
    plt.show()


if __name__ == '__main__':
    run_from_problems(find_ucs_rout, 'UCSRuns')
    run_from_problems(find_astar_route, 'AStarRuns', add_estimated_time=True)
    # run this to create plot using the 100 astar runs data:
    # create_astar_plot()
