import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = "8841434385:AAFgNWa1sSXN_017zUxOdbHxGpiz_Pj0VUY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Vercel havolangiz ulandi
WEBAPP_URL = "https://non-savdo-online.vercel.app/"

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🥐 Menuni ochish (Buyurtma)", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="📞 Aloqa"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}!\n"
        f"**Nonchi Aka** nonvoyxonasining rasmiy botiga xush kelibsiz! 🥐\n\n"
        f"Issiq tandir nonlari va patirlarni tanlash hamda buyurtma berish uchun quyidagi **Menuni ochish** tugmasini bosing:",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# WebApp (sayt) ichidan "Buyurtmani rasmiylashtirish" bosilganda keladigan ma'lumotni qabul qilish
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