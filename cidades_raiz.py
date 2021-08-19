# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 20:11:15 2021

@author: tiago
"""
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
numero_arquivos = 2

df = pd.read_csv(f'cidades_raiz/city_info.csv') 
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.groupby(['Name',"ID"]).mean().reset_index()

for index, row in df.iterrows():
    name = row["Name"]
    id_cidade = row["ID"]
    df_cidade = pd.read_csv(f'cidades_raiz/{id_cidade}.csv') 
    
    df_cidade = df_cidade.loc[:, ~df_cidade.columns.str.contains('^Unnamed')]
    df_cidade = df_cidade.drop(columns=['prcp'])
    
    df_cidade['Date'] = df_cidade['Date'].str[0:4]
    df_cidade_mean = df_cidade.groupby(['Date']).mean()
    date = df_cidade_mean.index
    temp_max =  df_cidade_mean['tmax']
    temp_min =  df_cidade_mean['tmin']
    plt.figure(index)
    plt.plot(date,temp_max,temp_min) 


