# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 15:37:40 2021

@author: louis
"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox(executable_path="C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Web Scrapping//S2//geckodriver.exe")
driver.get("https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html")


liste_liens_resto=[]
page=0

while True:
    time.sleep(1)
    
    liste_lien_html=driver.find_elements_by_xpath('//a[@class="bHGqj Cj b"]')
    #liste_lien_html=driver.find_elements_by_class_name("bHGqj Cj b")
    for html in liste_lien_html:
        #print(class_lien)
        a=html.get_attribute('href')
        liste_liens_resto.append(a)
      
    if len(driver.find_elements_by_css_selector("a.nav next rndBtn ui_button primary taLnk"))>0:
        page_suivante=driver.find_element_by_link_text("Suivant")
        page_suivante.click()
        page+=1
        if page>3:
            break
        else:
            break
driver.close()

