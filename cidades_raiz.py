# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 20:11:15 2021

@author: tiago
"""
import logging
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
import pyproj
pyproj.Proj("+init=epsg:4326")

import geopandas as gpd
from shapely.geometry import Point, Polygon

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
###
# END - Configure logs
###

def cidades_raiz(numero_arquivo:int):

    numero_arquivos = 2
    
    df = pd.read_csv(f'cidades_info/city_info{numero_arquivo}.csv') 
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.groupby(['Name',"ID"]).mean().reset_index()
    
    
    
    #kings_county_map.to_crs(epsg=4326).plot()
    df["temp_max_fim"] = df['Lon']
    df["temp_max_inicio"] = df['Lon']
    df["temp_min_fim"] = df['Lon']
    df["temp_min_inicio"] = df['Lon']
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
        
        temp_max_inicio = temp_max[30:].mean()
        temp_max_fim = temp_max[-30:].mean()
        
        temp_min =  df_cidade_mean['tmin']
        temp_min_inicio = temp_min[30:].mean()
        temp_min_fim = temp_min[-30:].mean()
        
        fig = plt.figure(index+numero_arquivo*100)
        plt.plot(date,temp_max,temp_min) 
        plt.savefig(f'saidas/cidades_temp_imagens/{name}.png')
        plt.close(fig)
        
        resultado = temp_max_fim-temp_max_inicio
        df.loc[index,"temp_max_fim"]=temp_max_fim
        df.loc[index,"temp_max_dif"]= resultado if resultado<2 else 2
        
    
    df.to_csv(f'saidas/cidades_temp_result/out{numero_arquivo}.csv', index=False)  
    
    


