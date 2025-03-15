from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
from loader import dp, bot
from aiogram.types import MediaGroup
from keyboards.default.klentkey import namunastart, boshmenu, orqaga
from utils.createimg import createshablon_funk
import logging
from loader import db
import os
from handlers.users.start import get_image_file_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "imgs") 


class Shablon(StatesGroup):
    id = State()
    job = State()
    oflayn_in_online = State()
    kompany_name = State()
    salary = State()



@dp.message_handler(text="ortga", state='*')
async def ortga_funk(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    if current_state == "Shablon:id":
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await message.answer("Bosh menu",reply_markup=boshmenu)
    if current_state == "Shablon:job":
        await Shablon.id.set()
        await message.answer("Elon Idisini kiriting!")
    elif current_state == "Shablon:oflayn_in_online":
        await Shablon.job.set()
        await message.answer("Kasb nomini kiriting!")
    elif current_state == "Shablon:kompany_name":
        await Shablon.oflayn_in_online.set()
        await message.answer("Ish shaklini kiriting!\nMisol: oflayn")
    elif current_state == "Shablon:salary":
        await Shablon.kompany_name.set()
        await message.answer("Kompaniya nomini kiriting!")
    



@dp.message_handler(text="Bosh menu",state=None)
async def stateend(message:types.Message):
    await message.answer("Bosh menu",reply_markup=boshmenu)




@dp.message_handler(text="Bosh menu",state='*')
async def stateend(message:types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.answer("Bosh menu",reply_markup=boshmenu)



# @dp.message_handler(text="Namuna")
# async def send_media_group(message: types.Message):
#     files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('1111.png', 'output1.png'))]

#     if not files:
#         await message.answer("Papkada rasm topilmadi.")
#         return

#     # MediaGroup yaratish
#     media_group = MediaGroup()
#     for file in files:
#         file_path = os.path.join(IMAGE_FOLDER, file)
#         media_group.attach_photo(types.InputFile(file_path))

#     # MediaGroupni yuborish
#     await bot.send_media_group(chat_id=message.chat.id, media=media_group)
#     await message.answer(f"1-rasm shablon rasm\n2-rasm natija",reply_markup=namunastart)





@dp.message_handler(text="Namuna")
async def send_media_group(message: types.Message):
    files = []
    for i in db.select_all_example():
        files.append(i[0])
        files.append(i[1])
    
    media = MediaGroup()
    for file in files:
        media.attach_photo(file)


    await bot.send_media_group(chat_id=message.chat.id, media=media)
    await message.answer(f"1-rasm shablon rasm\n2-rasm natija")



@dp.message_handler(text="Sinab ko'rish")
async def start_shablon(message: types.Message):

    await message.answer("Elon Idisni kiriting!\nMisol: 22", reply_markup=orqaga)
    await Shablon.id.set()


@dp.message_handler(state=Shablon.id)
async def elon_id(message: types.Message,state: FSMContext):
    if len(message.text) >= 6:
        await message.answer(
            "Qabul qilinadigan belgilar soni oshib ketti\nMaxsimal belgilar soni 5 ta")
    else:
        id = message.text

        await state.update_data(
            {"id": id}
        )
    
        await message.answer("Kasb nomini kiriting!")
        await Shablon.next()



@dp.message_handler(state=Shablon.job)
async def job_name(message: types.Message,state: FSMContext):
    if len(message.text) >= 31:
        await message.answer(
            "Qabul qilinadigan belgilar soni oshib ketti\nMaxsimal belgilar soni 30 ta\nQaytadan kiriting!")
    else:
        kasb_name = message.text

        await state.update_data(
            {"kasb_name": kasb_name}
        )
    
        await message.answer("Ish shaklini kiriting!\nMisol: oflayn")
        await Shablon.next()


@dp.message_handler(state=Shablon.oflayn_in_online)
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
        await Shablon.next()



@dp.message_handler(state=Shablon.kompany_name)
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
        await Shablon.next()


@dp.message_handler(state=Shablon.salary)
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

        respons = createshablon_funk(id,job,oflayn_or_onlayn,kompany,salarys,chat_id)
        img_file_id = await get_image_file_id(chat_id=chat_id, image_path=respons)

        await message.bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

        db.add_result(user_id=chat_id, user=user, resultimg=img_file_id, date=date)

        
        await state.finish()
