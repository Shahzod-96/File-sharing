
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext

# Define file codes and corresponding file links
FILE_CODES = {
    "01": "https://t.me/hMeKcS/2/01.mp4",  # Replace with actual file URL
    "02": "https://t.me/hMeKcS/3/02.mp4",  # Replace with actual file URL
    "03": "https://t.me/hMeKcS/4/03.mp4",
    "04": "https://t.me/hMeKcS/5/04.mp4",  
}

CHANNEL_USERNAME = "@MultiLevel_IELTShakhzod"  # Replace with your channel's username

async def start(update: Update, context: CallbackContext):
    """Handles the /start command and sends the join link."""
    user = update.effective_user

    # Create a button to join the channel
    keyboard = [
        [InlineKeyboardButton("Join Our Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("Verify Membership", callback_data="verify")]
    ]

    await update.message.reply_text(
        f"Hi {user.first_name}! To download a file, please join our channel first.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def verify_membership(update: Update, context: CallbackContext):
    """Verifies if the user has joined the channel."""
    query = update.callback_query
    user_id = query.from_user.id
    bot = context.bot

    try:
        # Check if the user is a member of the channel
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            # Once verified, ask for the file code
            await query.edit_message_text("Thanks for joining! Please send the file code to get your file.")
        else:
            await query.edit_message_text("You are not a member yet. Please join the channel and try again.")
    except:
        await query.edit_message_text("You are not a member yet. Please join the channel and try again.")

async def handle_code(update: Update, context: CallbackContext):
    """Handles the file code input."""
    code = update.message.text.lower()  # Convert the code to lowercase to make it case-insensitive
    if code in FILE_CODES:
        # If the code is valid, send the corresponding file link
        await update.message.reply_text(f"Here is your file: {FILE_CODES[code]}")
    else:
        # If the code is invalid, ask the user to try again
        await update.message.reply_text("Invalid code! Please send a valid file code.")

def main():
    """Sets up the bot and starts polling."""
    application = Application.builder().token("8015973772:AAETNMoJqjJ7d-isWwMzFZH4jetFkXLuHjM").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify_membership))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
