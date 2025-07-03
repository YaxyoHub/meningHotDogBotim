
from dp import get_all_products
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_inline_menu():
    products = get_all_products()
    
    # Tugmalarni 2 ustunli qatorlarga ajratamiz
    product_buttons = []
    row = []
    for i, (pid, name, _) in enumerate(products, start=1):
        row.append(InlineKeyboardButton(text=name, callback_data=f"select_{pid}"))
        if i % 2 == 0:
            product_buttons.append(row)
            row = []
    if row:  
        product_buttons.append(row)


    product_buttons.append([InlineKeyboardButton(text="🧾 Jami", callback_data="show_total")])
    product_buttons.append([InlineKeyboardButton(text="➕ Menu qo'shish", callback_data="add_menu")])
    product_buttons.append([InlineKeyboardButton(text="🔄 Yangilash", callback_data="update_menu")])
    product_buttons.append([InlineKeyboardButton(text="🗑 Menu o'chirish", callback_data="delete_menu")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=product_buttons)
    return keyboard

def update_menu_kb():
    products = get_all_products()
    
    # Tugmalarni 2 ustunli qatorlarga ajratamiz
    product_buttons = []
    row = []
    for i, (pid, name, _) in enumerate(products, start=1):
        row.append(InlineKeyboardButton(text=name, callback_data=f"update_{pid}"))
        if i % 2 == 0:
            product_buttons.append(row)
            row = []
    if row:  
        product_buttons.append(row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=product_buttons)
    return keyboard

def delete_menu_kb():
    products = get_all_products()
    
    # Tugmalarni 2 ustunli qatorlarga ajratamiz
    product_buttons = []
    row = []
    for i, (pid, name, _) in enumerate(products, start=1):
        row.append(InlineKeyboardButton(text=name, callback_data=f"delete_{pid}"))
        if i % 2 == 0:
            product_buttons.append(row)
            row = []
    if row:  
        product_buttons.append(row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=product_buttons)
    return keyboard


