from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime
from aiogram.utils.markdown import code


from translator import translate
from database import DataBase
from keyboards import (
    admin_panel_buttons,
)


bot = Bot(token="6045023367:AAGlf55XrAHwKj8iLS8dpkg9p3tNdWdM1lw")
dp  = Dispatcher(bot=bot)
db  = DataBase()

async def check_one_channel(channel, user):
    try:
        is_member = await bot.get_chat_member(
            chat_id=channel,
            user_id=user,
        )
        if is_member["status"] != "left":
            return "true"
        return "false"
    except:
        return "error"
    
async def check_all_channels(user):
    for channel in db.get_channels():
        checker = await check_one_channel(channel=channel[0], user=user)
        if checker == "true":
            continue
        else:
            return False
    return True


@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    now = datetime.now()
    if not db.get_user(message.from_user.id):
        db.add_user(message.from_user.id, False, now.strftime("%d/%m/%Y"))
    if await check_all_channels(user=message.from_user.id):
        db.update_user(message.from_user.id)
        await message.answer("Salom")
    else:
        channels_inline_button = types.InlineKeyboardMarkup(row_width=1)
        for channel in db.get_channels():
            channels_inline_button.add(types.InlineKeyboardButton(text=f"{channel[0]}", url=f"t.me/{channel[0][1::]}"))
        await message.answer("Xurmatli foydalanuvchi botimizdan foydalanish uchun quyidagi kannallarimizga obuna bo'lganligingizni tekshirib ko'ring.", reply_markup=channels_inline_button)

@dp.message_handler(commands=['admin'])
async def admin_panel_handler(message: types.Message):
    is_admin = db.get_admin(message.from_user.id)
    if is_admin:
        await message.answer(f"Salom {message.from_user.first_name}! Admin panelga xush kelibsiz.", reply_markup=admin_panel_buttons)
    else:
        await message.answer("Kechirasiz! Sizga tegishli bo'lmagan buyruqdan foydalanayabsiz!")


@dp.callback_query_handler(text="add_admin")
async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Botga quyidagi buyruqni yuboring ```text @add_admin <admin_telegram_id>```", parse_mode="markdown")


@dp.callback_query_handler(text="delete_admin")
async def delete_admin(call: types.CallbackQuery):
    await call.message.answer("Botga quyidagi buyruqni yuboring ```text @del_admin <admin_telegram_id>```", parse_mode="markdown")

@dp.callback_query_handler(text="add_channel")
async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Botga quyidagi buyruqni yuboring ```text @add_channel @channel```", parse_mode="markdown")


@dp.callback_query_handler(text="delete_channel")
async def delete_admin(call: types.CallbackQuery):
    await call.message.answer("Botga quyidagi buyruqni yuboring ```text @del_channel @channel```", parse_mode="markdown")

@dp.callback_query_handler(text="send_message")
async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Xabarni kiriting", parse_mode="markdown")

@dp.callback_query_handler(text="list_admins")
async def list_admins(call: types.CallbackQuery):
    text = ""
    for i in db.get_admins():
        text += f"{code(str(i[0]))}\n"
    await call.message.answer(text)

@dp.callback_query_handler(text="list_channels")
async def list_admins(call: types.CallbackQuery):
    text = ""
    for i in db.get_channels():
        text += f"{i[0]}\n"
    await call.message.answer(text)

@dp.callback_query_handler(text="statistics")
async def delete_admin(call: types.CallbackQuery):
    await call.message.answer(f"""
Foydalanuvchilar soni: {len(db.get_all_users())}
Aktiv foydalanuvchilar: {len(list(db.get_users()))}
Kanallar: {len(list(db.get_channels()))}
Adminlar: {len(list(db.get_admins()))}
""", parse_mode="markdown")



@dp.message_handler(content_types=types.ContentType.ANY)
async def text_handler(message: types.Message):
    if message.chat.type == "private":
        if await check_all_channels(user=message.from_user.id):
            db.update_user(message.from_user.id)
            try:
                is_admin = db.get_admin(message.from_user.id)
                if is_admin:
                    if message.text:
                        if message.text.split()[0] == "@add_admin":
                            r = db.add_admin(message.text.split()[1])
                            if r:
                                await message.answer("Admin qo'shildi!")
                            else:
                                await message.answer("Bu admin mavjud")
                        elif message.text.split()[0] == "@del_admin":
                            r = db.delete_admin(message.text.split()[1])
                            if r:
                                await message.answer("Admin o'chirildi!")
                            else:
                                await message.answer("Bunday admin mavjud emas")
                        elif message.text.split()[0] == "@add_channel":
                            try:
                                channel = message.text.split()[1] if "@" in message.text.split()[1] else "@" + message.text.split()[1]
                                await bot.get_chat_administrators(channel)
                                r = db.add_channel(channel)
                                if r:
                                    await message.answer("Kanal qo'shildi")
                                else:
                                    await message.answer("Bu kanal mavjud")
                            except Exception as e:
                                print(e)
                                await message.answer("Bu kanal mavjud emas yoki bot bu kanal admini emas.")
                        elif message.text.split()[0] == "@del_channel":
                            r = db.delete_channel(message.text.split()[1])
                            if r:
                                await message.answer("Kanal o'chirildi")
                            else:
                                await message.answer("Bunday kanal mavjud emas")
                        else:
                            for user in db.get_users():
                                try:
                                    await bot.copy_message(
                                        chat_id=user[0],
                                        from_chat_id=message.from_user.id,
                                        message_id=message.message_id,
                                    )
                                except:
                                    pass
                    else:
                        for user in db.get_users():
                            await bot.copy_message(
                                chat_id=user[0],
                                from_chat_id=message.from_user.id,
                                message_id=message.message_id,
                            )
                else:
                    trans = translate(message.text)
                    en = trans["en"]
                    uz = trans["uz"]
                    await message.answer(f"""
    🇬🇧 {code(en)}

    🇺🇿 {code(uz)}
                """, parse_mode="markdown")
            except Exception as e:
                print(e)
        else:
            channels_inline_button = types.InlineKeyboardMarkup(row_width=1)
            for channel in db.get_channels():
                channels_inline_button.add(types.InlineKeyboardButton(text=f"{channel[0]}", url=f"t.me/{channel[0][1::]}"))
            await message.answer("Xurmatli foydalanuvchi botimizdan foydalanish uchun quyidagi kannallarimizga obuna bo'lganligingizni tekshirib ko'ring.", reply_markup=channels_inline_button)


executor.start_polling(dispatcher=dp, skip_updates=True)
