import os, asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from fastfood import router
from menu_qushish import add_router
from menu_yangilash import update_router
from menu_ochirish import delete_router
from admin_qushish import add_admin_router
from error import error_router

load_dotenv()
TOKEN = os.getenv("bottoken")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(add_router)
    dp.include_router(update_router)
    dp.include_router(delete_router)
    dp.include_router(add_admin_router)
    dp.include_router(error_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("✅ Bot ishga tushdi...")
    asyncio.run(main())
