from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states import OrderState
from keyboards import create_inline_menu
from dp import add_menu

add_router = Router()

# Yangi menu qo‘shish
@add_router.callback_query(F.data == "add_menu")
async def add_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("📝 Yangi menu nomini kiriting:")
    await state.set_state(OrderState.adding_name)
    await callback.answer()

@add_router.message(OrderState.adding_name)
async def add_menu_name(message: Message, state: FSMContext):
    await state.update_data(new_menu_name=message.text.strip())
    await message.answer("💰 Narxini kiriting:")
    await state.set_state(OrderState.adding_price)

@add_router.message(OrderState.adding_price)
async def add_menu_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Iltimos, narxni raqamda kiriting.")

    data = await state.get_data()
    name = data.get("new_menu_name")
    price = int(message.text.strip())

    result = add_menu(name, price)
    await message.answer(result, reply_markup=create_inline_menu())
    await state.set_state(OrderState.choosing)