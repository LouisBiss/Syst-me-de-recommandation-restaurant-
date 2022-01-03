# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 17:37:46 2022

@author: louis
"""

import pandas as pd

df_résultats= pd.read_csv('C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Système de recommandation//Projet//System_recommandation//affichage résultat filtrage collab//reco_resto_utilisateur.csv')

df_résultats.drop(['Unnamed: 0', 'id_utilisateur','resto_reco'], axis=1, inplace=True)

#print(df_résultats['Nom_utilisateur'][1])

"""
i=0
while i <= len(df_résultats) - 1 :
    df_résultats['resto_reco'][i]=df_résultats['resto_reco'][i].replace("['","")
    df_résultats['resto_reco'][i]=df_résultats['resto_reco'][i].replace("']","")
    df_résultats['resto_reco'][i]=df_résultats['resto_reco'][i].replace('"]','')
    df_résultats['resto_reco'][i]=df_résultats['resto_reco'][i].replace('["','')
    df_résultats['resto_reco'][i]=df_résultats['resto_reco'][i].replace('"','')
    df_résultats['resto_reco'][i]=df_résultats['resto_reco'][i].replace("'","")


    i=i+1
"""

#input_name = input('Quel utilisateur ? : ')


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
        Name_Input = request.form['name_input']
        
        df_test=df_résultats.loc[df_résultats['Nom_utilisateur'] == Name_Input]
        df_test = df_test.reset_index()

        a=df_test.loc[0,'nom_resto']
        
        
            
        return render_template('base.html', a=a)

    
if __name__=="__main__":
    app.run(debug=True)
