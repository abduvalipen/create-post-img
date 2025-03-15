from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
from loader import dp, bot
from aiogram.types import MediaGroup
from keyboards.default.klentkey import namunastart, boshmenu, orqaga
from utils.createimg import createshablon_funk
from utils.createtoshish import createshablon_funk_toshish
import logging
from loader import db
import os
from handlers.users.start import get_image_file_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "imgs") 


class ShablonT(StatesGroup):
    job = State()
    oflayn_in_online = State()
    kompany_name = State()
    salary = State()



@dp.message_handler(text="ortga", state='*')
async def ortga_funk(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return        
    if current_state == "ShablonT:job":
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await message.answer("Bosh menu",reply_markup=boshmenu)
        await message.answer("Elon Idisini kiriting!")
    elif current_state == "ShablonT:oflayn_in_online":
        await ShablonT.job.set()
        await message.answer("Kasb nomini kiriting!")
    elif current_state == "ShablonT:kompany_name":
        await ShablonT.oflayn_in_online.set()
        await message.answer("Ish shaklini kiriting!\nMisol: oflayn")
    elif current_state == "ShablonT:salary":
        await ShablonT.kompany_name.set()
        await message.answer("Kompaniya nomini kiriting!")
    


@dp.message_handler(state=ShablonT.job)
async def job_name(message: types.Message,state: FSMContext):
    if len(message.text) >= 31:
        await message.answer(
            "Qabul qilinadigan belgilar soni oshib ketti\nMaxsimal belgilar soni 30 ta\nQaytadan kiriting!")
    else:
        kasb_name = message.text

        await state.update_data(
            {"kasb_name": kasb_name}
        )
    
        await message.answer("Ish shaklini kiriting!\nMisol: Toshkent shahri")
        await ShablonT.next()


@dp.message_handler(state=ShablonT.oflayn_in_online)
async def ofline_in_onlai(message: types.Message,state: FSMContext):
    if len(message.text) >= 31:
        await message.answer(
            "Qabul qilinadigan belgilar soni oshib ketti\nMaxsimal belgilar soni 30 ta\nQaytadan kiriting!")
    else:

        ish_holati = message.text

        await state.update_data(
            {"ish_holati": ish_holati}
        )
    
        await message.answer("Kompaniya nomini kiriting!")
        await ShablonT.next()



@dp.message_handler(state=ShablonT.kompany_name)
async def kompany_name_funk(message: types.Message,state: FSMContext):
    if len(message.text) >= 31:
        await message.answer(
            "Qabul qilinadigan belgilar soni oshib ketti\nMaxsimal belgilar soni 30 ta\nQaytadan kiriting!")
    else:
        kompany_name = message.text

        await state.update_data(
            {"kompany_name": kompany_name}
        )
    
        await message.answer("Oylik maoshn kiriting! majburiy")
        await ShablonT.next()


@dp.message_handler(state=ShablonT.salary)
async def salary_funk(message: types.Message,state: FSMContext):
    if len(message.text) >= 31:
        await message.answer(
            "Qabul qilinadigan belgilar soni oshib ketti\nMaxsimal belgilar soni 30 ta\nQaytadan kiriting!")
    else:
        salary = message.text

        await state.update_data(
            {"salary": salary}
        )
    
        data = await state.get_data()
        id = data.get("id")
        job = data.get("kasb_name")
        oflayn_or_onlayn = data.get("ish_holati")
        kompany = data.get("kompany_name")
        salarys = data.get("salary")
        chat_id = message.from_user.id
        user = message.from_user.first_name
        date = str(message.date)

        waiting_message = await message.answer("⌛️")

        respons = createshablon_funk_toshish(job,oflayn_or_onlayn,salarys, kompany,chat_id)
        img_file_id = await get_image_file_id(chat_id=chat_id, image_path=respons)

        await message.bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

        db.add_result(user_id=chat_id, user=user, resultimg=img_file_id, date=date)

        
        await state.finish()
