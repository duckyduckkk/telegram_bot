# -*- coding: utf-8 -*-
def normal_table(raw_table):
    '''Обрабатывает пандас дата фрейм в стринг формате
    Для ровного вывода в телеграм чате'''
    first = raw_table.split('\n')[1:]
    line_width = [4,4,4,20]
    my_format = '№   M   О   Команда\n'
    
    for line in first:
        new_line = line.split()
        if len(new_line) > len(line_width):
            new_line[3]=new_line[3]+' '+new_line[4]
            new_line.remove(new_line[4])
        final_line = ''
        
        for index,element in enumerate(new_line):
            if index == 0:
                if len(element)==1:
                    element=f'0{element}'
            final_line = final_line + element+' '*(line_width[index]-len(element))
        my_format=my_format+final_line+'\n'
        
    return(my_format)


def normal_stat(raw_table):
    '''Обрабатывает пандас дата фрейм(бомбардиров) в стринг формате
    Для ровного вывода в телеграм чате'''
    first = raw_table.split('\n')[1:]
    line_width = [4,4,4,30]
    my_format = 'М   Г    П   Имя\n'
    
    for line in first:
        new_line = line.split()
        while len(new_line) > len(line_width):
            new_line[3]=new_line[3]+' '+new_line[4]
            new_line.remove(new_line[4])
        final_line = ''
        
        for index,element in enumerate(new_line):
            if index in (0,1,2):
                if len(element)==1:
                    element=f'0{element}'
            final_line = final_line + element+' '*(line_width[index]-len(element))
        my_format=my_format+final_line+'\n'
        
    return(my_format)