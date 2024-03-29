"""
Created on Sat Aug 14 20:11:15 2021

@author: Tiago Lobato
@coauthor: Felipe Rocha
"""
import os
import logging
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
import pyproj
pyproj.Proj("+init=epsg:4326")

import geopandas as gpd
from shapely.geometry import Point, Polygon

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

def consolidar_cidades():
    num_files_in_folder = len(os.listdir('/code/saidas/cidades_temp_result'))
    if num_files_in_folder < 3:
        log.error('Not all files to analyzed yet')
        exit(1)

    log.info('Processing image')

    crs = {'init':'EPSG:4326'}
    kings_county_map = gpd.read_file('mapas/USA_States.shp')
    kings_county_map.crs = {'init' :'epsg:4326'}
    kings_county_map = kings_county_map.to_crs({'init' :'epsg:4326'}) 
    
    arr=[]
    
    log.info('Summarize cities')
    
    for file in os.listdir('/code/saidas/cidades_temp_result'):
        df_saida = pd.read_csv(f'/code/saidas/cidades_temp_result/{file}') 
        arr.append(df_saida)
    
    log.info('Threat summary')
    
    df_final = pd.concat(arr)
    
    geometry = [Point(xy) for xy in zip(df_final['Lon'], df_final['Lat'])]
    geo_df = gpd.GeoDataFrame(df_final, 
                          crs = crs, 
                          geometry = geometry)
    
    log.info('Plot Max Temperature images')
    
    fig, ax = plt.subplots(figsize = (10,10))
    plt.xlim(-125, -65)
    plt.ylim(23, 50)
    kings_county_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
    geo_df.plot(column = 'temp_max_fim', ax=ax, cmap = 'rainbow',
                legend = True, legend_kwds={'shrink': 0.7}, 
                markersize = 50)
    ax.set_title('Média Temperatura Máxima ultimos 30 anos')
    plt.savefig('saidas/Temp_Max_Cidades.png')
    
    log.info('Plot Delta Temperature images')
    
    fig, ax = plt.subplots(figsize = (10,10))
    plt.xlim(-125, -65)
    plt.ylim(23, 50)
    kings_county_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
    geo_df.plot(column = 'temp_max_dif', ax=ax, cmap = 'seismic',
                legend = True, legend_kwds={'shrink': 0.7}, 
                markersize = 50)
    ax.set_title('Diferença Temperatura Máxima ultimos 30 anos e primeiros 30 anos')
    plt.savefig('saidas/Dif_Temp_Max_Cidades.png')

    log.info('End Process')

