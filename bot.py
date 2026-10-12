import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    WebAppInfo, 
    MenuButtonWebApp
)
from aiohttp import web

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_USERNAME = "NURSULTON_VIBE"  # Sizning Telegram lichkangiz

bot = Bot(token=TOKEN)
dp = Dispatcher()

WEBAPP_URL = "https://non-savdo-online.vercel.app/"

# Pastki menyu klaviaturasi
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🥐 Menuni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="🥖 Non narxlari"), KeyboardButton(text="📞 Aloqa")],
        [KeyboardButton(text="ℹ️ Biz haqimizda"), KeyboardButton(text="👨‍💼 Admin")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Bo'limni tanlang..."
)

# Admin lichkasiga o'tuvchi Inline tugma (Kanal emas!)
admin_inline_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💬 Admin Lchkasi (@NURSULTON_VIBE)", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    try:
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(
                text="🥐 Menuni ochish",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
    except Exception as e:
        print(f"Menu button error: {e}")

    await message.answer(
        f"Assalomu alaykum, **{message.from_user.first_name}**! 👋\n\n"
        f"🥖 **Nonchi Aka** nonvoyxonasining rasmiy botiga xush kelibsiz.\n"
        f"Issiq tandir nonlari va patirlarni menyudan tanlab buyurtma qilishingiz mumkin!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# 1. "📞 Aloqa" tugmasi uchun (Kanal kirmaydi, faqat tel raqam va admin lichkasi)
@dp.message(F.text == "📞 Aloqa")
async def show_contacts(message: types.Message):
    await message.answer(
        "📞 **Biz bilan bog'lanish uchun raqamlar:**\n\n"
        "📱 **Tel:** +998 (90) 922-99-20\n"
        "📱 **Tel:** +998 (90) 922-88-20\n\n"
        "💬 **Telegram Admin:** @NURSULTON_VIBE\n"
        "⏰ **Ish vaqti:** 06:00 dan 22:00 gacha",
        reply_markup=admin_inline_key,
        parse_mode="Markdown"
    )

# 2. "ℹ️ Biz haqimizda" va ma'lumotlar so'ralganda
@dp.message(F.text == "ℹ️ Biz haqimizda")
async def show_about(message: types.Message):
    await message.answer(
        "🥖 **Nonchi Aka Nonvoyxonasi**\n\n"
        "Biz har kuni tongda olovli tandirlarda toza va tabiiy masalliqlardan issiq non hamda patirlar yopib, mijozlarga yetkazib beramiz.\n\n"
        "👨‍💼 **Savollar bo'yicha admin:** @NURSULTON_VIBE",
        reply_markup=admin_inline_key,
        parse_mode="Markdown"
    )

# 3. "🥖 Non narxlari" so'ralganda to'liq ma'lumot va narxlar
@dp.message(F.text == "🥖 Non narxlari")
async def show_prices(message: types.Message):
    await message.answer(
        "🍞 **Non va Patirlar narxlari:**\n\n"
        "🔥 **Tandir Non** — 5,000 so'm\n"
        "└ *O'tin cho'g'ida yopilgan issiq klassik non.*\n\n"
        "🌿 **Sedanalik Patir** — 8,000 so'm\n"
        "└ *Xushbo'y sedana sepilgan sutli patir.*\n\n"
        "🧈 **Qatlama Patir** — 10,000 so'm\n"
        "└ *Saryog'li, qat-qat bo'lib pishirilgan mazali patir.*\n\n"
        "🥛 **Sutli Choyxona Non** — 9,000 so'm\n\n"
        "🛒 Buyurtma berish uchun **'🥐 Menuni ochish'** tugmasini bosing!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# 4. "👨‍💼 Admin" tugmasi
@dp.message(F.text == "👨‍💼 Admin")
async def show_admin(message: types.Message):
    await message.answer(
        "👨‍💼 Administrator bilan bog'lanish:\n\n"
        "Telegram: @NURSULTON_VIBE\n"
        "Telefon: +998 (90) 922-99-20",
        reply_markup=admin_inline_key
    )

# WebApp orqali kelgan buyurtmalarni ushlash
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    order_info = message.web_app_data.data
    
    await message.answer(
        f"✅ **Buyurtmangiz qabul qilindi!**\n\n"
        f"{order_info}\n\n"
        f"👤 **Mijoz:** {message.from_user.full_name}\n"
        f"🚀 Operatorlarimiz tez orada siz bilan bog'lanishadi!",
        parse_mode="Markdown"
    )
    
    if ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🚨 **Yangi buyurtma tushdi!**\n\n"
                     f"👤 **Mijoz:** {message.from_user.full_name} (@{message.from_user.username or 'yoq'})\n\n"
                     f"{order_info}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Admin xatosi: {e}")

# Web server (Render uchun)
async def handle(request):
    return web.Response(text="Nonchi Aka Bot is Active!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot kanal majburiyatlarisiz ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())