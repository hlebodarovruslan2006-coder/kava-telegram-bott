from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Настройки ---
TOKEN = "8569668451:AAEzn_ObGbnc-UeY-x2JJyn4t2y3V_-X_U"
ADMIN_CHAT_ID = 687268108
PHONE_LINK = "https://wa.me/79516382727"
INSTAGRAM_LINK = "https://www.instagram.com/kavakids03?igsh=MTVlb2p0dzM5cDBwdA%3D%3D&utm_source=qr"

# --- Меню ---
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Коляски", callback_data='menu_strollers')],
        [InlineKeyboardButton("Качели", callback_data='menu_swings')],
        [InlineKeyboardButton("Весы и шезлонг", callback_data='menu_scales')],
        [InlineKeyboardButton("📞 WhatsApp/Телефон: 89516382727", url=PHONE_LINK)],
        [InlineKeyboardButton("📷 Инстаграм", url=INSTAGRAM_LINK)]
    ])

strollers_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("BABALO — 1300 ₽/неделя, 2700 ₽/месяц", callback_data='order_BABALO')],
    [InlineKeyboardButton("⬅️ Главное меню", callback_data='back_main')]
])

swings_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("AMAROBABY — 1000 ₽/неделя, 1600 ₽/месяц", callback_data='order_AMAROBABY')],
    [InlineKeyboardButton("4MOMS — 1500 ₽/неделя, 3000 ₽/месяц", callback_data='order_4MOMS')],
    [InlineKeyboardButton("BABYTON — 700 ₽/неделя, 1400 ₽/месяц", callback_data='order_BABYTON')],
    [InlineKeyboardButton("⬅️ Главное меню", callback_data='back_main')]
])

scales_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("ВЕСЫ — 600 ₽/неделя, 1300 ₽/месяц", callback_data='order_ВЕСЫ')],
    [InlineKeyboardButton("ШЕЗЛОНГ — 700 ₽/неделя, 1400 ₽/месяц", callback_data='order_ШЕЗЛОНГ')],
    [InlineKeyboardButton("⬅️ Главное меню", callback_data='back_main')]
])

# --- Функции ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите категорию или действие:", reply_markup=get_main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_strollers":
        await query.edit_message_text("Выберите модель коляски:", reply_markup=strollers_menu)
    elif data == "menu_swings":
        await query.edit_message_text("Выберите модель качели:", reply_markup=swings_menu)
    elif data == "menu_scales":
        await query.edit_message_text("Выберите модель:", reply_markup=scales_menu)
    elif data.startswith("order_"):
        user = query.from_user
        product_name = data.replace("order_", "")
        price_map = {
            "BABALO": "1300 ₽/неделя, 2700 ₽/месяц",
            "AMAROBABY": "1000 ₽/неделя, 1600 ₽/месяц",
            "4MOMS": "1500 ₽/неделя, 3000 ₽/месяц",
            "BABYTON": "700 ₽/неделя, 1400 ₽/месяц",
            "ВЕСЫ": "600 ₽/неделя, 1300 ₽/месяц",
            "ШЕЗЛОНГ": "700 ₽/неделя, 1400 ₽/месяц"
        }
        price = price_map.get(product_name, "")
        product_text = f"{product_name} — {price}"

        # Отправка админу
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🛒 Новый заказ\nОт: @{user.username or user.first_name}\nТовар: {product_text}"
        )

        # Ответ пользователю
        await query.edit_message_text(
            f"✅ Вы выбрали: {product_text}\nМенеджер свяжется с вами.",
            reply_markup=get_main_menu()
        )
    elif data == "back_main":
        await query.edit_message_text("Главное меню:", reply_markup=get_main_menu())

# --- Основная логика ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__== "__main__":
    main()
