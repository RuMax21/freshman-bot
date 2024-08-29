from aiogram import Bot, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from dotenv import load_dotenv
from os import getenv

from app.states import FreshmanNumber
from utils.search_in_excel import find_user_code_range
from app.keyboards import another_number_keyboard, hide_message_keyboard, menu_keyboard
from utils.number_format import format_number
from consts import DESCRIPTION_SCHEDULE

load_dotenv()
router = Router()

message_ids_for_delete = []

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await message.answer('Введите номер СНИЛС:\n\nXXX-XXX-XXX XX')
    await state.set_state(FreshmanNumber.number)

@router.message(FreshmanNumber.number)
async def input_number(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)

    data = await state.get_data()
    data = format_number(data['number'])
    message_with_data = find_user_code_range(getenv('SRC'), data)

    if message_with_data != 'Уточните номер СНИЛС':
        await message.answer(message_with_data, parse_mode=ParseMode.MARKDOWN, reply_markup=menu_keyboard)
    else:
        await message.answer(message_with_data, parse_mode=ParseMode.MARKDOWN, reply_markup=another_number_keyboard)

    await state.clear()

@router.message()
async def any_message(message: Message) -> None:
    await message.answer('К сожалению, я Вас не понимаю. Для ввода номера СНИЛСа нажмите на кнопку ниже:', reply_markup=another_number_keyboard)

@router.callback_query(F.data == 'another_number')
async def input_another_number(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('Введите номер СНИЛС:\n\nXXX-XXX-XXX XX')
    await state.set_state(FreshmanNumber.number)

@router.callback_query(F.data == 'how_understand_schedule')
async def schedule_description(callback: CallbackQuery) -> None:
    sent_message = await callback.message.answer(text=DESCRIPTION_SCHEDULE[0] + DESCRIPTION_SCHEDULE[1] + DESCRIPTION_SCHEDULE[2] + DESCRIPTION_SCHEDULE[3], parse_mode=ParseMode.MARKDOWN)
    message_ids_for_delete.append(sent_message.message_id)
    sent_message = await callback.message.answer_photo(photo='https://sun9-23.userapi.com/impf/c847217/v847217721/d9e42/e4dfReitHAg.jpg?size=752x123&quality=96&sign=d83d2a1292da0972cd3be2db40bd1500&type=album')
    message_ids_for_delete.append(sent_message.message_id)
    sent_message = await callback.message.answer(text=DESCRIPTION_SCHEDULE[4])
    message_ids_for_delete.append(sent_message.message_id)
    sent_message = await callback.message.answer_photo(photo='https://sun9-77.userapi.com/impf/c847217/v847217721/d9e23/Vy33HZTKkzk.jpg?size=766x127&quality=96&sign=a1b470ff340b35c8e0f38469597fda63&type=album')
    message_ids_for_delete.append(sent_message.message_id)
    sent_message = await callback.message.answer(text=DESCRIPTION_SCHEDULE[5] + DESCRIPTION_SCHEDULE[6], reply_markup=hide_message_keyboard)
    message_ids_for_delete.append(sent_message.message_id)

@router.callback_query(F.data == 'hide_messages')
async def hide_messages(callback_query: CallbackQuery, bot: Bot) -> None:
    for i in range(5):
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id - i)