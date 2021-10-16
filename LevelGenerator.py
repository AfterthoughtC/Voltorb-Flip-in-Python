# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:48:45 2020

@author: AfterthoughtC
"""

import random
import numpy as np


def calculate_summult(scoredist):
    summult = 0
    for i in range(len(scoredist)):
        summult += scoredist[i]*i

    return(int(summult))

def calculate_final_mult(scoredist):
    final_mult = 1
    for i in range(1,len(scoredist)):
        final_mult = final_mult * i**scoredist[i]
    return(final_mult)

def generate_one_stage(stage, size = 6,level = 1,maxmult = 3):
    no_of_cells = size*size
    x0 = size + level - 1
    x1 = no_of_cells - x0
    summult = no_of_cells + random.randint(int(round(level**0.5))-2,int(round(level**0.5))) + int((stage-1)/2)
    scoredist = [x0,x1]
    while len(scoredist) < maxmult+1:
        scoredist.append(0)
    while(calculate_summult(scoredist) < summult):
        if sum(scoredist[1:maxmult]) == 0:
            return(scoredist)
        tomoveup = random.randint(1,calculate_summult(scoredist[:-1]))
        numno = 0
        not_shifted = True
        for i in range(1,maxmult):
            numno += scoredist[i]*i
            if tomoveup <= numno and not_shifted:
                scoredist[i] -= 1
                scoredist[i+1] += 1
                not_shifted = False
    return(scoredist)

def create_level_array(scoredist):
    straight_array = []
    square_size = int(sum(scoredist)**0.5)
    for i in range(len(scoredist)):
        straight_array.extend([i for j in range(scoredist[i])])
    random.shuffle(straight_array)
    level_array = np.zeros((square_size,square_size))
    for i in range(square_size):
        level_array[i,:] = straight_array[i*square_size:square_size*(i+1)]
    return(level_array)

def generate_one_level(size,level,maxmult,stages = 5):
    all_stages = []
    s = 1
    while len(all_stages) < stages:
        current_stage = generate_one_stage(s,size,level,maxmult)
        if current_stage not in all_stages:
            all_stages.append(current_stage)
            s += 1
    all_stages = sorted(all_stages,key = lambda scoredist: calculate_final_mult(scoredist))
    return(all_stages)
    


if __name__ == '__main__':
    one_level = generate_one_level(5,1,3)
    
    for i in range(len(one_level)):
        print("Stage Number "+str(i+1))
        print("Max Score: "+str(calculate_final_mult(one_level[i])))
        print(create_level_array(one_level[i]))