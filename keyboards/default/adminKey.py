from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from loader import db

admincommands = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="admin panel"),
            KeyboardButton(text="Namuna")
        ],
        [
            KeyboardButton(text="Sinab ko'rish")
        ],
        
        
    ],
    resize_keyboard=True
)

adminusers = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="users"),
        ],
        [
            KeyboardButton(text="Namuna qo'shish"),
            KeyboardButton(text="Namuna o'chirish"),
            KeyboardButton(text="Namuna all"),
        ],
        [
            KeyboardButton(text="Test shablon qo'shish"),
            KeyboardButton(text="Test shablon o'chirish"),
            KeyboardButton(text="Test shablon all"),
        ],
        [
            KeyboardButton(text="Add new company"),
            KeyboardButton(text="Delete company"),
            KeyboardButton(text="All company"),
        ],
        [
            KeyboardButton(text="reklama"),
        ],
        [
            KeyboardButton(text="back")
        ],
    ],
    resize_keyboard=True
)




def get_company_keyboard():
    company_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for item in db.select_all_company():
        status = "✅" if item[4] == "True" else "❌"
        company_keyboard.add(KeyboardButton(text=f"{item[3]} {status}"))

    company_keyboard.add(KeyboardButton(text="admin panel"))
    
    return company_keyboard


