import asyncio

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from keyboards.default.adminKey import adminusers,admincommands, get_company_keyboard
from keyboards.default.klentkey import boshmenu
from keyboards.inline.inlinekey import rek, holat
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
import re

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Namuna(StatesGroup):
    template_img = State()
    result_img = State()
    description = State()
    name = State()



class TestImg(StatesGroup):
    img = State()
    name = State()



class NamunaDelete(StatesGroup):
    name = State()



class TestImgDelete(StatesGroup):
    name = State()



class CompanyAdd(StatesGroup):
    user = State()
    user_id = State()
    loyiha = State()
    muddat = State()
    shablonimg = State()
    resultimg = State()


class CompanyDelete(StatesGroup):
    name = State()
    




class AdminCompany(StatesGroup):
    companyname = State()
    holat_update = State()
    imgsend = State()
    updatemuddat = State()








@dp.callback_query_handler(text="ortga", state='*')
async def ortgainline(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "AdminCompany:holat_update":
        await AdminCompany.companyname.set()
        await call.message.answer("Mavjud loyihalar",reply_markup=get_company_keyboard())
        await call.message.delete()



@dp.message_handler(text="/start", user_id=ADMINS)
async def get_all_users(message: types.Message):

    #await message.answer('admin panel',reply_markup=admincommands)
    await bot.send_message(chat_id=ADMINS[0],text='Siz adminsiz',reply_markup=admincommands)




@dp.message_handler(text="admin panel", user_id=ADMINS)
async def get_all_users(message: types.Message):

    await message.answer('admin panel',reply_markup=adminusers)



@dp.message_handler(text="admin panel",state='*', user_id=ADMINS)
async def get_all_users(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await message.answer('admin panel',reply_markup=adminusers)



@dp.callback_query_handler(text="adminpanel", state='*')
async def ortgainline(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await call.message.answer("admin panel",reply_markup=adminusers)
    await call.message.delete()




@dp.message_handler(text="users", user_id=ADMINS)
async def get_all_users(message: types.Message):
    count = db.count_users()
    users = db.select_all_users()
    text = f"instabot || Foydalanuvchilar soni: {count[0]}\n\n"
    for user in users:
        text+= f"{user[0]}). || {user[2]} || @{user[3]} || {user[1]}\n"
    await message.answer(text)


@dp.message_handler(text="back", user_id=ADMINS)
async def back_button(message: types.Message):

    await message.answer('Bosh menyu',reply_markup=admincommands)




@dp.message_handler(text="Namuna qo'shish")
async def add_db_shablon(message: types.Message):

    await message.answer("Bo'sh shablon rasmni yuboring!")
    await Namuna.template_img.set()


@dp.message_handler(content_types=ContentType.ANY, state=Namuna.template_img)
async def templateimg(message: types.Message,state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1]
        file_id = photo.file_id

        await state.update_data(
            {"file_id_b": file_id}
        )

        await message.answer("Tayyor shablon rasmni yuboring!")

        await Namuna.next()
        
    else:
        await message.answer("Rasm yuboring!!")



@dp.message_handler(content_types=ContentType.ANY, state=Namuna.result_img)
async def templateimg(message: types.Message,state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1]
        file_id = photo.file_id

        await state.update_data(
            {"file_id_t": file_id}
        )

        await message.answer("Deskriptionni kiriting!")

        await Namuna.next()
        
    else:
        await message.answer("Rasm yuboring!!")


@dp.message_handler(state=Namuna.description)
async def job_name(message: types.Message,state: FSMContext):

    description = message.text

    await state.update_data(
            {"description": description}
        )

    
    await message.answer("nomini kiriting!")
    await Namuna.next()




@dp.message_handler(state=Namuna.name)
async def salary_funk(message: types.Message,state: FSMContext):
    name = message.text

    await state.update_data(
        {"name": name}
    )
    
    data = await state.get_data()
    file_id_b = data.get("file_id_b")
    file_id_t = data.get("file_id_t")
    description = data.get("description")
    name = data.get("name")

    db.add_example(template_img=file_id_b,result_img=file_id_t,deskription=description,name=name)

    text  = f"Namuna shablon qo'shildi! Mavjud shablonlar\n\n"
    id = 1
    for i in db.select_all_example():
        text+=f"{id}) {i[3]}\n"
        id=id + 1
    await message.answer(text)
    
    await state.finish()



@dp.message_handler(text="Namuna o'chirish")
async def delete_db_shablon(message: types.Message):

    await message.answer("Nomini kiriting!")
    await NamunaDelete.name.set()



@dp.message_handler(state=NamunaDelete.name)
async def delete_name_shablon(message: types.Message,state: FSMContext):
    name = message.text

    db.delete_example(name=name)

    text  = f"Namuna shablon o'chirildi! Mavjud shablonlar\n\n"
    id = 1
    for i in db.select_all_example():
        text+=f"{id}) {i[3]}\n"
        id=id + 1
    await message.answer(text)

    #await message.answer("O'chirildi", reply_markup=adminusers)
    await state.finish()




@dp.message_handler(text="Namuna all", user_id=ADMINS)
async def bolim(message: types.Message):
    text  = f"Mavjud shablonlar\n\n"
    id = 1
    for i in db.select_all_example():
        text+=f"{id}) {i[3]}\n"
        id=id + 1
    await message.answer(text)




@dp.message_handler(text="Test shablon qo'shish")
async def add_db_testshablon(message: types.Message):

    await message.answer("Bo'sh shablon rasmni yuboring!")
    await TestImg.img.set()



@dp.message_handler(content_types=ContentType.ANY, state=TestImg.img)
async def templateimg(message: types.Message,state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1]
        file_id = photo.file_id

        await state.update_data(
            {"file_id_b": file_id}
        )

        await message.answer("Nomini kiriting!")

        await TestImg.next()
        
    else:
        await message.answer("Rasm yuboring!!")



@dp.message_handler(state=TestImg.name)
async def salary_funk(message: types.Message,state: FSMContext):
    name = message.text

    await state.update_data(
        {"name": name}
    )
    
    data = await state.get_data()
    file_id_b = data.get("file_id_b")
    name = data.get("name")

    db.add_templatetest(test_img=file_id_b,name=name)

    text  = f"Testlash uchun shablon qo'shildi! Mavjud shablonlar\n\n"
    id = 1
    for i in db.select_all_templatetest():
        text+=f"{id}) {i[2]}\n"
        id=id + 1
    await message.answer(text)

    
    await state.finish()



@dp.message_handler(text="Test shablon o'chirish")
async def delete_db_shablon(message: types.Message):

    await message.answer("Nomini kiriting!")
    await TestImgDelete.name.set()



@dp.message_handler(state=TestImgDelete.name)
async def delete_name_shablon(message: types.Message,state: FSMContext):
    name = message.text

    db.delete_templatetest(name=name)

    text  = f"Testlash uchun shablon o'chirildi! Mavjud shablonlar\n\n"
    id = 1
    for i in db.select_all_templatetest():
        text+=f"{id}) {i[2]}\n"
        id=id + 1
    await message.answer(text)

    await state.finish()



@dp.message_handler(text="Test shablon all", user_id=ADMINS)
async def bolim(message: types.Message):
    text  = f"Mavjud shablonlar\n\n"
    id = 1
    for i in db.select_all_templatetest():
        text+=f"{id}) {i[2]}\n"
        id=id + 1
    await message.answer(text)




@dp.message_handler(text="Add new company")
async def add_db_new_company(message: types.Message):

    await message.answer("user ismini kiriting!")
    await CompanyAdd.user.set()



@dp.message_handler(state=CompanyAdd.user)
async def user_namc(message: types.Message,state: FSMContext):

    user_name = message.text

    await state.update_data(
            {"user_name": user_name}
        )

    
    await message.answer("user id sini kiriting!")
    await CompanyAdd.next()




@dp.message_handler(state=CompanyAdd.user_id)
async def user_idc(message: types.Message,state: FSMContext):

    user_id = int(message.text)

    await state.update_data(
            {"user_id": user_id}
        )

    
    await message.answer("Loyiha nomini kiriting!")
    await CompanyAdd.next()



@dp.message_handler(state=CompanyAdd.loyiha)
async def user_loyiha(message: types.Message,state: FSMContext):

    loyiha = message.text

    await state.update_data(
            {"loyiha": loyiha}
        )

    
    await message.answer("Foydalanish muddatini kiriting!")
    await CompanyAdd.next()


@dp.message_handler(state=CompanyAdd.muddat)
async def user_muddat(message: types.Message,state: FSMContext):

    muddat = message.text

    await state.update_data(
            {"muddat": muddat}
        )

    
    await message.answer("Shablon rasmni kiriting!")
    await CompanyAdd.next()




@dp.message_handler(content_types=ContentType.ANY, state=CompanyAdd.shablonimg)
async def shablon_cimg(message: types.Message,state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1]
        file_id = photo.file_id

        await state.update_data(
            {"file_id_sh": file_id}
        )

        await message.answer("Kutilayotgan rasmni rasmni yuboring!")

        await CompanyAdd.next()
        
    else:
        await message.answer("Rasm yuboring!!")



@dp.message_handler(content_types=ContentType.ANY, state=CompanyAdd.resultimg)
async def shablon_rimg(message: types.Message,state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1]
        file_id = photo.file_id


        data = await state.get_data()
        user_name = data.get("user_name")
        user_id = data.get("user_id")
        loyiha = data.get("loyiha")
        muddat = data.get("muddat")
        file_id_sh = data.get("file_id_sh")
        file_id_r = file_id

        db.add_company(user=user_name, user_id=user_id, loyiha=loyiha, holat="False" ,muddat=muddat, shablonimg=file_id_sh, resultimg=file_id_r)

        await message.answer("Companiya qo'shildi!")


        await state.finish()
        
    else:
        await message.answer("Rasm yuboring!!")



@dp.message_handler(text="Delete company")
async def delete_db_shablon(message: types.Message):

    await message.answer("Nomini kiriting!")
    await CompanyDelete.name.set()



@dp.message_handler(state=CompanyDelete.name)
async def delete_name_shablon(message: types.Message,state: FSMContext):
    name = message.text

    db.delete_company(name)

    text  = f"kompaniya o'chirildi! Mavjud kompaniyalar\n\n"
    id = 1
    for i in db.select_all_company():
        text+=f"{id}) {i[3]}\n"
        id=id + 1
    await message.answer(text)

    await state.finish()





@dp.message_handler(text="All company", user_id=ADMINS)
async def bolim(message: types.Message):
    text  = f"Mavjud kompaniyalar\n\n"
    id = 1
    for i in db.select_all_company():
        text+=f"{id}) {i[3]}\n"
        id=id + 1
    await message.answer(text,reply_markup=get_company_keyboard())

    await AdminCompany.companyname.set()




@dp.message_handler(state=AdminCompany.companyname)
async def user_muddat(message: types.Message,state: FSMContext):

    text_message = message.text
    companyname = re.split(r"[✅❌]", text_message)[0].strip()

    loyiha = db.select_company(loyiha=companyname)
    text = generate_project_text(loyiha)

    await message.answer("Kompaniya uchun funksiyalar!", reply_markup=ReplyKeyboardRemove())  

    sent_message = await message.answer(text, reply_markup=holat)
    await state.update_data(
            {"company_name": companyname, "message_id": sent_message.message_id}
        )
    
    await AdminCompany.next()


@dp.callback_query_handler(state=AdminCompany.holat_update)
async def activ_no_activ(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    company_name = data.get("company_name")
    message_id = data.get("message_id") 
    if call.data in ["activ", "no activ"]:
        
        if call.data == 'activ':
            db.update_company_holat(holat="True", loyiha=company_name)
        elif call.data == 'no activ':
            db.update_company_holat(holat="False", loyiha=company_name)
    
        loyiha = db.select_company(loyiha=company_name)
        new_text = generate_project_text(loyiha)

        await call.message.edit_text(new_text, reply_markup=holat)
        await call.answer() 
    elif call.data == "alljobs":
        sendimgb = InlineKeyboardMarkup(row_width=3)
        for img_id, file_id in db.get_company_results(company_name=company_name)[-15:]:
            button = InlineKeyboardButton(text=f"Rasm {img_id}", callback_data=img_id)
            sendimgb.insert(button)
        back_button = InlineKeyboardButton(text="Orqaga", callback_data="imgortga")
        sendimgb.add(back_button)
        await call.message.answer("Quyidagi rasmlardan birini tanlang:", reply_markup=sendimgb)
        await call.message.delete()

        await AdminCompany.next()
    elif call.data == "updatemuddat":
        await call.message.answer("Yangi muddatni kiriting!")
        await call.message.delete()

        await AdminCompany.updatemuddat.set()


        
@dp.message_handler(state=AdminCompany.updatemuddat)
async def answer_fullname(message: types.Message, state: FSMContext):
    habar = message.text
    data = await state.get_data()
    company_name = data.get("company_name")
    db.update_company_muddat(muddat=habar, loyiha=company_name)
    loyiha = db.select_company(loyiha=company_name)
    text = generate_project_text(loyiha)
    await message.answer(text, reply_markup=holat)

    await AdminCompany.holat_update.set()



        
@dp.callback_query_handler(state=AdminCompany.imgsend)
async def send_image(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "imgortga":
        data = await state.get_data()
        company_name = data.get("company_name")
        loyiha = db.select_company(loyiha=company_name)
        text = generate_project_text(loyiha)
        await callback_query.message.answer(text, reply_markup=holat)
        await callback_query.message.delete()
        await AdminCompany.holat_update.set()
    else:
        id = callback_query.data
        file_id = db.select_result(id=id)
        await bot.send_photo(callback_query.message.chat.id, file_id)
    



def generate_project_text(loyiha):
    text = f"{loyiha[3]} loyihasi\n"
    text += f"Foydalanuvchi: {loyiha[1]} | id({loyiha[2]})\n"
    text += f"Loyiha: {loyiha[3]}\n"
    if loyiha[4] == "True":
        text += "Holati: activ ✅\n"
    else:
        text += "Holati: no activ ❌\n"
    text += f"Foydalanish vaqti: {loyiha[5]}\n"
    return text



class Reklama(StatesGroup):
    message = State()




@dp.message_handler(text="reklama",user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer("reklama yuboring")
    await Reklama.message.set()


@dp.message_handler(content_types=ContentType.ANY,state=Reklama.message)
async def answer_fullname(message: types.Message, state: FSMContext):
    habar = message.text

    await state.update_data(
        {"habar": habar}
    )
    data = await state.get_data()
    reklama = data.get("habar")

    msg = reklama
    
    for user in db.select_all_users():
        user_id = user[1]
        try:
            await message.send_copy(chat_id=user_id)
            await asyncio.sleep(0.05)
        except Exception as e:
            await bot.send_message(chat_id=ADMINS[0],text=f"{e}")
    await bot.send_message(chat_id=ADMINS[0],text=f"Reklama yuborildi! ✅")
    await state.finish()


