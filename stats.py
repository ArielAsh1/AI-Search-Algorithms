
# This file should be runnable to print map_statistics using
# $ python stats.py


from collections import namedtuple

from ways.info import ROAD_TYPES
from ways import load_map_from_csv
import sys

def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])

    num_of_road_types = len(ROAD_TYPES)
    # creates a new dict that will hold the count for each road type.
    # keys - road types and values - the count for each type. all values are initiated with 0.
    histogram = {road: 0 for road in range(num_of_road_types)}

    link_count = 0
    link_max_dist = -1
    link_sum_dist = 0
    link_min_dist = float("inf")
    for link in roads.iterlinks():
        histogram[link.highway_type] += 1  # incrementing count for this road type in the dict
        link_count += 1
        link_max_dist = max(link_max_dist, link.distance)
        link_min_dist = min(link_min_dist, link.distance)
        link_sum_dist += link.distance
    link_avg = link_sum_dist / link_count

    junc_count = 0
    junc_max_branch = -1
    junc_sum_branch = 0
    junc_min_branch = sys.maxsize
    for junc in roads.junctions():
        num_of_links = len(junc.links)
        junc_count += 1
        junc_max_branch = max(junc_max_branch,num_of_links)
        junc_min_branch = min(junc_min_branch, num_of_links)
        junc_sum_branch += num_of_links
    junc_avg = junc_sum_branch / junc_count

    return {
        'Number of junctions' : junc_count,
        'Number of links' : link_count,
        'Outgoing branching factor' : Stat(max=junc_max_branch, min=junc_min_branch, avg=junc_avg),
        'Link distance' : Stat(max=link_max_dist, min=link_min_dist, avg=link_avg),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : histogram,  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()

