from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)




admin_panel_buttons = InlineKeyboardMarkup(row_width=2)
admin_panel_buttons.add(InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"), InlineKeyboardButton(text="🗑 Admin o'chirish", callback_data="delete_admin"))
admin_panel_buttons.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"), InlineKeyboardButton(text="🗑 Kanal o'chirish", callback_data="delete_channel"))
admin_panel_buttons.add(InlineKeyboardButton(text="👨‍👨‍👦‍👦 Adminlar ro'yxati", callback_data="list_admins"), InlineKeyboardButton(text="📎 Kanal va guruhlar ", callback_data="list_channels"))
admin_panel_buttons.add(InlineKeyboardButton(text="✍️ Yangi xabar yuborish", callback_data="send_message"), InlineKeyboardButton(text="📊 Bot statistikasi", callback_data="statistics"))
