from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


boshmenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="My shablon"),
            KeyboardButton(text="Namuna")
        ],
        [
            KeyboardButton(text="Sinab ko'rish"),
        ],
        
    ],
    resize_keyboard=True
)


namunastart = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Sinab ko'rish"),
            KeyboardButton(text="Bosh menu")
        ],
        
    ],
    resize_keyboard=True
)


orqaga = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ortga"),
            KeyboardButton(text="Bosh menu")
        ],
        
    ],
    resize_keyboard=True
)

