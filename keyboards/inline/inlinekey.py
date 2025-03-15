from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

til = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇺🇿 uz',callback_data='uz'),
            InlineKeyboardButton(text='🇺🇸 eng',callback_data='en'),
            InlineKeyboardButton(text='🇷🇺 ru',callback_data='ru')
        ],
    ]
)


rek = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text='✅ Ha',callback_data='ha'),
        InlineKeyboardButton(text="❌ Yo'q",callback_data="yuq")
    ],
    ]
)


holat = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text='✅ activ',callback_data='activ'),
        InlineKeyboardButton(text="❌ no activ",callback_data="no activ")
    ],
    [
        InlineKeyboardButton(text='🗄 all jobs',callback_data='alljobs'),
        InlineKeyboardButton(text='⏱️ update m',callback_data='updatemuddat'),
    ],
    [
        InlineKeyboardButton(text='🔙 ortga',callback_data='ortga'),
    ],
    [
        InlineKeyboardButton(text="🥷 admin panel",callback_data="adminpanel")
    ],
    ]
)




create = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text='🛠 create img',callback_data='create'),
    ],
    ]
)