from pyrogram import Client, filters, types
from bot.messages import Messages, Buttons
from bot.plugins.filters import check_ban


@Client.on_callback_query(filters.regex("^about$"))
@Client.on_message(filters.command("about") & filters.private & filters.incoming)
@check_ban
async def about(client: Client, message):
    if isinstance(message, types.CallbackQuery):
        await message.answer()
        await message.message.delete()
        message = message.message

    text = Messages.ABOUT_MESSAGE.format(bot_name=f"[{message.from_user.first_name}](https://telegram.me/{message.from_user.username})", bot_version="1.0.0")

    await message.reply_text(text, quote=True, reply_markup=Buttons.ABOUT_BUTTONS, disable_web_page_preview=True)
