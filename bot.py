import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, MenuButtonWebApp

load_dotenv()

# Token faqat Render.com sozlamalaridan (yoki .env fayldan) olinadi
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

WEBAPP_URL = "https://non-savdo-online.vercel.app/"

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🥐 Menuni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="📞 Aloqa"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True
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
        f"Salom, {message.from_user.first_name}!\n"
        f"**Nonchi Aka** nonvoyxonasining rasmiy botiga xush kelibsiz! 🥐\n\n"
        f"Pastdagi tugmani bosing yoki chatning chap pastki qismidagi **'Menuni ochish'** tugmasidan foydalaning:",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    order_info = message.web_app_data.data
    await message.answer(
        f"✅ **Buyurtmangiz qabul qilindi!**\n\n"
        f"{order_info}\n\n"
        f"👤 Buyurtmachi: {message.from_user.full_name}\n"
        f"Tez orada operatorlarimiz siz bilan bog'lanishadi! Rahmat!",
        parse_mode="Markdown"
    )

@dp.message(lambda msg: msg.text == "📞 Aloqa")
async def show_contacts(message: types.Message):
    await message.answer(
        "📞 **Bog'lanish uchun raqamlarimiz:**\n\n"
        "📱 +998 (90) 922-99-20\n"
        "📱 +998 (90) 922-88-20\n\n"
        "⏰ Har kuni 06:00 dan 22:00 gacha xizmatingizdamiz!",
        parse_mode="Markdown"
    )

@dp.message(lambda msg: msg.text == "ℹ️ Biz haqimizda")
async def show_about(message: types.Message):
    await message.answer(
        "🥖 **Nonchi Aka Nonvoyxonasi**\n\n"
        "Biz har soatda issiq va xushbo'y tandir nonlarini yopamiz! "
        "Faqat tabiiy mahsulotlar va milliy retseptlar.",
        parse_mode="Markdown"
    )

async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())