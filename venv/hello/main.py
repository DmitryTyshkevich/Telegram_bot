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


class User_registration(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()


@dp.message_handler(Text('Регистрация'), state=None)
async def registr(message: types.Message, state: FSMContext):
    with open('registration_data.json', encoding='utf-8') as f:
        user_data = json.load(f)
    if not str(message.chat.id) in user_data:
        await message.answer('1. Введите имя:', reply_markup=ReplyKeyboardRemove())
        await User_registration.step_1.set()
    else:
        await message.answer('Вы уже зарегистрированы!')
        await state.finish()



@dp.message_handler(state=User_registration.step_1)
async def first_name_input(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text.capitalize())
    await message.answer('Ваше имя сохранено!\n'
                         '2. Введите фамилию: ')

    await User_registration.step_2.set()


@dp.message_handler(state=User_registration.step_2)
async def last_name_input(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text.capitalize())
    await message.answer('Ваша фамилия сохранена!\n'
                         '3. Введите почтовый адрес: ')

    await User_registration.step_3.set()


@dp.message_handler(state=User_registration.step_3)
async def mailing_address_input(message: types.Message, state: FSMContext):
    await state.update_data(mailing_address=message.text)
    await message.answer('Ваша почтовый адрес сохранен!\n'
                         '4. Отправьте фото для Вашего профиля: ')

    await User_registration.step_4.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=User_registration.step_4)
async def load_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    data = await state.get_data()
    with open('registration_data.json', encoding='utf-8') as f:
        user_data = json.load(f)
    user_data[str(message.chat.id)] = data
    with open('registration_data.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)
    await message.answer('Регистрация успешно завершена!', reply_markup=keyboard.start)
    await state.finish()


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


@dp.message_handler(commands=['mailing_list'])
async def mailing_list(message: types.Message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'*Рассылка началась'
                                                f'\nБот оповестит, когда закончит рассылку*',
                               parse_mode=types.ParseMode.MARKDOWN_V2)
        recieve_users, block_users = 0, 0
        with open('user.txt') as file:
            joined_users = set()
            for line in file:
                joined_users.add(line.strip())

            for user in joined_users:
                try:
                    await bot.send_photo(user, open('carl.jpg', 'rb'))
                    recieve_users += 1
                except:
                    block_users += 1
                await asyncio.sleep(0.4)
            await bot.send_message(message.chat.id, f'Рассылка завершена \n'
                                                    f'Сообщение получили: *{recieve_users}* пользователей \n'
                                                    f'Заблокировали бота *{block_users}*',
                                   parse_mode=types.ParseMode.MARKDOWN_V2)


# Обработчик команд с клавиатуры
@dp.message_handler(Text(['Info', 'Литература', "AUDI Class A", 'Статистика']), state=None)
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
        case 'Статистика':
            await message.answer('Хочешь посмотреть статистику бота?', reply_markup=keyboard.in_stats)


@dp.message_handler(Text(['Данные пользователя']))
async def output_logging_data(message: types.Message):
    with open('registration_data.json', encoding='utf-8') as f:
        user_data = json.load(f)
    id = str(message.chat.id)
    if id in user_data:
        await message.answer_photo(user_data[id]["photo"])
        await message.answer(f'Имя: {user_data[id]["first_name"]}\n'
                             f'Фамилия: {user_data[id]["last_name"]}\n'
                             f'Email: {user_data[id]["mailing_address"]}', reply_markup=keyboard.unregistration)

    else:
        await message.answer('Ваш профиль не зарегистрирован!')

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


@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Ботом воспользовалось *{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='У тебя нет админки\n Куда ты полез', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='cancle')
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Ты вернулся в главное меню. Жми опять кнопки', parse_mode='Markdown')

@dp.callback_query_handler(text_contains='delete')
async def del_registration(call: types.CallbackQuery):
    with open('registration_data.json', encoding='utf-8') as f:
        user_data = json.load(f)
    del user_data[str(call.message.chat.id)]
    with open('registration_data.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)
    await call.message.answer('Ваши данные успешно удалены!')
    await call.answer()


if __name__ == '__main__':
    print('Бот запущен!')
    executor.start_polling(dp, skip_updates=True)
