import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
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
ADMIN_ID = os.getenv("ADMIN_ID")  # .env faylingizda ADMIN_ID=123456789 ko'rinishida yozing
ADMIN_USERNAME = "nonchi_aka_admin" # O'zingizning shaxsiy Telegram username'ingiz

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

WEBAPP_URL = "https://non-savdo-online.vercel.app/"

# FSM Holatlari
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()

# 1. Asosiy Pastki Klaviatura (Main Keyboard)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🥐 Menuni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="🥖 Non turlari va Narxlar"), KeyboardButton(text="🎉 Aktsiyalar")],
        [KeyboardButton(text="👨‍💼 Admin Lchkasi"), KeyboardButton(text="📞 Aloqa va Manzil")],
        [KeyboardButton(text="⭐ Fikr bildirish"), KeyboardButton(text="❓ Ko'p beriladigan savollar")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Kerakli bo'limni tanlang..."
)

# 2. Admin Lchkasi va Tools Inline Klaviaturasi
admin_tools_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💬 Admin Lchkasiga Yozish", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton(text="📢 Rasmiy Kanal", url="https://t.me/nonchi_aka_kanal")],
        [InlineKeyboardButton(text="🌐 Veb-saytga O'tish", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
)

# 3. Bekor qilish klaviaturasi
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True
)


