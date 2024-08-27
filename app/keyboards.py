from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Другой СНИЛС', callback_data='another_number')]])