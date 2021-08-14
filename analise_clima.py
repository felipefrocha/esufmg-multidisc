# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 20:11:15 2021

@author: tiago
"""
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
numero_arquivos = 10
for numero in range(numero_arquivos):
    df = pd.read_csv(f'cidades/file ({numero+1}).csv') 
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.drop(columns=['prcp'])
    df['Date'] = df['Date'].str[0:4]
    df2 = df.groupby(['Date']).mean()
    date = df2.index
    temp_max =  df2['tmax']
    temp_min =  df2['tmin']
    plt.figure(numero)
    plt.plot(date,temp_max,temp_min) 
