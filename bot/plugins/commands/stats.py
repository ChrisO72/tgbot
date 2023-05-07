from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import OWNER_ID
from database import db


@Client.on_message(filters.command('stats') & filters.private & filters.incoming & filters.user(OWNER_ID))
async def stats(c: Client, m: Message):
    total_users = await db.get_total_users()
    text = f"Total Users: {total_users}"
    await m.reply(text)
