# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 15:44:44 2020

@author: 0010824
"""


import datetime as dt 
from workalendar.asia import Taiwan
import calendar
import pandas as pd 
from pandas.tseries.offsets import BDay
import copy


def bool_switchContract(date: str): 
    '''
    檢查date是否過了當月的結算日，若有則True，若無則False
    '''
    dd = dt.datetime.strptime(date, "%Y%m%d")

    c = calendar.Calendar(firstweekday=calendar.SATURDAY)
    monthcal = c.monthdatescalendar(dd.year, dd.month)
    
    # 處理第一個禮拜weekday為假日，可能導致期貨結算日為第四個禮拜三的問題
    firstweek = monthcal[0]
    week_sum = sum(1 for d in firstweek if d.month == dd.month)
    
    Cnt = 0 
    for i in range(-1, -1-week_sum, -1): #從禮拜5蹈禮拜1
        if Check_date_is_holiday(dt.datetime.strftime(firstweek[i], "%Y%m%d")): 
            Cnt += 1
    
    if Cnt == week_sum:         
        monthly_expire_date = monthcal[3][-3]
    else: 
        monthly_expire_date = monthcal[2][-3]     
        
    if dd.date() >= monthly_expire_date: 
        return True
            
    return False

def Check_date_is_holiday(date: str): 
    '''
    判斷該天是否為假日，但若是台灣補假(deffered holidays)要自己補
    '''
    D = dt.datetime.strptime(date, "%Y%m%d").date()
    Year = D.year
    cal = Taiwan()
    cal_holidays = cal.holidays(Year)
    cal_holidays.append((dt.datetime(2020, 5, 1).date(), 'deffered Holidays'))
    cal_holidays.append((dt.datetime(2020, 6, 25).date(), 'deffered Holidays'))
    cal_holidays.append((dt.datetime(2020, 6, 26).date(), 'deffered Holidays'))
    cal_holidays.append((dt.datetime(2020, 10, 2).date(), 'deffered Holidays'))
    cal_holidays.append((dt.datetime(2020, 10, 9).date(), 'deffered Holidays'))
    for holiday in cal_holidays:
        if D == holiday[0]:
            return True
    return False

def get_nearbyTXF_code(date: str): 
    D = dt.datetime.strptime(date, "%Y%m%d").date()
    month = D.month
    year = D.year
    tmpS1 = 'TXF'
    if bool_switchContract(date):
        tmpS2 = chr(65 + month)
    else: 
        tmpS2 = chr(64 + month)
    
    tmpS3 = str(year%10)
    if tmpS2 == 'M': #到了12月換月日
        tmpS2 = 'A'
        tmpS3 = str((year + 1)%10) 
        
    S = tmpS1 + tmpS2 + tmpS3
    return S

def get_datesRange(startDate: str, endDate: str): 
    '''
    Parameters
    ----------
    startDate : str
        
    endDate : str
        
    Returns
    -------
    datesStrList : List
        回傳日期的區間

    '''
    assert endDate >= startDate
    datesList = pd.date_range(startDate, endDate, freq=BDay()).date
    datesStrList = [str(ele).replace("-", "") for ele in datesList]
    return datesStrList

def get_valid_datesRange(startDate: str, endDate: str): 
    datesList = get_datesRange(startDate, endDate)
    new_datesList = copy.deepcopy(datesList)
    for thisday in datesList: 
        if  Check_date_is_holiday(thisday): 
            new_datesList.remove(thisday)
    return new_datesList

def get_valid_dates_count(startDate: str, endDate: str): 
    dateList = get_valid_datesRange(startDate, endDate)
    return len(dateList) - 1

if __name__ == '__main__':
    list_dates = get_valid_datesRange('20200501', '20201007')
    dateCnt = get_valid_dates_count('20200507', '20200506')
    list_fut_code = []
    for ds in list_dates: 
        list_fut_code.append(get_nearbyTXF_code(ds))
    df = pd.DataFrame()
    df['dates'] = list_dates
    df['TXF'] = list_fut_code
    print(df)


