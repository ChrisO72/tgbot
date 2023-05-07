import os
from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers import get_chatbot


@Client.on_message(filters.command('get_chat') & filters.private & filters.incoming)
async def get_chat(c: Client, m: Message):
    sts = await m.reply_text("Processing...")
    user_id = m.from_user.id
    chatbot = await get_chatbot(user_id)
    f = f"chat_{user_id}.txt"
    await chatbot.save(f)
    await m.reply_document(f, caption="Here is your chat history")
    os.remove(f)
    await sts.delete()


@Client.on_message(filters.command('get_chat') & filters.group & filters.incoming)
async def get_chat(c: Client, m: Message):
    await m.reply_text("This command is only available in private chat", quote=True)