from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from bot.helpers import add_new_user
from bot.messages import Messages, Buttons



@Client.on_callback_query(filters.regex("^home$"))
@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c: Client, m: Message):
    if isinstance(m, CallbackQuery):
        await m.answer()
        await m.message.delete()
        m.message.from_user = m.from_user
        m = m.message

    await add_new_user(c, m.from_user.id, m.from_user.mention)

    Buttons.HOME_BUTTONS.inline_keyboard[0][0].url = Buttons.HOME_BUTTONS.inline_keyboard[0][0].url.format(
        bot_username=c.me.username)
    START_MSG = Messages.START_MESSAGE.format(m.from_user.mention)
    return await m.reply(START_MSG, disable_web_page_preview=True, quote=True, reply_markup=Buttons.HOME_BUTTONS)


@Client.on_message(filters.command('start') & filters.group & filters.incoming)
async def start_group(c: Client, m: Message):
    await m.reply_text("I am alive, /help", quote=True)
