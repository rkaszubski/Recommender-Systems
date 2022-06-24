#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np


#function that allows the user to rate movies found on our generated recommendations
#returns a list of MovieID, Rating that can then be appended to the users previously created ratings
def run_file(movies):
    print("Please rate on a scale of 1 to 5 (1,2,3,4,5), you haven't seen it just hit Enter.")
    print("We can then update your recommendations based on your newly added ratings!")
    cont = True
    out = []
    rated = []
    while cont:
        a = int(input("Enter index of movie you want to rate from the recommendations above: "))
        if a not in rated:
            print("You are rating:", movies[a-1][1])
            b = int(input("Rate from 1 to 5: "))
            print("You rated:", movies[a-1][1], "as a", b)
            out.append([movies[a-1][0], b])
            rated.append(a)
        else:
            print("Already rated, ", movies[a][1])
        b = str(input("Continue rating? y/n"))
        if b == "y" or b =="Y":
            continue
        else:
            cont = False
    return out