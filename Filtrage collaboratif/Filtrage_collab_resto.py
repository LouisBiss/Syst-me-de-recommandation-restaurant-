# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 15:13:37 2022

@author: louis
"""

from surprise import Dataset
from surprise import accuracy
import numpy as np
import os
import csv
import pandas as pd
from surprise.model_selection import train_test_split
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from surprise import Reader, Dataset, KNNBasic, KNNWithMeans, KNNBaseline, KNNWithZScore
from sklearn.metrics.pairwise import cosine_similarity
from surprise.model_selection import cross_validate
import ast 
import json



def selet_top(predictions, n):
    # First map the predictions to each user.
    top_r = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_r[uid].append((iid, est))
        err=abs(est - true_r)
        #print(err)

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_r.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_r[uid] = user_ratings[:n]

    return top_r


#Reading the dataset
Data= pd.read_csv('C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Système de recommandation//Projet//BDD//avis_notes_resto.csv')

#efface colonne inutile
Data = Data.drop('Unnamed: 0', 1)


#création de colonnes convertissant les valeurs en id unique
Data['id_utilisateur'] = Data.groupby(Data.Nom_utilisateur.tolist(), sort=False).ngroup() + 1
Data['id_resto'] = Data.groupby(Data.Nom_Resto.tolist(), sort=False).ngroup() + 1


#rating_scale min = 1 et max = 5 de scores 
reader = Reader(rating_scale=(1, 5))
Data1 = Dataset.load_from_df(Data[['id_utilisateur', 'id_resto', 'note']], reader)

#Splitting the dataset
trainset, testset = train_test_split(Data1, test_size=0.3,random_state=10)
print('Number of users: ', trainset.n_users, '//n')
print('Number of items: ', trainset.n_items, '//n')
models=[KNNBasic, KNNWithMeans]
mesure=['cosine', 'pearson']
list_k=[10,20,30,40]
    # Creating an empty Dataframe with column names only
dfObj = pd.DataFrame(columns=['model', 'measure', 'k', 'resman', 'value'])
for i in range (0,2):
    print('models',models[i])
    for j in range(0,2):
        print('mesure',mesure[j])
        for k in list_k:
            print('la valeur de k :', k)
            #Use user_based true/false to switch between user-based or item-based collaborative filtering
            algo = models[i](k=k,sim_options={'name': mesure[j], 'user_based': True})
            #results = cross_validate(algo = algo, data = Data1, measures=['RMSE'], cv=5, return_train_measures=True)    
            #resmean=results['test_rmse'].mean()
            algo.fit(trainset)        
            # run the trained model against the testset
            test_pred = algo.test(testset)
            test_pred
            #evaluate model
            valeur=accuracy.rmse(test_pred, verbose=True)
            print("valeur", valeur)
            top_r = selet_top(test_pred, n=5)
            
            dfObj = dfObj.append({'model': models[i], 'measure': mesure[j], 'k':k, 'resman':valeur, 'value': top_r}, ignore_index=True) #index 0, 1
     
dfObj.sort_values(by = 'resman', inplace = True)          

#meilleur algo avec parametres
ress1=dfObj.iloc[0]
#ress1
#recuperer les valeurs user, item, score du meilleur resultats
#ress=dfObj['value'].iloc[0]
#resu=df.iloc[0, df.columns.get_loc('value')] 
resu=dfObj.iloc[0, dfObj.columns.get_loc('value')] 
resue=dfObj.iloc[0]['value']

#création dataframe des résultats
df_résultats=pd.DataFrame()
df_résultats['id_utilisateur']=""
df_résultats['resto_reco']=""



#Print the recommended items for each user
for uid, user_ratings in resu.items():
    #créer une ligne vide
    df_résultats.loc[df_résultats.shape[0]] = "" 

    df_résultats['id_utilisateur'].iloc[-1]=uid                      
    df_résultats['resto_reco'].iloc[-1]=[iid for (iid, _) in user_ratings]                     

    #print(uid, [iid for (iid, _) in user_ratings])
   
sub_df=Data[['id_utilisateur','Nom_utilisateur']]
sub_df['id_utilisateur'].drop_duplicates()

sub_df_2=Data[['id_resto','Nom_Resto']]

df_test = pd.merge(df_résultats, sub_df, left_on='id_utilisateur', right_on='id_utilisateur', how='left')
 
map_dict = dict(zip(sub_df_2.id_resto,sub_df_2.Nom_Resto))
df_test['nom_resto'] =  df_test['resto_reco'].explode().map(map_dict).groupby(level=0).agg(list)
   
df_test.to_csv('reco_resto_utilisateur.csv')
