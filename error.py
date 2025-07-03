from aiogram import F, Router
from aiogram.types import Message

error_router = Router()

@error_router.message(F.text)
async def error_hand(msg: Message):
    await msg.answer("Iltimos botga to'g'ridan-to'g'ri xabar yubormang ⚠️")