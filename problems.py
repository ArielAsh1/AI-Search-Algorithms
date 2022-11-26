# name: Ariel Ashkenazy
# ID: 208465085


""" this file creates 100 random problems as requested in question 1.3 """

import pandas as pd
import random
from ways import load_map_from_csv


def single_step_on_map(s1, junctions_list):
    # if new s1 has no target links break loop (in case it can't move 15 links forward)
    if len(s1.links) == 0:
        return s1
    junc_target_index = s1.links[0].target
    # now find this target index in junc_list and make it the new start for next link step
    t1 = junctions_list[junc_target_index]
    return t1


# gets a start junction (s1) and move along the map between 5 and 15 links to arrive somewhere (t1).
# returns target junction t1
def move_on_map(s1, junctions_list):
    min_steps = random.randint(5, 15)
    t1 = s1
    steps = 0
    # makes sure we make at least min_steps, and after we make sure we didn't move around in a circle.....
    while steps < min_steps or t1.index == s1.index:
        t1 = single_step_on_map(t1, junctions_list)
        steps += 1

    return t1


def create_random_problems_csv():
    roads = load_map_from_csv()
    problems = []
    num_of_problems = 100
    junc_list = roads.junctions()
    non_dead_end = list(filter(lambda x: len(x.links) > 0, junc_list))
    # generate a list of 100 unique start junctions
    start_list = random.sample(range(len(non_dead_end)), num_of_problems)

    # creates 100 tuples (s1,t1) of start and target indices for random problems
    for junc_start in start_list:
        # save the original start index and send it to move_on_map function
        s1 = non_dead_end[junc_start]
        t1 = move_on_map(s1, junc_list)

        # now save (s1,t1) as a new set and add them to the ongoing list
        start_target_tuple = (s1.index, t1.index)
        problems.append(start_target_tuple)

    # convert list to csv file
    s1_t1_df = pd.DataFrame(problems)
    s1_t1_df.to_csv('problems.csv', encoding='utf-8', header=False, index=False)


# a function built to test this file is working properly - FOR MY OWN USE -
# this is not an integrated part of the code and not necessary for the correct run on this code!
def test():
    roads = load_map_from_csv()
    junc_list = roads.junctions()
    with open('problems.csv', 'r') as f:
        for line in f.readlines():
            start, dest = line.split(',')
            s = junc_list[int(start)]
            if all([link.source != int(dest) and link.target != int(dest) for link in s.links]):
                print(start, dest)


if __name__ == '__main__':
    create_random_problems_csv()


