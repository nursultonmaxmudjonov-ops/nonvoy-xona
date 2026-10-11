import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = "8841434385:AAFgNWa1sSXN_017zUxOdbHxGpiz_Pj0VUY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# WebApp tugmasi bor asosiy menyu
# Eslatma: URL manziliga o'zingizning internetdagi saytingiz havolasini yozasiz (HTTPS bo'lishi shart!)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Buyurtma berish (Menu)", web_app=WebAppInfo(url="SIZNING_WEBSITE_HAVOLANGIZ"))],
        [KeyboardButton(text="📞 Aloqa"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}!\n"
        f"**Nonchi Aka** nonvoyxonasining rasmiy botiga xush kelibsiz! 🥐\n\n"
        f"Mahsulotlarni tanlash va buyurtma berish uchun quyidagi tugmani bosing:",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# WebApp'dan (saytdan) yuborilgan buyurtmani qabul qilish
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    order_data = message.web_app_data.data
    await message.answer(
        f"✅ **Yangi buyurtma qabul qilindi!**\n\n"
        f"📋 Ma'lumot:\n{order_data}\n\n"
        f"Tez orada operatorlarimiz siz bilan bog'lanishadi!",
        parse_mode="Markdown"
    )

@dp.message(lambda msg: msg.text == "📞 Aloqa")
async def show_contacts(message: types.Message):
    await message.answer(
        "📞 **Bog'lanish uchun raqamlarimiz:**\n\n"
        "📱 +998 (90) 922-99-20\n"
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
    print("Bot muvaffaqiyatli ishga tushdi va buyruqlarni kutmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())