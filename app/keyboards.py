from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

another_number_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Другой СНИЛС', callback_data='another_number')]])

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Карта корпусов', url='https://cchgeu.ru/contacts/karta-korpusov/'),
                                                                          InlineKeyboardButton(text='Как понять расписание?', callback_data='how_understand_schedule')],
                                                                          [InlineKeyboardButton(text='Другой СНИЛС', callback_data='another_number')]])

hide_message_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Скрыть', callback_data='hide_messages')]])