from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    choosing = State()
    entering_quantity = State()
    adding_name = State()
    adding_price = State()
    updating_id = State()
    updating_price = State()
    deleting_id = State()                # 🔹 ID ni kiritish holati
    deleting_confirm_price = State()     # 🔹 Narxni tasdiqlash holati


class UpdateMenu(StatesGroup):
    waiting_id = State()
    waiting_for_price = State()

class Admin(StatesGroup):
    admin_name = State()
    admin_id = State()

class DELETEadmin(StatesGroup):
    admin_id =State()