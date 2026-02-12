bot.pyimport os
import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8235845999:AAEmNfae8X4VD09MAHj3JthgzZZ1cyyQVtw")
ADMIN_ID = 5091804719

# Database
conn = sqlite3.connect("likes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    total_likes INTEGER DEFAULT 0,
    coins INTEGER DEFAULT 100
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_limit (
    date TEXT,
    count INTEGER
)
""")
conn.commit()


def is_admin(user_id):
    return user_id == ADMIN_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to Pro Like Bot\n\n"
        "Commands:\n"
        "/like USERID\n"
        "/balance USERID"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Use: /balance 123456")
        return

    user_id = context.args[0]
    cursor.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    coins = data[0] if data else 0

    await update.message.reply_text(
        f"💰 Coin Balance\n\n🆔 ID: {user_id}\n🪙 Coins: {coins}"
    )


async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only Admin Can Use This Command!")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Use Format: /like 123456")
        return

    user_id = context.args[0]
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT count FROM daily_limit WHERE date=?", (today,))
    result = cursor.fetchone()

    if result:
        if result[0] >= 15:
            await update.message.reply_text("🚫 Daily Limit Finished!")
            return
        else:
            cursor.execute("UPDATE daily_limit SET count=count+1 WHERE date=?", (today,))
    else:
        cursor.execute("INSERT INTO daily_limit VALUES (?, ?)", (today, 1))

    cursor.execute("SELECT total_likes, coins FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    before = data[0] if data else 0
    coins = data[1] if data else 100

    cost = 10
    if coins < cost:
        await update.message.reply_text("❌ Not Enough Coins!")
        return

    added = 49
    total = before + added
    coins -= cost

    if data:
        cursor.execute("UPDATE users SET total_likes=?, coins=? WHERE user_id=?",
                       (total, coins, user_id))
    else:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)",
                       (user_id, total, coins))

    conn.commit()

    remaining = 15 - (result[0] + 1) if result else 14

    message = f"""
╔═══🔥 LIKE SUCCESS 🔥═══╗

🆔 ID: {user_id}
👍 Before: {before}
➕ Added: {added}
❤️ Total: {total}

🪙 Coins Left: {coins}
📊 Remaining Today: {remaining}

╚══════════════════╝
"""

    await update.message.reply_text(message)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("like", like))
app.add_handler(CommandHandler("balance", balance))

print("🔥 Pro Bot Running...")
app.run_polling()
