from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import Admin, DELETEadmin
from dp import check_admin, add_admin_sql, delete_admin_sql

add_admin_router = Router()

admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Admin qo'shish", callback_data="admin_add"),
            InlineKeyboardButton(text="Admin o'chirish", callback_data="admin_del")
        ]
    ]
)


@add_admin_router.message(Command("admin"))
async def adminsss(message: Message):
    result = check_admin(message.from_user.id)
    if not result:
        return await message.answer("⛔ Siz bu botdan foydalana olmaysiz.")
    await message.reply("Admin qo'shish yoki o'chirish", reply_markup=admin_button)

@add_admin_router.callback_query(F.data == "admin_add")
async def add_adminssss(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Admin ismini kiriting:")
    await state.set_state(Admin.admin_name)

@add_admin_router.message(Admin.admin_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(admin_name=message.text)
    await message.answer("Endi admin ID sini kiriting:")
    await state.set_state(Admin.admin_id)

@add_admin_router.message(Admin.admin_id)
async def get_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Admin ID uchun raqam kiriting")
    else:
        admin_idd = int(message.text)
        await state.update_data(admin_id=admin_idd)
        data = await state.get_data()
        add_admin_sql(data['admin_name'], data['admin_id'])
        await message.answer("Admin qo'shildi ✅", reply_markup=admin_button)
        await state.clear()


@add_admin_router.callback_query(F.data == "admin_del")
async def del_adminssss(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Admin ID sini kiriting:")
    await state.set_state(DELETEadmin.admin_id)
    
@add_admin_router.message(DELETEadmin.admin_id)
async def delete_adminssss(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Admin ID uchun raqam kiriting")
        return
    admin_id = int(message.text)
    result = check_admin(admin_id)
    if not result:
        await message.answer("Bunday IDli admin yo'q", reply_markup=admin_button)
    else:
        delete_admin_sql(admin_id)
        await message.answer("Admin o'chirildi ✅", reply_markup=admin_button)
    await state.clear()

    