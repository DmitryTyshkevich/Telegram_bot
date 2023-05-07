from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True)
in_buttons = InlineKeyboardMarkup()
in_buttons2 = InlineKeyboardMarkup()

info = KeyboardButton("Info")  # кнопка информации
stats = KeyboardButton("Помощь в обучении")

reference_list = InlineKeyboardButton(text='Открыть список',
                                      callback_data='referencelist')
inline_info = InlineKeyboardButton(text='Получить информацию', callback_data='inlineinfo')

start.add(stats, info)  # добавляем кнопуи в основу бота
in_buttons.add(reference_list)
in_buttons2.add(inline_info)
