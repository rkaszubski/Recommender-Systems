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
user_movie_df = df.pivot(index='CustomerID',columns ='MovieID' ,values='Rating').fillna(0)


movie_names = list(user_movie_df.columns) 
customer_names = list(user_movie_df.index.values)

knn = NearestNeighbors(metric='cosine',algorithm = 'brute', n_neighbors=10)

movie_title = pd.read_csv("data/movie_titles.csv", encoding='unicode_escape', usecols=[2], header=None)
movie_title.columns = ['title']
movie_title

recommendation = {}
#function to make recommendation, returns a list of recommendations
def make_recommendation(user_ratings, input_user,data,model,n_recommendation):
    model.fit(data)
    input_user_array = input_user.to_numpy()
    similar_users_list = (model.kneighbors(input_user_array,n_neighbors=n_recommendation+1,return_distance=False)).tolist()
    for i in similar_users_list[0][1:]:
        for j in data.columns:
            ratingLst = []
            if int(input_user[j]) == 0 and data.iloc[i][j] > 3:
                if j not in recommendation:
                    ratingLst.append(data.iloc[i][j])
                    recommendation[j] = ratingLst
                else:
                    recommendation.get(j).append(data.iloc[i][j])
    print("Recommended Movies:")
    number = 0
    recs = []
    watched = []
    for movie in user_ratings:
        watched.append([movie][0][0])
    for k in sorted(recommendation, key=lambda k: len(recommendation[k]), reverse=True):
        if number < 10:
            if k-1 not in watched:
                res = movie_title.loc[k-1]['title']
                recs.append([k-1, res])
                print(number+1, res)
                number += 1 #recommend top 10 movies
    return recs     

#convert user_ratings from list to dataframe
# create a empty dataframe




#run function from main.py

def classify(user_ratings):
    column_names = movie_names
    df_newUser = pd.DataFrame(columns = column_names)
    for i in user_ratings:
        df_newUser.at[0 , i[0]] = i[1]
    newUser_df = df_newUser.fillna(0)
    recs = make_recommendation(user_ratings, newUser_df, user_movie_df, knn, 10)
    return recs