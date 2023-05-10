from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True)
in_literature = InlineKeyboardMarkup()
in_info = InlineKeyboardMarkup()
buttons_models_audi = InlineKeyboardMarkup(row_width=2)

info = KeyboardButton("Info")  # кнопка информации
stats = KeyboardButton("Литература")
audi_class_a = KeyboardButton("AUDI Class A")
restart = KeyboardButton('/restart')

reference_list = InlineKeyboardButton(text='Открыть список',
                                      callback_data='referencelist')
inline_info = InlineKeyboardButton(text='Получить информацию', callback_data='inlineinfo')

audi_a1 = InlineKeyboardButton(text='AUDI A1', callback_data='AUDI_A1')
audi_a2 = InlineKeyboardButton(text='AUDI A2', callback_data='AUDI_A2')
audi_a3 = InlineKeyboardButton(text='AUDI A3', callback_data='AUDI_A3')
audi_a4 = InlineKeyboardButton(text='AUDI A4', callback_data='AUDI_A4')
audi_a4_allroad = InlineKeyboardButton(text='AUDI A4-ALLROAD', callback_data='AUDI_A4-ALLROAD')
audi_a5 = InlineKeyboardButton(text='AUDI A5', callback_data='AUDI_A5')
audi_a6 = InlineKeyboardButton(text='AUDI A6', callback_data='AUDI_A6')
audi_a6_allroad = InlineKeyboardButton(text='AUDI A6-ALLROAD', callback_data='AUDI_A6-ALLROAD')
audi_a7 = InlineKeyboardButton(text='AUDI A7', callback_data='AUDI_A7')
audi_a8 = InlineKeyboardButton(text='AUDI A8', callback_data='AUDI_A8')

start.add(stats, audi_class_a, info)
start.add(restart)  # добавляем кнопуи в основу бота

in_literature.add(reference_list)
in_info.add(inline_info)

buttons_models_audi.add(audi_a1, audi_a2)
buttons_models_audi.add(audi_a3, audi_a4)
buttons_models_audi.add(audi_a4_allroad, audi_a5)
buttons_models_audi.add(audi_a6, audi_a6_allroad)
buttons_models_audi.add(audi_a7, audi_a8)
