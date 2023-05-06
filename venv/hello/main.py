from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config  # импортируем файл config
import keyboard  # импортируем файл config keyboard

import logging  # модуль для вывода информации

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


@dp.message_handler(Command("start"), state=None)  # задаем название команды start
async def welcome(message):
    joinedFile = open("user.txt", "r")  # создаем файл в который будем записывать id пользователя
    joinedUsers = set()
    for line in joinedFile:  # цикл, в котором проверяем имеется ли такой id в фале user
        joinedUsers.add(line.strip())
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt", 'a')
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)
    await  bot.send_message(message.chat.id, f'ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ',
                            reply_markup=keyboard.start, parse_mode="Markdown")


if __name__ == '__main__':
    print('Бот запущен!')
    executor.start_polling(dp)
