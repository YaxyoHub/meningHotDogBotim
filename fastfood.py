import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dp import get_all_products, get_product_by_id, check_admin

from states import OrderState
from utils import save_order_to_json, load_orders_from_json, clear_user_orders
from keyboards import create_inline_menu
from dotenv import load_dotenv


load_dotenv()
ADMIN_IDs = list(map(int, os.getenv("ADMIN_ID").split(",")))
router = Router()


# /start komandasi
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    result = check_admin(message.from_user.id)
    if not result:
        return await message.answer("⛔ Siz bu botdan foydalana olmaysiz.")
    await message.answer("🍔 Mahsulotni tanlang:", reply_markup=create_inline_menu())
    await state.set_state(OrderState.choosing)

# Mahsulot tanlash
@router.callback_query(F.data.startswith("select_"))
async def handle_product_select(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    prod_id = int(callback.data.split("_")[1])
    await state.update_data(selected_product_id=prod_id)

    name, _ = get_product_by_id(prod_id)
    await callback.message.answer(f"{name} nechta sotdingiz?")
    await state.set_state(OrderState.entering_quantity)
    await callback.answer()

# Miqdorni kiritish
@router.message(OrderState.entering_quantity)
async def enter_quantity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Iltimos, son kiriting.")

    user_id = message.from_user.id
    count = int(message.text)
    data = await state.get_data()
    prod_id = data.get("selected_product_id")

    save_order_to_json(user_id, prod_id, count)
    await message.answer("✅ Qabul qilindi!", reply_markup=create_inline_menu())
    await state.set_state(OrderState.choosing)

# Buyurtmalar ro'yxatini ko'rsatish
@router.callback_query(F.data == 'show_total')
async def show_total_callback(callback: CallbackQuery):
    await callback.message.delete()

    user_id = callback.from_user.id
    orders = load_orders_from_json(user_id)

    if not orders:
        await callback.message.answer("🛒 Hech narsa tanlanmagan.")
    else:
        total_text = "🧾 Buyurtma:\n\n"
        total_price = 0

        for prod_id_str, quantity in orders.items():
            prod_id = int(prod_id_str)
            name, price = get_product_by_id(prod_id)
            summa = price * quantity
            total_text += f"{name} — {quantity} ta = {summa:,} so‘m\n"
            total_price += summa

        total_text += f"\n💰 Umumiy: {total_price:,} so‘m"
        await callback.message.answer(total_text, reply_markup=create_inline_menu())
        clear_user_orders(user_id)

    await callback.answer()

