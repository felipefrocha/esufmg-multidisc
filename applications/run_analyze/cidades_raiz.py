# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 20:11:15 2021

@author: tiago
@coauthor: Felipe Rocha
"""
import os
import logging
import pyproj
import pandas as pd
import numpy as np 
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon


pyproj.Proj("+init=epsg:4326")

###
# Configure logs
###
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
###
# END - Configure logs
###

def process_city(file_name:str):

    log.info(f'File founded - /code/cidades_info/{file_name}')
    df = pd.read_csv(f'/code/cidades_info/{file_name}') 

    
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
    
        if not os.path.isdir("/code/cidades_raiz"):
            log.info(os.listdir('/code/cidades_raiz/'))
            exit(1)

        df_cidade = pd.read_csv(f'/code/cidades_raiz/{id_cidade}.csv') 
        
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
        
        fig = plt.figure(index)
        plt.plot(date,temp_max,temp_min) 
        plt.savefig(f'/code/saidas/cidades_temp_imagens/{name}.png')
        plt.close(fig)
        
        resultado = temp_max_fim-temp_max_inicio
        df.loc[index,"temp_max_fim"]=temp_max_fim
        df.loc[index,"temp_max_dif"]= resultado if resultado<2 else 2
        
    
    df.to_csv(f'/code/saidas/cidades_temp_result/{file_name}', index=False)  
    
    


