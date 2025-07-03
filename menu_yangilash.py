from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states import UpdateMenu
from keyboards import update_menu_kb, create_inline_menu
from dp import update_menu_sql

update_router = Router()

# Menyuni yangilash (to‘g‘rilangan)
@update_router.callback_query(F.data == "update_menu")
async def update_menu_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "🆔 Qaysi menyuni yangilamoqchisiz? Tanlang:",
        reply_markup=update_menu_kb() 
    )
    await state.set_state(UpdateMenu.waiting_id)  # bu qatorni qo'shamiz
    await callback.answer()


@update_router.callback_query(F.data.startswith("update_"), UpdateMenu.waiting_id)
async def update_menu(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.split("_")[1])
    await state.update_data(waiting_id=pid)
    await callback.message.answer("Iltimos menu uchun yangilangan narx kiriting:")
    await state.set_state(UpdateMenu.waiting_for_price)

@update_router.message(UpdateMenu.waiting_for_price)
async def get_price(msg: Message, state: FSMContext):
    await state.update_data(waiting_for_price=msg.text)
    data = await state.get_data()
    update_menu_sql(data['waiting_id'], data['waiting_for_price'])
    await msg.answer("Menu yangilandi ✅", reply_markup=create_inline_menu())
    await state.clear()