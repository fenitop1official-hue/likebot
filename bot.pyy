from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your bot token and admin ID
BOT_TOKEN = "8235845999:AAEmNfae8X4VD09MAHj3JthgzZZ1cyyQVtw"
ADMIN_ID = 5091804719  # Only this ID can use /like

# In-memory user data
users = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Simple Like Bot\n\n"
        "Commands:\n"
        "/like USERID\n"
        "/balance USERID"
    )

# /balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /balance USERID")
        return

    user_id = context.args[0]
    coins = users.get(user_id, 100)
    await update.message.reply_text(f"ID: {user_id}\nCoins: {coins}")

# /like command
async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only admin can use this command!")
        return

    if not context.args:
        await update.message.reply_text("Usage: /like USERID")
        return

    user_id = context.args[0]
    before = users.get(user_id, 100)
    added = 49
    total = before + added
    users[user_id] = total

    await update.message.reply_text(
        f"Like Added!\nID: {user_id}\nBefore: {before}\nAdded: {added}\nTotal: {total}"
    )

# Run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("like", like))
app.add_handler(CommandHandler("balance", balance))

print("Simple Bot Running...")
app.run_polling()
