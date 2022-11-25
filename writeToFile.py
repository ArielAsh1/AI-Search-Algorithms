from main import find_ucs_rout, find_astar_route, huristic_function, roads
from Helper import get_link_time
import csv


def get_link(source, target):
    source_junc = roads[source]
    for link in source_junc.links:
        if link.target == target:
            return link
    return None


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
            res_list.append(line + '\n')

    with open(f'results/{filename}.txt', "w") as file:
        file.writelines(res_list)


if __name__ == '__main__':
    run_from_problems(find_ucs_rout, 'UCSRuns')
    run_from_problems(find_astar_route, 'AStarRuns', add_estimated_time=True)
