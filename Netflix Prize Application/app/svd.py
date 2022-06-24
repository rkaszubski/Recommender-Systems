import pickle
from tqdm import tqdm
import numpy as np
import pandas as pd
import os
import pathlib
from surprise import Reader, Dataset
from surprise import SVD
from surprise import SVDpp
from surprise.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

movie_title = pd.read_csv("data/movie_titles.csv", encoding='unicode_escape', usecols=[2], header=None)
movie_title.columns = ['title']
movie_title.head(15)



class SVDPredictor:
    error_table = pd.DataFrame(columns = ["Model", "Train_RMSE", "Test_RMSE"])
    
    #Class takes in final.csv as a whole as a DataFrame
    def __init__(self, data, titles):
        self.movie = data
        self.titles = titles
        self._createAlgorithmFromData()
        
    def _createAlgorithmFromData(self):
        #check if algo and trainset/train_data files are already created
        self._splitMovie()
        self._createTrainSet()
        self._run_surprise()
        
    def recommendFor(self, customerID, count, user_ratings):
        preds = []
        ids = []
        watched = []
        for movie in user_ratings:
            watched.append([movie][0][0])
        for mov in self.movie.MovieID.unique().tolist():
            preds.append(self.predict(customerID, mov).est)
            ids.append(mov)
            
        movieAndRating = {}
        copyPreds = preds[:]
        while count > 0:
            index = copyPreds.index(max(copyPreds))
            maxPred = max(copyPreds)
            mov = ids[index]
            if mov not in watched:
                title = movie_title.iloc[mov-1:mov]['title'][mov-1]
                movieAndRating[mov] = maxPred
            copyPreds.pop(index)
            count -= 1
        return movieAndRating
        
    def predict(self, userID, movieID):
        #use algo to predict rating. Return predicted rating
        return self.algo.predict(userID, movieID)
    
    def _splitMovie(self):
        self.movie = self.movie.iloc[:1500000]
        
    def _createTrainSet(self):
        reader = Reader(rating_scale=(1,5))
        movieInput = pd.DataFrame()
        movieInput['CustomerID'] = self.movie['CustomerID']
        movieInput['MovieID'] = self.movie['MovieID']
        movieInput['Rating'] = self.movie['Rating']

        self.train_data = Dataset.load_from_df(movieInput, reader)
        self.trainset = self.train_data.build_full_trainset()
        #write to a file
    
    def _reduceDataSize(self):
        #self.movie['Date'] = self.movie['Date'].astype('category')
        self.movie['MovieID'] = self.movie['MovieID'].astype('int16')
        self.movie['CustomerID'] = self.movie['CustomerID'].astype('int32')
        self.movie['Rating'] = self.movie['Rating'].astype('int8')
    
    def _run_surprise(self):
        self.algo = SVD(n_factors = 5, biased=True, verbose=False)
        self.algo = self.algo.fit(self.trainset)
            

movieID = pd.read_pickle("data/cleanedMovie.pkl")
 
def recommendFor(customerID, model):
    predictions = []
    ids = []
    for mov in movieID.MovieID.unique().tolist():
        predictions.append(model.predict(customerID, mov).est)
        ids.append(mov)
    return predictions

def recommendedMovies(count, preds, movs):
    movieAndRating = {}
    copyPreds = preds[:]
    for i in range(count):
        index = copyPreds.index(max(copyPreds))
        maxPred = max(copyPreds)
        mov = movs[index]
        title = movie_title.iloc[mov-1:mov]['title'][mov-1]
        movieAndRating[title] = maxPred
        copyPreds.pop(index)
    return movieAndRating
 
#function required to run svd by main.py       
def run_svd(user_ratings):
    movie = pd.read_pickle("data/cleanedMovie.pkl")
    #print(movie.shape)
    for rating in user_ratings:
        movie = movie.append(pd.DataFrame([[rating[0],2649430,rating[1]]], columns=movie.columns))
    #print(movie.shape)
    #print(movie.loc[movie['CustomerID'] == 2649430])
    svd = SVDPredictor(movie, movie_title)
    out= svd.recommendFor(2649430, 10, user_ratings)
    print("")
    print("Recommended movies:")
    movies_returned = 0
    output = []
    for key, value in out.items():
        print(movies_returned+1, movie_title.iloc[key-1]['title'])
        movies_returned += 1
        output.append([key,movie_title.iloc[key-1]['title']])
    return output