# === BOT HANDLERLARI ===

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
        print(f"Menu button xatosi: {e}")

    await message.answer(
        f"Assalomu alaykum va rahmattullohi va barakatuh, **{message.from_user.first_name}**! 👋\n\n"
        f"🥖 **Nonchi Aka** milliy va zamonaviy nonvoyxonasining rasmiy botiga xush kelibsiz!\n\n"
        f"🔥 Har soatda olovli tandirdan chiqqan issiq nonlar va maxsus patirlarimizni osongina buyurtma qiling.\n\n"
        f"Pastdagi **'🥐 Menuni ochish'** tugmasidan foydalanib xaridingizni amalga oshirishingiz yoki adminga to'g'ridan-to'g'ri yozishingiz mumkin!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Admin Lchkasi tugmasi bossa
@dp.message(lambda msg: msg.text == "👨‍💼 Admin Lchkasi")
async def contact_admin(message: types.Message):
    await message.answer(
        f"👨‍💼 **Admin Lchkasi va Aloqa Markazi:**\n\n"
        f"Buyurtmalaringiz, taklif yoki maxsus so'rovlaringiz bo'yicha administratorimizga to'g'ridan-to'g'ri yozishingiz mumkin.\n\n"
        f"👤 **Admin username:** @{ADMIN_USERNAME}\n"
        f"📞 **Telefon:** +998 (90) 922-99-20\n\n"
        f"Pastdagi tugmani bosing va admin bilan bog'laning 👇",
        reply_markup=admin_tools_keyboard,
        parse_mode="Markdown"
    )

# Non turlari va Narxlari
@dp.message(lambda msg: msg.text == "🥖 Non turlari va Narxlar")
async def show_bread_prices(message: types.Message):
    await message.answer(
        "🍞 **Nonchi Aka mahsulotlarining to'liq katalogi va narxlari:**\n\n"
        "🔥 **1. Tandir Non** — 5,000 so'm\n"
        "└ *O'tin cho'g'ida pishirilgan xushbo'y va yumshoq klassik non.*\n\n"
        "🌿 **2. Sedanalik Patir** — 8,000 so'm\n"
        "└ *Tabiiy sut va saryog'li hamir, ustiga shifobaxsh sedana sepilgan.*\n\n"
        "🧈 **3. Qatlama Patir** — 10,000 so'm\n"
        "└ *Qat-qat bo'lib pishirilgan, haqiqiy saryog' ta'miga ega shirin va shirinmas patir.*\n\n"
        "🥛 **4. Sutli Choyxona Non** — 9,000 so'm\n"
        "└ *Choyxonabop, yumshoq va dasturxonbop maxsus non.*\n\n"
        "🛒 Online buyurtma qilish uchun **'🥐 Menuni ochish'** tugmasini bosing!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Aktsiyalar
@dp.message(lambda msg: msg.text == "🎉 Aktsiyalar")
async def show_promotions(message: types.Message):
    await message.answer(
        "🎁 **Hozirda mavjud bo'lgan chegirma va aktsiyalar:**\n\n"
        "1️⃣ **5+1 Aktsiyasi:** 5 ta Qatlama patir xarid qiling va 1 ta Tandir nonni tekinga oling!\n"
        "2️⃣ **Ertalabki chegirma:** Har kuni soat 06:00 dan 08:00 gacha barcha nonlarga **10% chegirma**!\n\n"
        "Batafsil ma'lumot olish uchun Admin lchkasiga yozishingiz mumkin: @"+ADMIN_USERNAME,
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Veb-ilovadan kelgan buyurtmalarni ushlash va Adminga lchkaga xabar berish
@dp.message(F.web_app_data)
async def handle_web_app_order(message: types.Message):
    order_data = message.web_app_data.data
    
    # Mijozga javob
    await message.answer(
        f"✅ **Buyurtmangiz qabul qilindi!**\n\n"
        f"{order_data}\n\n"
        f"👤 **Mijoz:** {message.from_user.full_name}\n"
        f"📱 **Telegram:** @{message.from_user.username or 'Mavjud emas'}\n\n"
        f"🚀 Operatorlarimiz tez orada siz bilan bog'lanishadi!",
        parse_mode="Markdown"
    )
    
    # Adminga Telegram Lchkasiga buyurtma haqida ma'lumot uzatish
    if ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🚨 **YANGI BUYURTMA TUSHDI!**\n\n"
                     f"👤 **Mijoz:** {message.from_user.full_name} (@{message.from_user.username or 'Mavjud emas'})\n"
                     f"🆔 **ID:** `{message.from_user.id}`\n\n"
                     f"📦 **Buyurtma tarkibi:**\n{order_data}\n\n"
                     f"👉 [Mijoz Lchkasiga Yozish](tg://user?id={message.from_user.id})",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Adminga xabar yuborishda xatolik: {e}")

# Aloqa va Manzil
@dp.message(lambda msg: msg.text == "📞 Aloqa va Manzil")
async def show_location(message: types.Message):
    await message.answer(
        "📍 **Manzilimiz:** Toshkent shahri, Yunusobod tumani, 4-mavze.\n"
        "🕒 **Ish vaqti:** Har kuni 06:00 dan 22:00 gacha\n\n"
        "📞 **Telefonlarimiz:**\n"
        "📱 +998 (90) 922-99-20\n"
        "📱 +998 (93) 123-45-67\n\n"
        "💬 Admin Lchkasi: @"+ADMIN_USERNAME,
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )
    await bot.send_location(chat_id=message.chat.id, latitude=41.311081, longitude=69.240562)

# Fikr bildirish FSM
@dp.message(lambda msg: msg.text == "⭐ Fikr bildirish")
async def ask_feedback(message: types.Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_feedback)
    await message.answer(
        "📝 O'z fikr va takliflaringizni yozib qoldiring. Xabaringiz to'g'ridan-to'g'ri adminga yetib boradi:",
        reply_markup=cancel_keyboard
    )

@dp.message(lambda msg: msg.text == "❌ Bekor qilish", FeedbackState.waiting_for_feedback)
async def cancel_feedback_action(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Xabar yuborish bekor qilindi.", reply_markup=main_keyboard)

@dp.message(FeedbackState.waiting_for_feedback)
async def receive_feedback(message: types.Message, state: FSMContext):
    user_text = message.text
    await state.clear()
    
    await message.answer("✅ **Rahmat! Fikringiz qabul qilindi va adminga yetkazildi.**", reply_markup=main_keyboard)
    
    if ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"💬 **YANGI FIKR-MULOHAZA!**\n\n"
                     f"👤 **Mijoz:** {message.from_user.full_name} (@{message.from_user.username or 'Mavjud emas'})\n"
                     f"🆔 **ID:** `{message.from_user.id}`\n\n"
                     f"✉️ **Matn:** {user_text}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Adminga fikr uzatishda xato: {e}")

# 24/7 Serverni faol ushlab turish kodi
async def handle(request):
    return web.Response(text="Nonchi Aka Bot & Admin Tools is active 24/7!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot muvaffaqiyatli ishga tushdi va Admin Tools bog'landi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())