# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:37:05 2021

@author: louis
"""

import selenium 
from selenium import webdriver
import re
import pandas as pd 

#creation dataframe et des colonnes
df=pd.DataFrame()
df['Nom_Resto']=""
df['Type_Cuisine']=""
df['Type_Repas']=""
df['Arrondissement']=""


driver = webdriver.Firefox(executable_path="C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Web Scrapping//S2//geckodriver.exe")
driver.get("https://www.tripadvisor.fr/Restaurant_Review-g187147-d9806534-Reviews-ASPIC-Paris_Ile_de_France.html")


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
arrd = re.findall(r'[750]\S*', adr) 
df['Arrondissement'].iloc[-1]=arrd


#print(Type_Cuisine.text)
#print(test.text)
driver.close()


