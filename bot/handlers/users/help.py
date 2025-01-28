from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from filters.users import IsGroup,IsBlocked
from filters.admins import IsAdmin

from loader import db,dp,bot

@dp.message_handler(IsGroup())
async def falsereturn(message: types.Message):
    pass

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer("\n".join(text))


from main import do_all
@dp.message_handler(IsAdmin(),commands='yangilash',state='*')
async def new(message: types.Message):
    a = do_all()
    if a:
        await message.answer(text="✅Baza muvaffaqiyatli yangilandi")
    else:
        await message.answer(text="❌Baza yangilanmadi")



@dp.message_handler(IsBlocked())
async def echo(message: types.Message):
    await message.answer(f"<b>🚫Siz botimizdan Blocklangansiz</b>")