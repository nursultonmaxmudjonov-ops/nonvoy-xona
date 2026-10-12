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
ADMIN_ID = os.getenv("ADMIN_ID")  # .env faylingga ADMIN_ID=12345678 deb yozasan

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

WEBAPP_URL = "https://non-savdo-online.vercel.app/"

# FSM holatlari (Fikr-mulohaza uchun)
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()

# 1. Asosiy Reply Klaviatura
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🥐 Menuni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="🥖 Non turlari va Narxlar"), KeyboardButton(text="🎉 Aktsiyalar")],
        [KeyboardButton(text="📞 Aloqa va Manzil"), KeyboardButton(text="❓ Ko'p beriladigan savollar")],
        [KeyboardButton(text="⭐ Fikr bildirish"), KeyboardButton(text="ℹ️ Biz haqimizda")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Kerakli bo'limni tanlang..."
)

# 2. FAQ Inline Klaviaturasi
faq_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Yetkazib berish vaqti", callback_data="faq_delivery")],
        [InlineKeyboardButton(text="💳 To'lov turlari", callback_data="faq_payment")],
        [InlineKeyboardButton(text="🍞 Non saqlanishi", callback_data="faq_storage")],
        [InlineKeyboardButton(text="🌐 Telegram Kanalimiz", url="https://t.me/nonchi_aka_kanal")]
    ]
)

# 3. Bekor qilish klaviaturasi
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True
)


# === HANDLERLAR ===

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
        f"🔥 Har soatda olovli tandirdan chiqqan issiq nonlar, saryog'li qatlamalar va maxsus patirlarimizni osongina buyurtma qiling.\n\n"
        f"Pastdagi **'🥐 Menuni ochish'** tugmasi orqali xaridingizni boshlang!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "🤖 **Botdan foydalanish yo'riqnomasi:**\n\n"
        "1️⃣ **🥐 Menuni ochish** — To'g'ridan-to meva, patir va nonlarni savatga qo'shib buyurtma bering.\n"
        "2️⃣ **🥖 Non turlari va Narxlar** — Barcha nonlar haqida batafsil ma'lumot va narxlar.\n"
        "3️⃣ **🎉 Aktsiyalar** — Joriy chegirmalar va sovg'alar.\n"
        "4️⃣ **⭐ Fikr bildirish** — Bizning xizmatimiz haqida o'z fikringizni adminga yuboring.\n"
        "5️⃣ **📞 Aloqa va Manzil** — Telefon raqamlarimiz va joylashuvimiz.",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Veb-ilovadan kelgan buyurtmalarni ushlash
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    order_info = message.web_app_data.data
    
    # Mijozga javob
    await message.answer(
        f"✅ **Buyurtmangiz muvaffaqiyatli qabul qilindi!**\n\n"
        f"{order_info}\n\n"
        f"👤 **Mijoz:** {message.from_user.full_name}\n"
        f"📱 **Telegram:** @{message.from_user.username or 'Kiritilmagan'}\n\n"
        f"🚀 Operatorlarimiz 5 daqiqa ichida siz bilan bog'lanib, buyurtmani tasdiqlashadi. Rahmat!",
        parse_mode="Markdown"
    )
    
    # Adminga xabar yuborish
    if ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🚨 **YANGI BUYURTMA TUSHDI!**\n\n"
                     f"👤 **Mijoz:** {message.from_user.full_name} (@{message.from_user.username})\n"
                     f"🆔 **ID:** `{message.from_user.id}`\n\n"
                     f"📦 **Tafsilotlar:**\n{order_info}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Admin xabarnomasida xato: {e}")

