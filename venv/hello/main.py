from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config  # импортируем файл config
import keyboard  # импортируем файл config keyboard

import logging  # модуль для вывода информации
import json
import parser
from asyncio import set_event_loop, new_event_loop

set_event_loop(new_event_loop())  # Устанавливает loop как текущий цикл событий для текущего потока ОС.(для запуска
# модуля с парсером)

storage = MemoryStorage()  # FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)  # хранилище состояний в оперативной памяти

logging.basicConfig(
    # указываем название с логами
    filename='log.txt',
    # указываем уровень логирования
    level=logging.INFO,
    # указываем формат сохранения логов
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s '
           u'[%(asctime)s] %(message)s')


# Обработчик команд "/start" и "/restart"
@dp.message_handler(Command(["start", "restart"]), state=None)  # задаем название команды start
async def welcome(message):
    with open("user.txt", "r") as joinedFile:  # создаем файл в который будем записывать id пользователя
        joinedUsers = set()
        for line in joinedFile:  # цикл, в котором проверяем имеется ли такой id в фале user
            joinedUsers.add(line.strip())
    if not str(message.chat.id) in joinedUsers:  # делаем запись в файл user нового id
        with open("user.txt", 'a') as joinedFile:
            joinedFile.write(str(message.chat.id) + "\n")
            joinedUsers.add(message.chat.id)
    # await  bot.send_message(message.chat.id, f'Здравствуйте, *{message.from_user.first_name},* Bot запущен',
    #                         reply_markup=keyboard.start, parse_mode="Markdown")
    # 2 способ вывода сообщения:
    await message.answer(f'Здравствуйте, {message.from_user.first_name}, Bot запущен',
                         reply_markup=keyboard.start)
    # после проверки и записи выводим сообщение с именем пользователя и отображаем кнопки


# Обработчик команд с клавиатуры
@dp.message_handler(Text(['Info', 'Литература', "AUDI Class A"]), state=None)
async def get_message(message: types.Message):
    match message.text:
        case 'Info':
            await message.answer('Информация о боте:', reply_markup=keyboard.in_info)
        case 'Литература':
            await message.answer('Список полезной литературы для разработчиков на языке Python',
                                 reply_markup=keyboard.in_literature)
        case "AUDI Class A":
            await bot.send_message(message.chat.id, text='Выберите модель:',
                                   reply_markup=keyboard.buttons_models_audi)


# Обработчик инлайн кнопок 'Открыть список' и 'Получить информацию'
@dp.callback_query_handler(text=['referencelist', 'inlineinfo'])
async def inline_reference_list_button_handler(call: types.CallbackQuery):
    match call.data:
        case 'referencelist':
            with open('Список_литературы.txt', encoding='utf-8') as file:
                await call.message.answer(file.read())

        case 'inlineinfo':
            await call.message.answer('Бот создан для изучения фреймворка aiogram')
    await call.answer()


# Обработчик инлайн-кнопок: buttons_models_audi
@dp.callback_query_handler(Text(startswith='AUDI_'))
async def func(call: types.CallbackQuery):
    if call.data in parser.links_per_model:
        for link in parser.links_per_model[call.data]:
            await call.message.answer(link)
        await call.answer()


if __name__ == '__main__':
    print('Бот запущен!')
    executor.start_polling(dp, skip_updates=True)
