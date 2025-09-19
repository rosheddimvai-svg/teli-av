import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# আপনার বট টোকেন এবং প্রাইভেট চ্যানেল আইডি এখানে দিন।
BOT_TOKEN = "8197222627:AAGjX1XrAqlNnpMYpjSKjA4yOisfeTJbQEk"
PRIVATE_CHANNEL_ID = -1002323042564

# এডমিনের ইউজারনেম (যোগাযোগের জন্য)
ADMIN_USERNAME = "@rs_rezaul_99"

# লগিং কনফিগারেশন, যাতে বটের কার্যক্রম দেখা যায়।
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def check_member(user_id: int, bot: Bot) -> bool:
    """
    এই ফাংশনটি যাচাই করে যে ব্যবহারকারী প্রাইভেট চ্যানেলের সদস্য কিনা।
    """
    try:
        member = await bot.get_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=user_id)
        # এখানে 'member' এর স্ট্যাটাস যাচাই করা হয়।
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        logging.error(f"Error checking channel member: {e}")
        return False

async def start(update: Update, context: CallbackContext) -> None:
    """
    যখন ব্যবহারকারী /start কমান্ড ব্যবহার করবে, তখন এই ফাংশনটি কাজ করবে।
    """
    user = update.effective_user
    is_member = await check_member(user.id, context.bot)

    if not is_member:
        # যদি ব্যবহারকারী চ্যানেলের সদস্য না হয়, তাহলে এই বার্তাটি দেখাবে।
        await update.message.reply_text(
            "Access declined ❌\nআপনি আমাদের টিমের মেম্বার নন এবং আমাদের ভিআইপি চ্যানেলে যুক্ত হননি। এই কারণে আপনি এটি ব্যবহার করতে পারবেন না।"
        )
        return

    # যদি ব্যবহারকারী চ্যানেলের সদস্য হয়, তাহলে মেনু দেখাবে।
    keyboard = [
        [InlineKeyboardButton("DKWIN এর UID পাঠান", callback_data="send_uid")],
        [InlineKeyboardButton("এডমিনের সাথে যোগাযোগ করুন", url=f"https://t.me/{ADMIN_USERNAME[1:]}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"স্বাগতম, {user.first_name}!\n\nআপনি আমাদের ভিআইপি টিমের একজন সদস্য। বটটি ব্যবহার করার জন্য নিচের বাটনগুলো ব্যবহার করুন।",
        reply_markup=reply_markup
    )

async def handle_uid_message(update: Update, context: CallbackContext) -> None:
    """
    এই ফাংশনটি UID মেসেজ পরিচালনা করবে।
    """
    user = update.effective_user
    user_message = update.message.text
    
    # এটি নিশ্চিত করার জন্য যে ব্যবহারকারী UID পাঠাচ্ছে। আপনি চাইলে এখানে UID এর ফরম্যাট যাচাই করতে পারেন।
    await update.message.reply_text(f"আপনার UID: {user_message} পেয়েছি। ধন্যবাদ!")

def main() -> None:
    """
    বটটি শুরু করার জন্য মূল ফাংশন।
    """
    # Application তৈরি করা
    application = Application.builder().token(BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার যোগ করা।
    application.add_handler(CommandHandler("start", start))

    # যদি কোনো টেক্সট মেসেজ আসে, তবে handle_uid_message ফাংশনটি কাজ করবে।
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_uid_message))

    # পোলিং শুরু করা
    application.run_polling()

if __name__ == "__main__":
    main()