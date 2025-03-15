import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.inlinekey import til
from keyboards.default.klentkey import boshmenu



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    chat_id = message.from_user.id
    username = message.from_user.username
    fulname = message.from_user.first_name
    date = str(message.date)
    try:
        db.add_user(chat_id=chat_id,first_name=fulname,username=username,date=date)
        for admin in ADMINS:
            await bot.send_message(chat_id=admin,text=f" {message.from_user.first_name} bazaga qoshildi")
    except sqlite3.IntegrityError as err:
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=err)


    await message.answer(f"Assalomu alaykum!", reply_markup=boshmenu)




async def get_image_file_id(chat_id: int, image_path: str) -> str:
    with open(image_path, 'rb') as photo:
        message = await bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=boshmenu)
    file_id = message.photo[-1].file_id


    return file_id