# Non turlari bo'limi
@dp.message(lambda msg: msg.text == "🥖 Non turlari va Narxlar")
async def show_bread_types(message: types.Message):
    await message.answer(
        "🍞 **Nonchi Aka mahsulotlari va joriy narxlar:**\n\n"
        "🔥 **1. Tandir Non** — 5,000 so'm\n"
        "└ *Olovli tandirda o'tin cho'g'ida yopilgan mumtoz o'zbek noni.*\n\n"
        "🌿 **2. Sedanalik Patir** — 8,000 so'm\n"
        "└ *Sut va saryog' qo'shib qorilgan, ustiga sedana sepilgan xushbo'y patir.*\n\n"
        "🧈 **3. Qatlama Patir** — 10,000 so'm\n"
        "└ *Qat-qat bo'lib pishirilgan, haqiqiy uy saryog'i ta'miga ega mazali patir.*\n\n"
        "🥛 **4. Sutli Choyxona Non** — 9,000 so'm\n"
        "└ *Yumshoq, uzoq saqlanuvchi va dasturxonbop non.*\n\n"
        "🛒 Buyurtma berish uchun **'🥐 Menuni ochish'** tugmasini bosing!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Aktsiyalar bo'limi
@dp.message(lambda msg: msg.text == "🎉 Aktsiyalar")
async def show_promos(message: types.Message):
    await message.answer(
        "🎁 **Hozirgi mavjud aktsiyalarimiz:**\n\n"
        "1️⃣ **5+1 Aktsiyasi:** 5 ta Qatlama patir xarid qiling va 1 ta Tandir nonni sovg'aga oling!\n"
        "2️⃣ **Ertalabki chegirma:** Har kuni soat 06:00 dan 08:00 gacha barcha nonlarga **10% chegirma** amal qiladi!\n\n"
        "Aksiya shartlaridan foydalanish uchun veb-menuda izoh qoldiring!",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Aloqa va Manzil bo'limi
@dp.message(lambda msg: msg.text == "📞 Aloqa va Manzil")
async def show_contacts(message: types.Message):
    await message.answer(
        "📍 **Manzilimiz:** Toshkent shahri, Yunusobod tumani, 4-mavze.\n"
        "🕒 **Ish vaqtimiz:** Har kuni 06:00 dan 22:00 gacha (dam olishlarsiz).\n\n"
        "📞 **Bog'lanish uchun telefonlar:**\n"
        "📱 +998 (90) 922-99-20\n"
        "📱 +998 (93) 123-45-67\n\n"
        "💬 Admin bilan bog'lanish: @nonchi_aka_admin",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )
    # Lokatsiyani yuborish (Toshkent koordinatasi xaritada)
    await bot.send_location(chat_id=message.chat.id, latitude=41.311081, longitude=69.240562)

# Ko'p beriladigan savollar
@dp.message(lambda msg: msg.text == "❓ Ko'p beriladigan savollar")
async def show_faq(message: types.Message):
    await message.answer(
        "Savolingizga javob olish uchun pastdagi tugmalardan birini tanlang:",
        reply_markup=faq_inline_keyboard
    )

# FAQ Inline javoblari
@dp.callback_query(F.data.startswith("faq_"))
async def handle_faq_callbacks(callback: types.CallbackQuery):
    if callback.data == "faq_delivery":
        await callback.message.answer("🚀 **Yetkazib berish vaqti:** Toshkent shahri bo'ylab buyurtmangiz 30-45 daqiqa ichida issiq holatda yetkaziladi.")
    elif callback.data == "faq_payment":
        await callback.message.answer("💳 **To'lov usullari:** Click, Payme, Uzum va Naqd pul shaklida to'lov qilishingiz mumkin.")
    elif callback.data == "faq_storage":
        await callback.message.answer("🍞 **Saqlash:** Nonlarimiz tabiiy bo'lgani uchun xona haroratida 3 kun davomida o'z yumshoqligini yo'qotmaydi.")
    await callback.answer()

# Biz haqimizda bo'limi
@dp.message(lambda msg: msg.text == "ℹ️ Biz haqimizda")
async def show_about(message: types.Message):
    await message.answer(
        "🥖 **'Nonchi Aka' Nonvoyxonasi**\n\n"
        "Biz o'z faoliyatimizni milliy qadriyatlarimiz va qadimiy nonvoychilik an'analarini saqlagan holda olib boramiz.\n\n"
        "🌟 **Nega aynan biz?**\n"
        "• Faqat saralangan un va tabiiy masalliqlar;\n"
        "• Maxsus o'tin cho'g'ida yopiladigan issiq tandir nonlar;\n"
        "• Halol va toza mahsulotlar;\n"
        "• Qulay va tezkor yetkazib berish xizmati.",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# ⭐ FIKR BILDIRISH FSM (STATE)
@dp.message(lambda msg: msg.text == "⭐ Fikr bildirish")
async def start_feedback(message: types.Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_feedback)
    await message.answer(
        "📝 **O'z fikr-mulohazangiz, taklif yoki shikoyatingizni yozib yuboring:**\n"
        "Biz har bir mijozimiz fikrini diqqat bilan o'rganib chiqamiz.",
        reply_markup=cancel_keyboard,
        parse_mode="Markdown"
    )

@dp.message(lambda msg: msg.text == "❌ Bekor qilish", FeedbackState.waiting_for_feedback)
async def cancel_feedback(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Xabar yuborish bekor qilindi.", reply_markup=main_keyboard)

@dp.message(FeedbackState.waiting_for_feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    feedback_text = message.text
    await state.clear()
    
    await message.answer("✅ **Rahmat! Fikringiz qabul qilindi.** Buni albatta inobatga olamiz!", reply_markup=main_keyboard)
    
    # Adminga fikrni jo'natish
    if ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"💬 **YANGI FIKR-MULOHAZA!**\n\n"
                     f"👤 **Mijoz:** {message.from_user.full_name} (@{message.from_user.username})\n"
                     f"🆔 **ID:** `{message.from_user.id}`\n\n"
                     f"✉️ **Matn:** {feedback_text}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Adminga fikr yuborishda xato: {e}")

# Render bepul saxlanishi uchun kichik veb-server
async def handle(request):
    return web.Response(text="Nonchi Aka Bot is active 24/7!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot muvaffaqiyatli ishga tushdi va faol holatda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())