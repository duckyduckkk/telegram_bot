# -*- coding: utf-8 -*-
import pandas as pd

from config import sites,flags
from config import teams_short_cut as sh

def get_table(country):
    '''Достает с сайта html таблицу команд
    для выбранного чемпионата и конвертирует ее в текст
    с помощью функции normal_table модуля parse_table'''
    url = sites[country]+'table/'
    table = pd.read_html(url, header=0)
    table[1].index += 1 # index starts from 0 by default
    text = table[1].loc[:,['М','О','Команда']].to_string(justify='right')
    table_for_message = normal_table(text)
    
    return(table_for_message)
    
def get_stat(country):
    '''Достает с сайта html таблицу сличной статистикой игроков 
    для выбранного чемпионата и конвертирует ее в текст
    с помощью функции normal_table модуля parse_table'''
    url = sites[country]+'stat/'
    table = pd.read_html(url, header=0)
    table[1].index +=1
    text = table[1].loc[:,['М','Г','П','Имя']].to_string(justify='right',index=False)
    table_for_message = flags[country]+'\n'+normal_stat(text)
    
    return(table_for_message)

def make_league_table(country:str):
    '''Функция которая будет выравнивать строки таблиц  html 
    для отправки телеграмм боту сводной таблицы чемпионата
    country -- наименования чемпионата в формате ключей словаря
               из модуля config'''
               
    url = sites[country]+'table/'
    table_from_url = pd.read_html(url, header=0)
    header = '''№  М  О   Команда {flag}\n'''.format(flag=flags[country])
    list_of_rows = table_from_url[1].loc[:,['Unnamed: 0','М','О','Команда']].values.tolist()
    template = '''{0[0]:02d} {0[1]:02d} {0[2]}  {0[3]}'''
    final_output_table = header+'\n'.join([template.format(i) for i in list_of_rows])
    
    return final_output_table

    
def make_stat_table(country:str):
    '''Функция которая будет выравнивать строки таблиц  html 
    для отправки телеграмм боту таблицы со статистикой игроков
    country -- наименования чемпионата в формате ключей словаря
               из модуля config'''
               
    url = sites[country]+'stat/'
    header = '''№  М  Г   П    Имя {flag}\n'''.format(flag=flags[country])
    table_from_url = pd.read_html(url, header=0)
    list_of_rows = table_from_url[1].loc[:,['Unnamed: 0','М','Г','П','Имя']].values.tolist()
    template = '''{0[0]:02d} {0[1]:02d} {0[2]:02d} {0[3]:02d}  {0[4]}'''
    final_output_stat = header+'\n'.join([template.format(i) for i in list_of_rows])
    
    return final_output_stat
    
def make_schedule_for_next_tour(country):
    '''функция, которая формирует таблицу расписания матчей 
    для отправки телеграм боту 
    country -- наименования чемпионата в формате ключей словаря
               из модуля config'''
    url = sites[country]+'calendar/'
    table_from_url = pd.read_html(url, header=0)
    header = '''Дата{flag}         С    Хоз🏠-Гос🚌\n'''.format(flag=flags[country])
    tours = len(table_from_url[1:])
    
    for i in range(1,tours):
        score_col = table_from_url[i]['Счет'].values.tolist()
        data_col = table_from_url[i]['Дата'].values.tolist()
        if '- : -' in score_col and 'перенесен' not in data_col:
            next_tour = table_from_url[i].loc[:,['Дата','Счет','Хозяева','Гости']]
            future_tour = table_from_url[i+1].loc[:,['Дата','Счет','Хозяева','Гости']]
            schedule = pd.concat([next_tour,future_tour])
            break
        else:
            schedule = table_from_url[tours].loc[:,['Дата','Счет','Хозяева','Гости']]
            
    if 'schedule' not in locals():         #когда только 1 тур на страничке
        schedule = table_from_url[tours].loc[:,['Дата','Счет','Хозяева','Гости']]
        
    schedule['Дата'] = [item[:5]+'|'+item[-5:] if item[:2]!='пе' else item for item in schedule['Дата']]
    schedule['Хозяева'] = [sh[item] if item in sh.keys() else item for item in schedule['Хозяева']]
    schedule['Гости'] = [sh[item] if item in sh.keys() else item for item in schedule['Гости']]
    schedule['Счет'] = [i[0]+':'+i[4] for i in schedule['Счет']]
    list_of_rows = schedule.values.tolist()
    template = template = '''{0[0]} {0[1]} {0[2]}-{0[3]}'''
    
    final_output_schedule = header + '\n'.join([template.format(i) for i in list_of_rows])
    
    return final_output_schedule
