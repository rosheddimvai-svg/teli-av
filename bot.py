import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# আপনার বট টোকেন এবং প্রাইভেট চ্যানেল আইডি এখানে দিন।
BOT_TOKEN = "8197222627:AAGjX1XrAqlNnpMYpjSKjA4yOisfeTJbQEk"
PRIVATE_CHANNEL_ID = -1002323042564

# এডমিনের ইউজারনেম এবং ওপেন হ্যাক ওয়েবসাইটের লিঙ্ক
ADMIN_USERNAME = "rs_rezaul_99"
HACK_WEBSITE_URL = "https://as-official-channel.netlify.app/"

# লগিং কনফিগারেশন
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def check_member(user_id: int, bot: Bot) -> bool:
    """
    যাচাই করে যে ব্যবহারকারী প্রাইভেট চ্যানেলের সদস্য কিনা।
    """
    try:
        member = await bot.get_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        logging.error(f"Error checking channel member: {e}")
        return False

async def start(update: Update, context: CallbackContext) -> None:
    """
    যখন ব্যবহারকারী /start কমান্ড ব্যবহার করবে।
    """
    user = update.effective_user
    is_member = await check_member(user.id, context.bot)

    if not is_member:
        # যদি ব্যবহারকারী চ্যানেলের সদস্য না হয়, তবে এই বার্তাটি দেখাবে।
        keyboard = [
            [InlineKeyboardButton("যোগাযোগ করুন", url=f"https://t.me/{ADMIN_USERNAME}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"🚫 **অ্যাক্সেস ডিক্লাইনড!**\n\nআপনি আমাদের ভিআইপি কমিউনিটির সদস্য নন। এই বটটি শুধুমাত্র আমাদের DKWIN টিমের সদস্যদের জন্য তৈরি করা হয়েছে। আপনি যদি আমাদের টিমে যুক্ত হতে চান, তাহলে নিচের বাটনে ক্লিক করে এডমিনের সাথে যোগাযোগ করুন।",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # যদি ব্যবহারকারী চ্যানেলের সদস্য হয়, তবে এই বার্তাটি এবং মেনু দেখাবে।
    keyboard = [
        [InlineKeyboardButton("ওপেন হ্যাক", web_app=WebAppInfo(url=HACK_WEBSITE_URL))],
        [InlineKeyboardButton("Rules", callback_data="show_rules")],
        [InlineKeyboardButton("এডমিনের সাথে যোগাযোগ করুন", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"💎 স্বাগতম, {user.first_name}!\n\nআপনি DKWIN টিমের একজন সম্মানিত সদস্য। আপনার সুবিধার জন্য নিচের অপশনগুলো থেকে বেছে নিন।",
        reply_markup=reply_markup
    )

async def show_rules(update: Update, context: CallbackContext) -> None:
    """
    ব্যবহারকারী যখন 'Rules' বাটনে ক্লিক করবে, তখন এই ফাংশনটি কাজ করবে।
    """
    query = update.callback_query
    await query.answer()

    rules_text = (
        "📜 **বট ব্যবহারের নিয়মাবলী:**\n\n"
        "১. এই বটটি শুধুমাত্র DKWIN টিমের সদস্যদের জন্য।\n"
        "২. বটের কোনো অপশন অপব্যবহার করা যাবে না।\n"
        "৩. কোনো সমস্যা হলে এডমিনের সাথে যোগাযোগ করুন।\n"
        "৪. বটের মাধ্যমে প্রাপ্ত যেকোনো তথ্য বা টুলস ব্যক্তিগত ব্যবহারের জন্য এবং গোপন রাখতে হবে।"
    )
    await query.message.reply_text(rules_text, parse_mode='Markdown')

def main() -> None:
    """
    বটটি শুরু করার জন্য মূল ফাংশন।
    """
    application = Application.builder().token(BOT_TOKEN).build()

    # বিভিন্ন হ্যান্ডলার যোগ করা।
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_rules, pattern="^show_rules$"))
    
    application.run_polling()

if __name__ == "__main__":
    main()
