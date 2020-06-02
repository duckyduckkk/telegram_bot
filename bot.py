# -*- coding: utf-8 -*-
import telebot
import config # my config
import requests
from telebot import apihelper
from parse_table import normal_table # my parser for table
from telebot import types
import pandas as pd
from get_table import get_table,get_stat


stat = 'https://www.sports.ru/epl/stat/'
table = pd.read_html(stat, header=0)
text = table[1].loc[:,['М','Г','Имя','Команда']].to_string(justify='right',index=False)

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
    item7 = types.KeyboardButton("Игроки")
    markup.add(item1,item2,item3,item4,item5,item6,item7)
    
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, я умею выводить таблицы чемпионатов топ 5 стран по футболу=).".format(message.from_user, bot.get_me()),
        parse_mode='html',reply_markup = markup)


@bot.message_handler(content_types=['text'])
def lala(message):
    if message.chat.type == 'private':
        if message.text == 'АПЛ 🏴󠁧󠁢󠁥󠁮󠁧󠁿':
            bot.send_message(message.chat.id,get_table('АПЛ'),
                parse_mode='html')
        elif message.text == 'Ла Лига 🇪🇸':
            bot.send_message(message.chat.id,get_table('Ла Лига'),
                parse_mode='html')
        elif message.text == 'Бундес Лига 🇩🇪':
            bot.send_message(message.chat.id,get_table('Бундес Лига'),
                parse_mode='html')
        elif message.text == 'Лига 1 🇫🇷':
            bot.send_message(message.chat.id,get_table('Лига 1'),
                parse_mode='html')
        elif message.text == 'Серия А 🇮🇹':
            bot.send_message(message.chat.id,get_table('Серия А'),
                parse_mode='html')
        elif message.text == 'РПЛ 🇷🇺':
            bot.send_message(message.chat.id,get_table('РПЛ'),
                parse_mode='html')
        elif message.text == 'Игроки':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Игроки АПЛ 🏴󠁧󠁢󠁥󠁮󠁧󠁿',callback_data='player_apl')
            item2 = types.InlineKeyboardButton('Игроки Ла Лиги 🇪🇸',callback_data='player_laliga')
            item3 = types.InlineKeyboardButton("Бундес Лига 🇩🇪",callback_data='player_bundes')
            item4 = types.InlineKeyboardButton("Лига 1 🇫🇷",callback_data='player_liga1')
            item5 = types.InlineKeyboardButton("Серия А 🇮🇹",callback_data='player_sereaa')
            item6 = types.InlineKeyboardButton("РПЛ 🇷🇺",callback_data='player_rpl')
            markup.add(item1,item2,item3,item4,item5,item6)
            
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
                bot.send_message(call.message.chat.id,get_stat('АПЛ'),parse_mode='html')
            elif call.data == 'player_laliga':
                bot.send_message(call.message.chat.id,get_stat('Ла Лига'),parse_mode='html')
            elif call.data == 'player_bundes':
                bot.send_message(call.message.chat.id,get_stat('Бундес Лига'),parse_mode='html')
            elif call.data == 'player_liga1':
                bot.send_message(call.message.chat.id,get_stat('Лига 1'),parse_mode='html')
            elif call.data == 'player_sereaa':
                bot.send_message(call.message.chat.id,get_stat('Серия А'),parse_mode='html')
            elif call.data == 'player_rpl':
                bot.send_message(call.message.chat.id,get_stat('РПЛ'),parse_mode='html')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id,text=call.message.text,
                                reply_markup=None)
            
    except Exception as e:
        print(repr(e))
  
#RUN
bot.polling(none_stop=True)