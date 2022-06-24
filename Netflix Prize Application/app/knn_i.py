#!/usr/bin/env python
# coding: utf-8

# In[1]
import numpy as np
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from math import sqrt
from sklearn.metrics import mean_squared_error
import math

df = pd.read_pickle('data/cleanedMovie.pkl')
user_movie_df = df.pivot(index='CustomerID',columns ='MovieID' ,values='Rating')
movie_names = list(user_movie_df.columns) 
customer_names = list(user_movie_df.index.values)

movie_users_df = df.pivot(index='MovieID',columns = 'CustomerID',values='Rating').fillna(0)

movie_title = pd.read_csv("data/movie_titles.csv", encoding='unicode_escape', usecols=[2], header=None)
movie_title.columns = ['title']
movie_title





#initiate knn algorithm
knn = NearestNeighbors(metric='cosine',algorithm = 'brute', n_neighbors=30)

#function to find similarity between movies
def find_similarity(topMovies,data,model,n_recommendation):
    dict_similarity = {}
    model.fit(data)
    for index in topMovies:
        array_index = data.iloc[index].to_numpy()
        neigh_dist, neigh_ind = model.kneighbors(array_index.reshape(1, 13141),n_neighbors=n_recommendation+1)
        neigh_dist_Lst = neigh_dist.tolist()[0][1:] #ignore itself
        neigh_ind_Lst = neigh_ind.tolist()[0][1:]
        for i in range(len(neigh_dist_Lst)):
            if neigh_ind_Lst[i] not in dict_similarity:
                dict_similarity[neigh_ind_Lst[i]] = (1-neigh_dist_Lst[i]) * topMovies.get(index)
            else:
                ratio = dict_similarity.get(neigh_ind_Lst[i])
                new_ratio = (ratio + (1-neigh_dist_Lst[i]) * topMovies.get(index))/2
                dict_similarity[neigh_ind_Lst[i]] = new_ratio
            
    sort_dict = dict(sorted(dict_similarity.items(), key=lambda item: item[1],reverse=True))
    return sort_dict

#function to make a recommendation - returns a list of movies recommended
def make_recommendation(user_ratings, topMovies, newUser_rating, data, model, n_recommendation):    
    count = 0
    recs = []
    sort_dict = find_similarity(topMovies,data,model,n_recommendation)
    print("Recommended Movies:")
    for movie_ind in sort_dict:
        if count < 10:
            if int(newUser_rating[movie_ind]) == 0:
                res = movie_title.loc[movie_ind-1]['title']
                recs.append([movie_ind-1, res])
            print(count+1, res)
            count += 1
    return recs





#function called by main.py to run knn - item based
#returns a list of movies that were recommended
def classify(user_ratings):
    newUser_dict = {}
    column_names = movie_names
    df_newUser = pd.DataFrame(columns = column_names)
    for i in user_ratings:
        newUser_dict[i[0]] = i[1]
        df_newUser.at[0 , i[0]] = i[1]
    newUser_df = df_newUser.fillna(0)    
    newUser_dict_sort = dict(sorted(newUser_dict.items(), key=lambda item: item[1],reverse=True))
    top3movies = {k: newUser_dict_sort[k] for k in list(newUser_dict_sort)[:3]}
    recs = make_recommendation(user_ratings, top3movies, newUser_df, movie_users_df,knn,10)
    return recs