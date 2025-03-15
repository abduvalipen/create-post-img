from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import MediaGroup
from keyboards.default.klentkey import namunastart, boshmenu, orqaga
from utils.createimg import createshablon_funk
from keyboards.inline.inlinekey import create
import logging
from loader import db, dp
from aiogram.types import CallbackQuery
from .createshablon import Shablon





@dp.message_handler(text="My shablon",state=None)
async def create_shablon(message: types.Message):
    user_id = message.from_user.id
    company = db.select_company(user_id=user_id)
    if company:
        text = f"👨‍💼 Foydalanuvchi {company[1]}\n\n🗂 Loyiha: {company[3]}\n"
        if company[4] == "True":
            text += "⚙️ Holati: activ ✅\n"
        else:
            text += "⚙️ Holati: no activ ❌\n"
        text += f"⏱️ Foydalanish vaqti: {company[5]}\n"
        await message.answer(text, reply_markup=create)
    else:
        msg = f"Siz shablon yaratmagansiz! Yangi shablonlar admin orqali yaratiladi\nAdmin: @tem_uzb\nTel: +998935530337"
        await message.answer(msg)



@dp.callback_query_handler(text="create")
async def create_img_user(call: CallbackQuery):
    user_id = call.from_user.id
    company = db.select_company(user_id=user_id)
    if company[4] == "True":
        await call.message.answer("Elon Idisni kiriting!\nMisol: 22", reply_markup=orqaga)
        await call.message.delete()

        await Shablon.id.set()
    else:
        await call.message.answer("Sizning profilingiz activ emas. Adminga bog'laning!")
        await call.message.delete()


