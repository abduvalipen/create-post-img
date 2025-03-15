from aiogram import types

from loader import dp
from .createshablon import Shablon


from aiogram.dispatcher import FSMContext




@dp.message_handler(text="ortga", state='*')
async def ortga_funk(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    # print(current_state)
    # print(type(current_state))
    # if current_state == Shablon.job:
    #     await state.finish()
    # elif current_state == Shablon.oflayn_in_online:
    #     await Shablon.job.set()
    # await message.answer(message.text)