from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from keyboards import delete_menu_kb, create_inline_menu
from dp import delete_menu_sql, check_admin

delete_router = Router()

@delete_router.callback_query(F.data == "delete_menu")
async def delete_cmd(callback: CallbackQuery):
    result = check_admin(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer("Qaysi menuni o'chirmoqchisiz?", reply_markup=delete_menu_kb())

@delete_router.callback_query(F.data.startswith("delete_"))
async def update_menu(callback: CallbackQuery):
    await callback.answer("Menu o'chirildi ✅", show_alert=True)
    await callback.message.delete()
    pid = int(callback.data.split("_")[1])
    delete_menu_sql(pid)
    await callback.message.answer("Marhamat", reply_markup=create_inline_menu())
