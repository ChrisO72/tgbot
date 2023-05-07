from pyrogram import Client, filters, types
from bot.messages import Messages, Buttons
from bot.plugins.filters import check_ban


@Client.on_callback_query(filters.regex("^help$"))
@Client.on_message(filters.command("help") & filters.private & filters.incoming)
@check_ban
async def help(client, message):
    if isinstance(message, types.CallbackQuery):
        await message.answer()
        await message.message.delete()
        message = message.message

    await message.reply_text(Messages.HELP_MESSAGE, quote=True, reply_markup=Buttons.HELP_BUTTONS)


# for group
@Client.on_message(filters.command("help") & filters.group & filters.incoming)
async def help_group(client, message):
    text = Messages.GROUP_HELP_MESSAGE.format(bot_username=client.me.username)
    await message.reply_text(text, quote=True)