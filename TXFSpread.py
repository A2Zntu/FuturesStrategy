# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:28:00 2020

@author: 0010824
"""

import os 
import pandas as pd 
import matplotlib.pyplot as plt 
from TW_date_func import bool_switchContract, get_nearbyTXF_code,  get_valid_datesRange, get_valid_dates_count
from datetime import datetime, timedelta, date
import datetime as dt  
import matplotlib.font_manager as font_manager
work_dir = os.getcwd()
file_path = os.path.join(work_dir, 'Data')

#設定中文字
font_path = os.path.join(work_dir, 'tools', 'msjh.ttc')
font = font_manager.FontProperties(fname= font_path,
                                   weight='bold',
                                  
                                   style='normal', size=16)


df_TXF = pd.read_csv(os.path.join(file_path, "台指期近遠月.csv"), index_col=False, encoding = 'cp950') 
df_TXF['遠近月收盤價差'] = df_TXF['遠月收盤價'] - df_TXF['近月收盤價']
df_TXF['時間'] = pd.to_datetime(df_TXF['時間'])

list_nearbycodes = [] 
for i in range(len(df_TXF)): 
    dd = dt.datetime.strftime(df_TXF['時間'][i], "%Y%m%d")
    list_nearbycodes.append(get_nearbyTXF_code(dd))

    
df_TXF['NearbyCode'] = list_nearbycodes

list_settledays = []
for i in range(1, len(df_TXF)): 
    if df_TXF['NearbyCode'][i] != df_TXF['NearbyCode'][i-1]:
        list_settledays.append(df_TXF['時間'][i])

df_TXF.to_csv(os.path.join(work_dir, 'TXFSpread.csv'), encoding='utf_8_sig', index=False)

        
#畫圖
       
plt.style.use('ggplot')
plt.figure(figsize=(20,10))

tradeDate = df_TXF['時間'][64:]
spread = df_TXF['遠近月收盤價差'][64:]
title_name = '台指期遠近月收盤價差'

plt.plot(tradeDate, spread, color = 'black', marker='o',  markersize=4)
for dd in list_settledays[4:]:
    plt.axvline(dd, ls='--')
plt.title(title_name, fontproperties=font)
plt.ylabel('價差', fontsize=14, fontproperties=font)
plt.xlabel('日期', fontsize=14, fontproperties=font)
file_name = 'Spread'
mydir = os.path.join(os.getcwd(), 'Graph',  datetime.now().strftime('%Y%m%d_%H%M'))
if not os.path.exists(mydir): 
    os.makedirs(mydir)
plt.savefig(os.path.join(mydir, file_name))
plt.show()