from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers import get_chatbot, temp
from bot.plugins.filters import check_ban


@Client.on_message(filters.command('reset') & (filters.private | filters.group) & filters.incoming)
@check_ban
async def reset(c: Client, m: Message):

    user_id = m.from_user.id

    chatbot = await get_chatbot(user_id)
    await chatbot.reset()

    if user_id in temp.USER_PROMPT:
        temp.USER_PROMPT.remove(user_id)

    await m.reply("Your thread has been reset")
