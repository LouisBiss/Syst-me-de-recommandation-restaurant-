# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 11:02:44 2021

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

driver = webdriver.Firefox(executable_path="C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Web Scrapping//S2//geckodriver.exe")

#création dataframe
df=pd.DataFrame()
df['Nom_Resto']=""
df['Nom_utilisateur']=""
df['note']=""

#récuperer le premier nom de la classe des span de chaque div (contenant la note)


for lien in tqdm(liste_liens_resto):
    
    driver.get(lien)

    i=0
    while i <= 4: 
        try:
    
            #créer une ligne vide
            df.loc[df.shape[0]] = ""        
    
            ### NOM RESTO ###
    
            Nom_resto = driver.find_element_by_class_name("fHibz").text
            df['Nom_Resto'].iloc[-1]=Nom_resto                      #ajoute le nom à la dernière ligne de la colonne
    
            ###  NOTE ####
            div = driver.find_elements_by_xpath("//div[@class='ui_column is-9']")[i]    #parents
            span = div.find_element_by_xpath("./child::*")                              #enfant
            nom_classe = span.get_attribute('class')                                    #attribut
            note = nom_classe[24:-1]                   #efface les 24 premiers charactères ainsi que le dernier
            df['note'].iloc[-1]=note
            
            ### UTILISATEUR ###
            Nom_utilisateur = driver.find_elements_by_xpath("//div[@class='info_text pointer_cursor']")[i].text   
            df['Nom_utilisateur'].iloc[-1]=Nom_utilisateur                    #ajoute le nom à la dernière ligne de la colonne
    
            i = i+1
            
            
    
        except:
            pass

    sleep(1)
    
    
driver.close()

df.to_csv('avis_notes_resto.csv')
