from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import json
import os

TOKEN = "8898973532:AAHMTmQiSs7GdsvH6PaO3K5QKuAklUAOxP0"

ADMIN_ID = 1250190731


def load_users():
    if not os.path.exists("users.json"):
        return {}

    with open("users.json", "r") as f:
        return json.load(f)


def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)


def main_keyboard():

    keyboard = [
        ["🏠 Home"],
        ["🪙 Coins", "🏆 Progress"],
        ["💰 Investment", "💸 Withdraw"],
        ["👥 Referral", "📈 Market"],
        ["🖼 Photo Editor", "⚙ Account"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = load_users()

    user_id = str(update.effective_user.id)

    referrer = None

    if context.args:
        referrer = context.args[0]

    if user_id not in users:

        users[user_id] = {
            "coins": 0,
            "level": 1,
            "badge": "Beginner",
            "daily_claimed": False,
            "referrals": 0
        }

        if (
            referrer
            and referrer != user_id
            and referrer in users
        ):

            users[referrer]["coins"] += 50
            users[referrer]["referrals"] += 1

            await context.bot.send_message(
                chat_id=int(referrer),
                text="🎉 You earned 50 coins from a successful referral!"
            )

        save_users(users)

    await update.message.reply_text(
        "💎 Welcome to XPrime Finance!\n\nSelect an option below.",
        reply_markup=main_keyboard()
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    users = load_users()

    user_id = str(update.effective_user.id)

    if text == "🏠 Home":

        await update.message.reply_text(
            "🏠 Welcome to XPrime Finance!",
            reply_markup=main_keyboard()
        )


    elif text == "🪙 Coins":

        coins = users[user_id]["coins"]

        keyboard = [
            ["🎁 Daily Reward"],
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"🪙 Coin Center\n\n"
            f"Balance: {coins} coins",
            reply_markup=reply_markup
        )


    elif text == "🎁 Daily Reward":

        if users[user_id]["daily_claimed"]:

            await update.message.reply_text(
                "❌ You have already claimed today's reward."
            )

        else:

            users[user_id]["coins"] += 50

            users[user_id]["daily_claimed"] = True

            save_users(users)

            await update.message.reply_text(
                "🎁 Daily reward claimed!\n\n"
                "💰 +50 coins added to your account."
            )


    elif text == "🏆 Progress":

        level = users[user_id]["level"]

        badge = users[user_id]["badge"]

        coins = users[user_id]["coins"]

        referrals = users[user_id]["referrals"]

        keyboard = [
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"🏆 Progress\n\n"
            f"⭐ Level: {level}\n"
            f"🏅 Badge: {badge}\n"
            f"🪙 Coins: {coins}\n"
            f"👥 Referrals: {referrals}",
            reply_markup=reply_markup
        )


    elif text == "👥 Referral":

        bot_username = "XPrimeFinanceBot"

        referral_link = (
            f"https://t.me/{bot_username}?start={user_id}"
        )

        keyboard = [
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"👥 Referral Program\n\n"
            f"Referral ID:\n{user_id}\n\n"
            f"Referral Link:\n{referral_link}\n\n"
            f"Earn 50 coins for every successful referral.",
            reply_markup=reply_markup
        )


    elif text == "🔙 Back":

        await update.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_keyboard()
        )

    elif text == "💰 Investment":

        keyboard = [
            ["🥉 ₦3,800 Plan"],
            ["🥈 ₦5,000 Plan"],
            ["🥇 ₦10,000 Plan"],
            ["💎 ₦20,000 Plan"],
            ["👑 ₦50,000 Plan"],
            ["🚀 ₦100,000 Plan"],
            ["🏆 ₦250,000 Plan"],
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "💰 Investment Plans\n\nChoose a plan below:",
            reply_markup=reply_markup
        )


    elif text in [
        "🥉 ₦3,800 Plan",
        "🥈 ₦5,000 Plan",
        "🥇 ₦10,000 Plan",
        "💎 ₦20,000 Plan",
        "👑 ₦50,000 Plan",
        "🚀 ₦100,000 Plan",
        "🏆 ₦250,000 Plan"
    ]:

        keyboard = [
            ["Bank Transfer"],
            ["Bitcoin Wallet"],
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"{text}\n\nChoose payment method:",
            reply_markup=reply_markup
        )


    elif text == "Bank Transfer":

        await update.message.reply_text(
            "Bank Transfer\n\n"
            "Bank: OPAY\n"
            "Account Name: FAVOUR OMONIKE\n"
            "Account Number: 9025381060\n\n"
            "Send proof of payment to admin."
        )


    elif text == "Bitcoin Wallet":

        await update.message.reply_text(
            "Bitcoin Wallet\n\n"
            "BTC Address:\n\n"
            "3NER8BFijTkJDfWdcoatcRpASwSJLonk15"
        )


    elif text == "📈 Market":

        keyboard = [
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "Market\n\n"
            "Bitcoin\n"
            "Ethereum\n"
            "Solana",
            reply_markup=reply_markup
        )


    elif text == "🖼 Photo Editor":

        keyboard = [
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "🖼 Photo Editor\n\n"
            "Photo editing tools will be added soon.",
            reply_markup=reply_markup
        )


    elif text == "⚙ Account":

        keyboard = [
            ["👤 Profile"],
            ["❓ Help"],
            ["⚙ Settings"],
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "⚙ Account Menu",
            reply_markup=reply_markup
        )


    elif text == "👤 Profile":

        await update.message.reply_text(
            f"👤 Profile\n\n"
            f"User ID: {user_id}\n"
            f"Coins: {users[user_id]['coins']}\n"
            f"Level: {users[user_id]['level']}\n"
            f"Badge: {users[user_id]['badge']}\n"
            f"Referrals: {users[user_id]['referrals']}"
        )


    elif text == "❓ Help":

        await update.message.reply_text(
            "❓ Help\n\n"
            "Use the buttons to navigate through XPrime Finance."
        )


    elif text == "⚙ Settings":

        await update.message.reply_text(
            "⚙ Settings\n\n"
            "More settings will be added soon."
        )

    elif text == "💸 Withdraw":

        keyboard = [
            ["Bank Withdrawal"],
            ["Bitcoin Withdrawal"],
            ["🔙 Back"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "💸 Withdrawal Menu\n\n"
            "Choose a withdrawal method.",
            reply_markup=reply_markup
        )


    elif text == "Bank Withdrawal":

        await update.message.reply_text(
            "🏦 Bank Withdrawal\n\n"
            "Please send your details in this format:\n\n"
            "Bank Name:\n"
            "Account Name:\n"
            "Account Number:\n"
            "Amount:"
        )


    elif text == "Bitcoin Withdrawal":

        await update.message.reply_text(
            "₿ Bitcoin Withdrawal\n\n"
            "Please send your details in this format:\n\n"
            "Wallet Address:\n"
            "Amount:"
        )


    elif "Bank Name:" in text and "Account Number:" in text:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=
            f"🏦 NEW BANK WITHDRAWAL REQUEST\n\n"
            f"User ID: {user_id}\n\n"
            f"{text}"
        )

        await update.message.reply_text(
            "✅ Withdrawal request submitted successfully.\n\n"
            "Your request is under review."
        )


    elif "Wallet Address:" in text:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=
            f"₿ NEW BITCOIN WITHDRAWAL REQUEST\n\n"
            f"User ID: {user_id}\n\n"
            f"{text}"
        )

        await update.message.reply_text(
            "✅ Withdrawal request submitted successfully.\n\n"
            "Your request is under review."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu
    )
)

print("🚀 XPrime Finance is running...")

app.run_polling()

