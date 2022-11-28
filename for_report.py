# name: Ariel Ashkenazy
# ID: 208465085

""" in the file we create the required information on questions 12 and 13 in the report.
this file is not necessary for the entire program to work properly."""

import random
from matplotlib import pyplot as plt

from SearchAlgorithms import roads
from main import find_idastar_route, find_astar_route, find_ucs_rout
from ways import draw


# for question 13:
def calculate_runtime():
    import time

    with open('problems.csv') as problems_file:

        # choosing problems that will not take too long to run, as instructed by Osnat the teacher assistant:
        # lines in problems.csv: 4, 8, 10, 14, 22, 38, 48, 28, 94, 90
        line_numbers = [3, 7, 11, 13, 21, 37, 47, 27, 93, 89]
        selected_problems = []

        for i, line in enumerate(problems_file):
            if i in line_numbers:
                selected_problems.append(line.strip())

        usc_times = []
        astar_times = []
        idastar_times = []

        for problem in selected_problems:
            source, target = problem.split(",")
            source = int(source)
            target = int(target)

            # idastar:
            start_time = time.time()
            find_idastar_route(source, target)
            end_time = time.time()
            idastar_times.append(end_time - start_time)

            # astar:
            start_time = time.time()
            find_astar_route(source, target)
            end_time = time.time()
            astar_times.append(end_time - start_time)

            # usc:
            start_time = time.time()
            find_ucs_rout(source, target)
            end_time = time.time()
            usc_times.append(end_time - start_time)

        usc_avg_time = sum(usc_times) / len(usc_times)
        astar_avg_time = sum(astar_times) / len(astar_times)
        idastar_avg_time = sum(idastar_times) / len(idastar_times)
        print("usc_avg_time", usc_avg_time)
        print("astar_avg_time", astar_avg_time)
        print("idastar_avg_time", idastar_avg_time)


# for question 12:
# creates 10 plots based on the 10 idastar random runs, one for each run
def generate_drawings():
    with open('problems.csv') as problems_file:

        line_numbers = []
        # selecting 10 random lines to read in problems_file
        for _ in range(10):
            line_numbers.append(random.randint(0, 100))
        # creating the 10 random selected problems
        selected_problems = []
        for i, line in enumerate(problems_file):
            if i in line_numbers:
                selected_problems.append(line.strip())

        for problem in selected_problems:
            source, target = problem.split(",")
            path = find_idastar_route(int(source), int(target))
            draw.plot_path(roads, path)
            plt.show()

# creates 10 selected plots manually ,as instructed by Osnat the teacher assistant:
#     path = find_idastar_route(796843, 796851)  # 4
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(360397, 360400)  # 8
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(41995, 42001)  # 10
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(30322, 30327)  # 14
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(910530, 910538)  # 22
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(769464, 769469)  # 38
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(13982, 13988)  # 48
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(818373, 818380)  # 28
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(327192, 327197)  # 94
#     draw.plot_path(roads, path)
#     plt.show()
#     path = find_idastar_route(196176, 196187)  # 90
#     draw.plot_path(roads, path)
#     plt.show()


if __name__ == '__main__':
    calculate_runtime()  # question 13
    # generate_drawings()  # question 12
