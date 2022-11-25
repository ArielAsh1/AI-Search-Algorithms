from matplotlib import pyplot as plt
from main import find_idastar_route, find_astar_route, find_ucs_rout, roads, huristic_function
from ways import draw


# for question 13:
def calculate_runtime():

    import time

    with open('problems.csv') as problems_file:

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
def generate_drawings():
    # with open('problems.csv') as problems_file:
    #
    #     # lines in problems.csv: 4, 8, 10, 14, 22, 38, 48, 28, 94, 90
    #     line_numbers = [3, 7, 11, 13, 21, 37, 47, 27, 93, 89]
    #     selected_problems = []
    #
    #     for i, line in enumerate(problems_file):
    #         if i in line_numbers:
    #             selected_problems.append(line.strip())
    #
    #     for problem in selected_problems:
    #         source, target = problem.split(",")
    #         path = find_idastar_route(int(source), int(target))
    #         draw.plot_path(roads, path)
    #         plt.savefig(f"solution_img/fig_{source}-{target}.png")
    # plt.show()

# manual:
    path = find_idastar_route(796843, 796851)  # 4
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(360397, 360400)  # 8
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(41995, 42001)  # 10
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(30322, 30327)  # 14
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(910530, 910538)  # 22
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(769464, 769469)  # 38
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(13982, 13988)  # 48
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(818373, 818380)  # 28
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(327192, 327197)  # 94
    draw.plot_path(roads, path)
    plt.show()
    path = find_idastar_route(196176, 196187)  # 90
    draw.plot_path(roads, path)
    plt.show()

# # for question 9?
# def make_plot(solution):
#     target = solution[-1].target
#
#     def h(source):
#         curr = roads[source]
#         goal = roads[target]
#         return huristic_function(curr.lat, curr.lon, goal.lat, goal.lon)
#
#     # x represents what we thought would be the time cost, so we use the heuristic function for each source to goal
#     # each element i holds the heuristic time cost value from node i to the goal
#     # we also append 0 at the end, to represent the time cost from the goal to itself (for sure 0 so no need to compute)
#     x = [h(link.source) for link in solution] + [0]
#     y = [0]
#     # list is reversed, so we can move from goal to source and add only one link time at a time
#     for link in reversed(solution):
#         # holds the time cost from the next node to the goal
#         next_junc_time = y[0]
#         y.insert(0, get_link_time(link) + next_junc_time)
#
#     plt.scatter(x, y)
#     plt.show()


if __name__ == '__main__':
    calculate_runtime()  # question 13
    #generate_drawings()  # question 12

