# -*- coding: utf-8 -*-
import telebot
import requests
import random
import pandas as pd

from telebot import apihelper
from telebot import types

import config # my config
from get_table import get_table,get_stat,make_league_table
from get_table import make_stat_table,make_schedule_for_next_tour



bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('АПЛ 🏴󠁧󠁢󠁥󠁮󠁧󠁿')
    item2 = types.KeyboardButton("Ла Лига 🇪🇸")
    item3 = types.KeyboardButton("Бундес Лига 🇩🇪")
    item4 = types.KeyboardButton("Лига 1 🇫🇷")
    item5 = types.KeyboardButton("Серия А 🇮🇹")
    item6 = types.KeyboardButton("РПЛ 🇷🇺")
    item7 = types.KeyboardButton("Игроки 🙍‍♂️")
    item8 = types.KeyboardButton("Расписание 📅")
    markup.add(item1,item2,item3,item4,item5,item6,item7,item8)
    
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, я умею выводить таблицы чемпионатов топ 5 стран по футболу=).".format(message.from_user, bot.get_me()),
        parse_mode='html',reply_markup = markup)


@bot.message_handler(content_types=['text'])
def lala(message):
    if message.chat.type == 'private':
        if message.text == 'АПЛ 🏴󠁧󠁢󠁥󠁮󠁧󠁿':
            bot.send_message(message.chat.id,make_league_table('АПЛ'),
                parse_mode='MarkDown')
        elif message.text == 'Ла Лига 🇪🇸':
            bot.send_message(message.chat.id,make_league_table('Ла Лига'),
                parse_mode='html')
        elif message.text == 'Бундес Лига 🇩🇪':
            bot.send_message(message.chat.id,make_league_table('Бундес Лига'),
                parse_mode='html')
        elif message.text == 'Лига 1 🇫🇷':
            bot.send_message(message.chat.id,make_league_table('Лига 1'),
                parse_mode='html')
        elif message.text == 'Серия А 🇮🇹':
            bot.send_message(message.chat.id,make_league_table('Серия А'),
                parse_mode='html')
        elif message.text == 'РПЛ 🇷🇺':
            bot.send_message(message.chat.id,make_league_table('РПЛ'),
                parse_mode='html')
        elif message.text == 'Расписание 📅':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Календарь АПЛ 🏴󠁧󠁢󠁥󠁮󠁧󠁿',callback_data='schedule_apl')
            item2 = types.InlineKeyboardButton('Календарь Ла Лиги 🇪🇸',callback_data='schedule_laliga')
            item3 = types.InlineKeyboardButton("Календарь Бундес Лига 🇩🇪",callback_data='schedule_bundes')
            item4 = types.InlineKeyboardButton("Календарь Лига 1 🇫🇷",callback_data='schedule_liga1')
            item5 = types.InlineKeyboardButton("Календарь Серия А 🇮🇹",callback_data='schedule_sereaa')
            item6 = types.InlineKeyboardButton("Календарь РПЛ 🇷🇺",callback_data='schedule_rpl')
            item7 = types.InlineKeyboardButton("Календарь Лиги Чемпионов 🇪🇺",callback_data='schedule_ucl')
            markup.add(item1,item2,item3,item4,item5,item6,item7)
            
            bot.send_message(message.chat.id,'Нажми и получишь расписание ближайших двух туров нужной страны',
                parse_mode='html',reply_markup=markup)        
        elif message.text == 'Игроки 🙍‍♂️':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Игроки АПЛ 🏴󠁧󠁢󠁥󠁮󠁧󠁿',callback_data='player_apl')
            item2 = types.InlineKeyboardButton('Игроки Ла Лиги 🇪🇸',callback_data='player_laliga')
            item3 = types.InlineKeyboardButton("Игроки Бундес Лига 🇩🇪",callback_data='player_bundes')
            item4 = types.InlineKeyboardButton("Игроки Лига 1 🇫🇷",callback_data='player_liga1')
            item5 = types.InlineKeyboardButton("Игроки Серия А 🇮🇹",callback_data='player_sereaa')
            item6 = types.InlineKeyboardButton("Игроки РПЛ 🇷🇺",callback_data='player_rpl')
            item7 = types.InlineKeyboardButton("Игроки Лиги Чемпионов 🇪🇺",callback_data='player_ucl')
            markup.add(item1,item2,item3,item4,item5,item6,item7)
            
            bot.send_message(message.chat.id,'Нажми и получишь статистику игроков нужной страны',
                parse_mode='html',reply_markup=markup)
        else:
            bot.send_message(message.chat.id,'Я не понимаю, чего Вы хотите=(',
                parse_mode='html')
                
                
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'player_apl':
                bot.send_message(call.message.chat.id,make_stat_table('АПЛ'),parse_mode='html')
            elif call.data == 'player_laliga':
                bot.send_message(call.message.chat.id,make_stat_table('Ла Лига'),parse_mode='html')
            elif call.data == 'player_bundes':
                bot.send_message(call.message.chat.id,make_stat_table('Бундес Лига'),parse_mode='html')
            elif call.data == 'player_liga1':
                bot.send_message(call.message.chat.id,make_stat_table('Лига 1'),parse_mode='html')
            elif call.data == 'player_sereaa':
                bot.send_message(call.message.chat.id,make_stat_table('Серия А'),parse_mode='html')
            elif call.data == 'player_rpl':
                bot.send_message(call.message.chat.id,make_stat_table('РПЛ'),parse_mode='html')
            elif call.data == 'player_ucl':
                bot.send_message(call.message.chat.id,make_stat_table('Лига Чемпионов'),parse_mode='html')    
            
            elif call.data == 'schedule_apl':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('АПЛ'),parse_mode='html')
            elif call.data == 'schedule_laliga':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('Ла Лига'),parse_mode='html')
            elif call.data == 'schedule_bundes':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('Бундес Лига'),parse_mode='html')
            elif call.data == 'schedule_liga1':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('Лига 1'),parse_mode='html')
            elif call.data == 'schedule_sereaa':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('Серия А'),parse_mode='html')
            elif call.data == 'schedule_rpl':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('РПЛ'),parse_mode='html')
            elif call.data == 'schedule_ucl':
                bot.send_message(call.message.chat.id,make_schedule_for_next_tour('Лига Чемпионов'),parse_mode='html')

        bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id,text=call.message.text,
                                reply_markup=None)
            
    except Exception as e:
        print(repr(e))

#RUN
bot.polling(none_stop=True)