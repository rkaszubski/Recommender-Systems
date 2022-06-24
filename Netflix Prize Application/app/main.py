#!/usr/bin/env python
# coding: utf-8

# In[1]:
#import files for initializing ratings, and adding ratings
import initial
import addrating



import numpy as np
import pandas as pd

#ask user for their name which we use as an id of sorts to generate files storing their ratings
import pickle
print("Welcome to our movie recommender system!")
name = str(input("Please enter your name: "))

#user data is stored in the users folder in a pkl file
import os.path
save_path = 'users/'
file_name = name+".pkl"
completeName = os.path.join(save_path, file_name)

#if the file exists, open the ratings from it
if os.path.isfile(completeName):
    with open(completeName, 'rb') as f:
        user_data = pickle.load(f)
#else we know its a new user, so run the initializing to capture their first ratings
else:
    user_data = initial.run_file(20)

#print(user_data)
#loop to keep the application running
cont = True
while cont:
    print("")
    print("Our system supports Clustering, Knn User, Knn Item, and SVD, each offering different recommendations!")
    print("Which would you like to run?")
    print("a Clustering")
    print("b Knn User-Based")
    print("c Knn Item-Based")
    print("d SVD")
    #users can pick which recommendation algorithm/system they want to use
    choice = str(input("Please choose option a, b, c, or d "))
    if choice == "a" or choice == "A":
        print("Clustering...")
        print("Please Wait")
        import cluster
        #recs returns the top movies recommended from that cluster
        recs = cluster.cluster(user_data)
        #print(recs)
        #addmore allows the user to rate movies that were recommended thus strengthning their predictions
        addmore = str(input("Would you like to rate any of the recommendations? y/n"))
        if addmore == "Y" or addmore == "y":
            new = addrating.run_file(recs)
            user_data += new
            #print(user_data)
    #repeat code except for Knn-user
    elif choice == "b" or choice == "B":
        print("KNN user-based...")
        print("Please Wait")
        import knn_u
        recs = knn_u.classify(user_data)
        addmore = str(input("Would you like to rate any of the recommendations? y/n"))
        if addmore == "Y" or addmore == "y":
            new = addrating.run_file(recs)
            user_data += new
            #print(user_data)
    elif choice == "c" or choice == "C":
        print("KNN item-based...")
        print("Please Wait")
        import knn_i
        recs = knn_i.classify(user_data)
        addmore = str(input("Would you like to rate any of the recommendations? y/n"))
        if addmore == "Y" or addmore == "y":
            new = addrating.run_file(recs)
            user_data += new
            #print(user_data)
    elif choice == "d" or choice == "D":
        print("SVD...")
        print("Please Wait")
        import svd
        recs = svd.run_svd(user_data)
        addmore = str(input("Would you like to rate any of the recommendations? y/n"))
        if addmore == "Y" or addmore == "y":
            new = addrating.run_file(recs)
            user_data += new
            #print(user_data)
    #ask the user if they want to exit
    choice_cont = str(input("Run a different algorithm? y/n"))
    if choice_cont == "y" or choice_cont == "Y":
        continue
    else:
        cont = False

#save their rating data into their pickle file
with open(completeName, 'wb') as f:
    pickle.dump(user_data, f)


