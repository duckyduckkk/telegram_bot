import pandas as pd
from parse_table import normal_table,normal_stat
from config import sites
from config import flags


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
