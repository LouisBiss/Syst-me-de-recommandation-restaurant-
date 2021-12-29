# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 14:39:15 2021

@author: louis
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

#imorter les données
df_resto = pd.read_csv('C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Système de recommandation//Projet//BDD//données_resto.csv')
df_liens_resto = pd.read_csv('C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Système de recommandation//Projet//BDD//liens_resto.csv')

#fusion des dataframes
df_global = pd.merge(df_resto, df_liens_resto, left_index=True, right_index=True)

#renomme la colonne id
df_resto = df_resto.rename(columns={'Unnamed: 0': 'Id'})

df_resto['Type_Cuisine'].replace('', np.nan, inplace=True)
df_resto.dropna(subset=['Type_Cuisine'], inplace=True)
df_resto.reset_index(drop=True, inplace=True)


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


                 #######################################
                 #         INTERFACE - Flask           #
                 #######################################

from flask import Flask, render_template,request

app = Flask(__name__,template_folder='templates')


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        Resto_Input = request.form['resto_input']
        Arr_Input=request.form['arr_input']
        Arr_Input=str(Arr_Input)
        
        ######## OPTION 1 #############
        
        if Arr_Input=='Tout Paris':
            
            count_vec=CountVectorizer()
            con=count_vec.fit_transform(df_resto['metadata'])
            cosine_sim_matrix=cosine_similarity(con, con)
            indices = pd.Series(df_resto.index, index = df_resto['Nom_Resto']) 
            
            
            def content_recommender(Nom_Resto):
                idx=indices[Nom_Resto]
                sim_scores= list(enumerate(cosine_sim_matrix[idx]))
                sim_scores= sorted(sim_scores, key=lambda x : x[1], reverse=True)
                sim_scores=sim_scores[1:11]
                resto_indices=[i[0] for i in sim_scores]
                return df_resto['Nom_Resto'].iloc[resto_indices]
            
            #Get recommandation 
            list_recom=content_recommender(Resto_Input)
            print(list_recom)
            
            df_liste_recom = pd.DataFrame(list_recom)
            df_recom_et_liens = pd.merge(df_liste_recom, df_global, on='Nom_Resto')
                
            liste_lien_recom=df_recom_et_liens['lien_resto'].to_list()
            liste_recom_flask = df_liste_recom['Nom_Resto'].to_list()
            
            name_link_list = zip(liste_recom_flask, liste_lien_recom)
            
            return render_template('base.html' , list_recom=list_recom)
            #return render_template('base.html' , liste_lien_recom=liste_lien_recom, liste_recom_flask=liste_recom_flask, len1=len(liste_recom_flask))

        
    
        #############  OPTION 2 #####################
        
    
        else:
              
            #un deuxième df contenant uniquement l'arrondissement souhaité 
            #df_resto_2=df_resto[(df_resto['Arrondissement']==input_Arr)]
            df_resto_2=df_resto[(df_resto['Arrondissement']==Arr_Input)]
            
            
            
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
            
            #Get recommandation 
            list_recom=content_recommender(Resto_Input)
            print(list_recom)
                    
            df_liste_recom = pd.DataFrame(list_recom)
            df_recom_et_liens = pd.merge(df_liste_recom, df_global, on='Nom_Resto')
        
            liste_lien_recom=df_recom_et_liens['lien_resto'].to_list()
            liste_recom_flask = df_liste_recom['Nom_Resto'].to_list()
            
            name_link_list = zip(liste_recom_flask, liste_lien_recom)
            
            return render_template('base.html' , name_link_list=name_link_list)
            #return render_template('base.html' , liste_lien_recom=liste_lien_recom, liste_recom_flask=liste_recom_flask, len1=len(liste_recom_flask))

      

if __name__=="__main__":
    app.run(debug=True)