# -*- coding: utf-8 -*-
"""
Created on 04/08/19
Exctracting information from the emc website
@author: Silvia Bardoni 
"""
#Import libraries
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

drugs=[]
emc_n=[]
pages=[1,201,401]  #n. of pages
#Read main page
for n in pages:
    r = requests.get('https://www.medicines.org.uk/emc/browse-medicines?prefix=A&offset='+str(n)+'&limit=200' )
    soup = BeautifulSoup(r.content, "html.parser")
    html_doc = r.text
#    pretty_soup = soup.prettify()
#    print(pretty_soup)
    for h2 in soup.find_all('h2'):
        x= h2.text
        drugs.append(x)
        
        y = h2.a['href']
        emc_n.append('https://www.medicines.org.uk'+y)


df=pd.DataFrame({'drugs':drugs,'link':emc_n})  

    
LegalCat=[]  
for al in range(len(df)):
    x=df.link[al]   
    r = requests.get(x)
    html_doc2 = r.text
    soup2 = BeautifulSoup(html_doc2, 'html.parser')
    pretty_soup2 = soup2.prettify()
    #print(pretty_soup2)
    reference = soup2.find('div', class_="row detail")
    #letter = reference.h3.text
    z = reference.p.text
    #print(test.p)  #one item
    LegalCat.append(z)
    
df['legal']=LegalCat 

base_dir = os.getcwd()
dir_path = os.path.join(base_dir, 'Documents\Data Science\Projects I worked on')
os.chdir(dir_path)     #change directory


df.to_pickle('emc_600')

df.to_csv('A600.csv', index = None)
    
