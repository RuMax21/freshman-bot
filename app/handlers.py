from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from dotenv import load_dotenv
from os import getenv

from app.states import FreshmanNumber
from utils.search_in_excel import find_user_code_range
from app.keyboards import keyboard
from utils.number_format import format_number

load_dotenv()
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await message.answer('🎉 Приветствуем тебя, дорогой первокурсник! 🎉\n\nДля просмотра необходимой информации по ВУЗу необходимо ввести номер СНИЛСа:\n\nXXX-XXX-XXX XX')
    await state.set_state(FreshmanNumber.number)

@router.message(FreshmanNumber.number)
async def input_number(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)

    data = await state.get_data()
    data = format_number(data['number'])
    message_with_data = find_user_code_range(getenv('SRC'), data)

    await message.answer(message_with_data, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    await state.clear()

@router.message()
async def any_message(message: Message) -> None:
    await message.answer('К сожалению, я Вас не понимаю. Для ввода номера СНИЛСа нажмите на кнопку ниже:', reply_markup=keyboard)

@router.callback_query(F.data == 'another_number')
async def input_another_number(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('Введите номер СНИЛС:\n\nXXX-XXX-XXX XX')
    await state.set_state(FreshmanNumber.number)