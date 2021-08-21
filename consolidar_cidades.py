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

def consolidar_cidades():
    crs = {'init':'EPSG:4326'}
    kings_county_map = gpd.read_file('mapas/USA_States.shp')
    kings_county_map.crs = {'init' :'epsg:4326'}
    kings_county_map = kings_county_map.to_crs({'init' :'epsg:4326'}) 
    
    arr=[]
    
    
    for i in range(9):
        df_saida = pd.read_csv(f'saidas/cidades_temp_result/out{i+1}.csv') 
        arr.append(df_saida)
    
    
    df_final = pd.concat(arr)
    
    geometry = [Point(xy) for xy in zip(df_final['Lon'], df_final['Lat'])]
    geo_df = gpd.GeoDataFrame(df_final, 
                          crs = crs, 
                          geometry = geometry)
    
    
    
    fig, ax = plt.subplots(figsize = (10,10))
    plt.xlim(-125, -65)
    plt.ylim(23, 50)
    kings_county_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
    geo_df.plot(column = 'temp_max_fim', ax=ax, cmap = 'rainbow',
                legend = True, legend_kwds={'shrink': 0.7}, 
                markersize = 50)
    ax.set_title('Média Temperatura Máxima ultimos 30 anos')
    plt.savefig('saidas/Temp_Max_Cidades.png')
    
    
    fig, ax = plt.subplots(figsize = (10,10))
    plt.xlim(-125, -65)
    plt.ylim(23, 50)
    kings_county_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
    geo_df.plot(column = 'temp_max_dif', ax=ax, cmap = 'seismic',
                legend = True, legend_kwds={'shrink': 0.7}, 
                markersize = 50)
    ax.set_title('Diferença Temperatura Máxima ultimos 30 anos e primeiros 30 anos')
    plt.savefig('saidas/Dif_Temp_Max_Cidades.png')

