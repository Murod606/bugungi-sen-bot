import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
TOKEN = os.getenv("BOT_TOKEN")


questions = [
    {
        "text": "🌙 Hozir kayfiyatingiz qaysi biriga yaqin?",
        "options": ["😊 Baxtli", "😐 Oddiy", "😔 G'amgin", "😵 Charchagan"]
    },
    {
        "text": "🎨 Qaysi rangni tanlaysiz?",
        "options": ["🖤 Qora", "💙 Ko'k", "❤️ Qizil", "💚 Yashil"]
    },
    {
        "text": "🌍 Hozir qayerda bo'lishni xohlardingiz?",
        "options": ["🏖 Dengizda", "🏔 Tog'da", "🌃 Shaharda", "🏡 Uyda"]
    },
    {
        "text": "🎵 Qaysi ovoz sizga yoqimli?",
        "options": ["🌧 Yomg'ir", "🌊 Dengiz", "🔥 Olov", "🎶 Musiqa"]
    },
    {
        "text": "🔢 Bir raqam tanlang:",
        "options": ["1️⃣ 7", "2️⃣ 13", "3️⃣ 23", "4️⃣ 99"]
    }
]


descriptions = [
    "Siz tashqaridan sokin ko'rinsangiz ham, ichingizda juda ko'p fikrlar yashaydi. 🌙",
    "Siz odamlarni tez tushunasiz, lekin o'zingizni hammaga ham ko'rsatishni yoqtirmaysiz.",
    "Sizda mustaqillik kuchli. Boshqalar nima desa ham, oxirgi qarorni o'zingiz qabul qilasiz.",
    "Sizning eng kuchli tomoningiz sezgirligingiz. Mayda narsalarni boshqalar sezmaydi, siz esa darhol payqaysiz.",
    "Siz yangi taassurotlarni yaxshi ko'rasiz. Bir xil hayot sizni tez zeriktirishi mumkin.",
    "Sizning ichingizda romantik va biroz sirli dunyo bor. Uni hamma ham ko'ra olmaydi.",
    "Siz ishonchni oson bermaysiz. Ammo biror kishiga ishonsangiz, chin dildan ishonasiz.",
    "Siz ko'p narsani hazil bilan yashirasiz. Ba'zan kulayotgan odamning ichida eng ko'p gap bo'ladi."
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔮 O'zimni tekshirish", callback_data="start_test")]
    ]

    await update.message.reply_text(
        "🪞 *BUGUNGI SEN*\n\n"
        "Bu oddiy test emas.\n"
        "Men sizga 5 ta savol beraman va javoblaringizdan "
        "bugungi kayfiyatingiz va xarakteringiz haqida kichik portret yarataman.\n\n"
        "Tayyormisiz? 👀",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["question"] = 0
    context.user_data["answers"] = []

    await send_question(query, context)


async def send_question(query, context):
    number = context.user_data["question"]

    if number >= len(questions):
        await show_result(query, context)
        return

    question = questions[number]

    keyboard = []

    for i, option in enumerate(question["options"]):
        keyboard.append([
            InlineKeyboardButton(
                option,
                callback_data=f"answer_{i}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            f"📌 {number + 1}/{len(questions)}",
            callback_data="nothing"
        )
    ])

    await query.edit_message_text(
        f"🧩 *Savol {number + 1}*\n\n{question['text']}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    answer_number = int(query.data.split("_")[1])

    context.user_data["answers"].append(answer_number)
    context.user_data["question"] += 1

    await send_question(query, context)


async def show_result(query, context):
    answers = context.user_data["answers"]

    score = sum(answers)

    description = descriptions[score % len(descriptions)]

    moods = [
        "🌙 Sokinsiz, lekin chuqur",
        "✨ Yengil va pozitiv",
        "🌧 Biroz o'ychan",
        "🔥 Kuchli va qat'iyatli",
        "🌌 Sirli va romantik",
        "🌿 Tinchlik izlayotgan",
    ]

    colors = [
        "Qora 🖤",
        "Ko'k 💙",
        "Qizil ❤️",
        "Yashil 💚",
        "Binafsha 💜",
        "Oq 🤍",
    ]

    mood = random.choice(moods)
    color = random.choice(colors)

    text = (
        "🔮 *SIZNING BUGUNGI PORTRETINGIZ*\n\n"
        f"🧠 *Ichki holat:* {mood}\n"
        f"🎨 *Bugungi rangingiz:* {color}\n\n"
        f"💭 *Siz haqingizda:*\n{description}\n\n"
        "━━━━━━━━━━━━━━\n"
        "✨ *Bugungi kichik xabar:*\n"
        "Bugun siz kutmagan joydan kichik bir quvonch "
        "kelishi mumkin. Uni o'tkazib yubormang. 🌙"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 Qaytadan o'tish",
                callback_data="start_test"
            )
        ]
    ]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def nothing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("⏳ Savolga javob bering 🙂")


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤔 Men hozircha faqat tugmalar orqali ishlayman.\n\n"
        "/start ni bosib, testni boshlang."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(start_test, pattern="^start_test$")
    )
    app.add_handler(
        CallbackQueryHandler(answer, pattern="^answer_")
    )
    app.add_handler(
        CallbackQueryHandler(nothing, pattern="^nothing$")
    )
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message)
    )

    print("🤖 Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
