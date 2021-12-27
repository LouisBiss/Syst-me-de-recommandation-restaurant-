# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 17:05:40 2021

@author: louis
"""

"""Créer un premier système de recommandation basé sur le contenu. 
Par exemple, la recommandation des restaurants à un utilisateur est 
basée sur la description des restaurants."""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer

#imorter les données
df_resto = pd.read_csv('C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Système de recommandation//Projet//BDD//données_resto.csv')

#renomme la colonne id
df_resto = df_resto.rename(columns={'Unnamed: 0': 'Id'})

input_Arr = input('Dans quel arrondissement souhaitez vous manger ? : ')
input_Rest = input('Quel restaurant avez vous aimé ? : ')


df_resto['Type_Cuisine'].replace('', np.nan, inplace=True)
df_resto.dropna(subset=['Type_Cuisine'], inplace=True)
df_resto.reset_index(drop=True, inplace=True)


#vérifie que les id sont bien des int
print(df_resto['Id'].dtypes)
print(df_resto.info())



#convertir les ID non-integer en NaN
def verif_id(x):
    try:
        return int(x)
    except:
        return np.nan
df_resto['Id']=df_resto['Id'].apply(verif_id)

#conversion des de la colonne contenant les types de cuisines en liste 
i=0
while i <= len(df_resto) - 1 :
    
    #type cuisine
    df_resto['Type_Cuisine'][i]=str(df_resto['Type_Cuisine'][i])
    
    df_resto['Type_Cuisine'][i]=df_resto['Type_Cuisine'][i].replace("'","")
    #df_resto['Type_Cuisine'][i]=df_resto['Type_Cuisine'][i].replace(' ','')
    #convertit en liste les séparer par une virgule
    df_resto['Type_Cuisine'][i]= df_resto['Type_Cuisine'][i].split(",") 
    
    #type de repas
    df_resto['Type_Repas'][i]=str(df_resto['Type_Repas'][i])
    
    df_resto['Type_Repas'][i]=df_resto['Type_Repas'][i].replace("'","")
    #convertit en liste les séparer par une virgule
    df_resto['Type_Repas'][i]= df_resto['Type_Repas'][i].split(",") 
    
    
    i=i+1
    

#df_resto['Type_Cuisine']=df_resto['Type_Cuisine'].apply(literal_eval)
df_resto['Type_Cuisine']=df_resto['Type_Cuisine'].apply(lambda x : x[:3] if len(x)> 3 else x)
df_resto['Type_Repas']=df_resto['Type_Repas'].apply(lambda x : x[:3] if len(x)> 3 else x)

df_resto['Type_Cuisine']=df_resto['Type_Cuisine'].apply(lambda x : [i.replace(" ","") for i in x])
df_resto['Type_Repas']=df_resto['Type_Repas'].apply(lambda x : [i.replace(" ","") for i in x])

df_resto['metadata'] = df_resto.apply(lambda x : ' ' .join(x['Type_Cuisine'])+ ' ' + ' '.join(x['Type_Repas']), axis = 1)

#un deuxième df contenant uniquement l'arrondissement souhaité 
#df_resto_2=df_resto[(df_resto['Arrondissement']==input_Arr)]
df_resto_2=df_resto[(df_resto['Arrondissement']==input_Arr)]



count_vec=CountVectorizer()
con=count_vec.fit_transform(df_resto_2['metadata'])
cosine_sim_matrix=cosine_similarity(con, con)
indices = pd.Series(df_resto.index, index = df_resto['Nom_Resto']) 


def content_recommender(Nom_Resto):
    idx=indices[Nom_Resto]
    sim_scores= list(enumerate(cosine_sim_matrix[idx]))
    sim_scores= sorted(sim_scores, key=lambda x : x[1], reverse=True)
    sim_scores=sim_scores[1:11]
    resto_indices=[i[0] for i in sim_scores]
    return df_resto_2['Nom_Resto'].iloc[resto_indices]

#Get recommandation of the lion King
list_recom=content_recommender(input_Rest)
print(list_recom)
