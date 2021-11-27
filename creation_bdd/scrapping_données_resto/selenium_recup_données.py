# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:37:05 2021

@author: louis
"""

import selenium 
from selenium import webdriver
import re
import pandas as pd 
from time import sleep
from tqdm import tqdm 

#importe les liens des resto
df_liens_resto= pd.read_csv('C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Système de recommandation//Projet//création_bdd//Scrapping_lien_des_restos//liens_resto.csv')

#conversion colonne en liste
liste_liens_resto=df_liens_resto['lien_resto'].to_list()

#creation dataframe et des colonnes
df=pd.DataFrame()
df['Nom_Resto']=""
df['Type_Cuisine']=""
df['Type_Repas']=""
df['Arrondissement']=""


driver = webdriver.Firefox(executable_path="C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Web Scrapping//S2//geckodriver.exe")


#boucle de récupération des données
for lien in tqdm(liste_liens_resto):
    
    driver.get(lien)
    
    
    #créer une ligne vide
    df.loc[df.shape[0]] = ""
    
    Nom_resto = driver.find_element_by_class_name("fHibz")  #trouve le nom du resto
    Nom_resto=Nom_resto.text                                #conserve uniquement le text
    df['Nom_Resto'].iloc[-1]=Nom_resto                      #ajoute le nom à la dernière ligne de la colonne
    
    Type_cuisine=driver.find_elements_by_css_selector("div.cfvAV")[1]
    Type_cuisine=Type_cuisine.text
    df['Type_Cuisine'].iloc[-1]=Type_cuisine
    
    Type_repas=driver.find_elements_by_css_selector("div.cfvAV")[2]
    Type_repas=Type_repas.text
    df['Type_Repas'].iloc[-1]=Type_repas
    
    #Prix=driver.find_elements_by_css_selector("div.cfvAV")[0]
    
    
    adr=driver.find_elements_by_css_selector("a.fhGHT")[1]
    adr=adr.text
    arrd = re.findall(r'[750]//S*', adr) 
    df['Arrondissement'].iloc[-1]=arrd
    
    sleep(1.1)


#print(Type_Cuisine.text)
#print(test.text)
driver.close()


