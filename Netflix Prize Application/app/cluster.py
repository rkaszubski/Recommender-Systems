#!/usr/bin/env python
# coding: utf-8

# In[1]
import numpy as np
import pandas as pd
import pickle

#import kMeans
from sklearn.cluster import KMeans

#open reduced dataset from pickle file
object = pd.read_pickle('data/cleanedMovie.pkl')
movies = pd.DataFrame(object)

#open all movie titles
terms = pd.read_csv('data/movie_titles.txt', sep='\t', encoding = "ISO-8859-1", header=None, index_col=0)
terms = terms.iloc[:,:2]
terms = terms.iloc[:,1:]

#pivot the data into a customer x movie matrix
movieMatrix = movies.pivot_table(values='Rating', index='CustomerID', columns='MovieID')
movieMatrix = movieMatrix.fillna(0)
movie_arr = np.array(movieMatrix)

#run kmeans and fit the data
kmeans = KMeans(n_clusters=10)
kmeans.fit(movie_arr)
   
#function to return movie title based on ID 
def toTitle(MovieID):
    return terms.loc[ MovieID , : ][2]
 
#prints recommendations   
def top_movies_user(df, n, user_ratings):
    #checks if a viewer has already seen a recommendation
    watched = []
    for movie in user_ratings:
        watched.append([movie][0][0])
    moviesreturned = 0
    movieidx = 0
    recs = []
    while moviesreturned != n:
        #if a movie hasn't been seen, we can print it out as a recommendation
        if df.index[movieidx] not in watched:
            print(moviesreturned+1, toTitle(df.index[movieidx]))
            recs.append([df.index[movieidx],toTitle(df.index[movieidx])])
            movieidx += 1
            moviesreturned +=1
            
        else:
            movieidx +=1
    #return the movies that were recommended
    return recs

#prints a specific cluster
def print_clust(kmeans, k, n, user_ratings):
        #accesses cluster data from kmeans
        clust = pd.DataFrame(kmeans.cluster_centers_[k-1])
        clust.index = movieMatrix.columns
        #print(clust)
        #sortDF = pd.DataFrame(clust,terms)
        #print(sortDF)
        sortDF = clust.sort_values(by=[0],ascending=False)
        #print(sortDF.loc[sortDF.index[0]][0])
        #print(sortDF)
        print("Top movies in Cluster", k)
        #calls function above to print movies
        recs = top_movies_user(sortDF, n, user_ratings)
        print("")
        return recs
  
#converts user supplied data into a full data row consisting of all movies - 0s subsitutied for movies not yet seen      
def user_row(user_data):
    out = pd.DataFrame(np.zeros(len(movieMatrix.columns)), index=movieMatrix.columns).T
    for rating in user_data:
        out[rating[0]] = rating[1]
    out = np.array(out)
    return out

#function that needs to be called to run clustering, passes in the user created ratings list
def cluster(user_ratings):
    user_data = user_row(user_ratings)
    #determines the users cluster based on the model
    user_cluster = kmeans.predict(user_data)
    print("You have been assigned to cluster:", user_cluster[0]+1)
    print("We recommend: ")
    recs = print_clust(kmeans, user_cluster[0]+1, 10, user_data)
    #returns recommended movies back to main.py
    return recs
    

    
    




