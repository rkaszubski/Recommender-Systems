#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np

#open reduced dataset and movie_titles

object = pd.read_pickle('data/cleanedMovie.pkl')
movies = pd.DataFrame(object)

terms = pd.read_csv('data/movie_titles.txt', sep='\t', encoding = "ISO-8859-1", header=None, index_col=0)
terms = terms.iloc[:,:2]
terms = terms.iloc[:,1:]

#function to convert movieID to title
def toTitle(MovieID):
    return terms.loc[ MovieID , : ][2]

#captures ratings of n movies when a new user joins app
def initial_rating(n, movielist, t):
    print("")
    
    ratings = []
    
    #if the user chooses to rate random movies
    if t == "r":
        print("These are",n, "random movies on our system:")
        order = np.random.randint(len(movielist), size=n)
    #if the user chooses to rate the most popular movies
    if t == "p":
        print("These are the top",n, "most watched movies on our system:")
        order = np.arange(n)
    print("Please rate at least 5 movies on a scale of 1 to 5 (1,2,3,4,5), you haven't seen it just hit Enter.")
    print("We can then start providing you recommendations based on your initial input!")
    print("")
    #iterates through n movies
    for mov in order:
        ID = movielist.index[mov]
        title = toTitle(ID)
        print("You are rating", title)
        #ensure proper input validation
        try:
            while True:
                b = int(input("Rate from 1 to 5: "))
                if b < 1 or b > 5:
                    print("Sorry, your response must be on a scale of 1 to 5.")
                    continue
                else:
                    break
            print("You rated", title, "as a", b)
            ratings.append([ID,b])
        #if the user presses enter of any non int values it skips the movie
        except:
            print("You skipped", title)
            print("")
            continue
        print("")
        
        
    return ratings

#function that asks how many movies to rate (n), returns a list of user created ratings back to main.py
def run_file(n):
    #print("Welcome to our Movie Recommender System!")
    print("We ask you to first rate some movies.")
    print("a Rate the", n,"most popular movies?")
    print("b Rate", n,"random movies?")
    choice = str(input("Please choose option a or b"))
    if choice == "a" or choice == "A":
        popular_movies = pd.DataFrame(movies["MovieID"].value_counts())
        return initial_rating(n, popular_movies, "p")
    else:
        popular_movies = pd.DataFrame(movies["MovieID"].value_counts())
        return initial_rating(n,popular_movies, "r")

