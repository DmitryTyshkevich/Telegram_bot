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

literature = '1. Марк Лутц «Изучаем Пайтон»\n2. Эрик Мэтиз «Изучаем Python. Программирование игр, визуализация данных, ' \
             'веб-приложения»\n3. Пол Бэрри «Изучаем программирование на Python»\n4. Эл Свейгарт «Автоматизация рутинных ' \
             'задач с помощью Python. Практическое руководство для начинающих»\n5. Майкл Доусон «Программируем на Python»' \
             '\n6. Зед Шоу «Легкий способ выучить Python»\n7. John M. Zelle «Python Programming:' \
             ' An Introduction to Computer Science»\n8. Дэн Бейдер «Чистый Python. Тонкости программирования для профи»' \
             '\n9. Марк Лутц «Программирование на Python»\n10. Дэвид Бизли, Брайан К. Джонс «Python. Книга рецептов»' \
             '\n11. Франсуа Шолле «Глубокое обучение на Python»\n12. Лучано Рамальо «Python. К вершинам  мастерства»\n' \
             '13. Андреас Мюллер и Сара Гвидо «Введение в машинное обучение с помощью Python. Руководство для ' \
             'специалистов по работе с данными»\n14. Brett Slatkin «Effective Python: 59 Ways to Write Better Python»'

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
    with open("user.txt", "r") as joinedFile:  # создаем файл в который будем записывать id пользователя
        joinedUsers = set()
        for line in joinedFile:  # цикл, в котором проверяем имеется ли такой id в фале user
            joinedUsers.add(line.strip())
    if not str(message.chat.id) in joinedUsers:  # делаем запись в файл user нового id
        with open("user.txt", 'a') as joinedFile:
            joinedFile.write(str(message.chat.id) + "\n")
            joinedUsers.add(message.chat.id)
    await  bot.send_message(message.chat.id, f'ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ',
                            reply_markup=keyboard.start, parse_mode="Markdown")
    # после проверки и записи выводим сообщение с именем пользователя и отображаем кнопки


@dp.message_handler(content_types=['text'], state=None)
async def get_message(message: types.Message):
    match message.text:
        case 'Info':
            await bot.send_message(message.chat.id, text='Информация о боте:',
                                   reply_markup=keyboard.in_buttons2)
        case 'Помощь в обучении':
            await bot.send_message(message.chat.id, text='Список полезной литературы для разработчиков на языке Python',
                                   reply_markup=keyboard.in_buttons)


@dp.callback_query_handler()
async def inline_reference_list_button_handler(call: types.CallbackQuery):
    match call.data:
        case 'referencelist':
            await call.message.answer(literature)
            await call.answer()
        case 'inlineinfo':
            await call.message.answer('Бот создан для изучения фреймворка aiogram')
            await call.answer()



if __name__ == '__main__':
    print('Бот запущен!')
    executor.start_polling(dp, skip_updates=True)
