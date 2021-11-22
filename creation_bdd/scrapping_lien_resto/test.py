# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 16:36:39 2021

@author: louis
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox(executable_path="C://Users//louis//Documents//COURS EMSE//Année 5 - Ingé 3//ESME//Web Scrapping//S2//geckodriver.exe")
driver.get("https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html")

cookies = driver.find_element_by_id('_evidon-accept-button')
cookies.click()

i=0
while i <= 10:
    time.sleep(2)
    page_suivante=driver.find_element_by_link_text("Suivant")
    #page_suivante=driver.find_element_by_class_name("nav next rndBtn ui_button primary taLnk")
    page_suivante.click()
    print(i)
    i=i+1

driver.close()


    