from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import OWNER_ID
from database import db


@Client.on_message(filters.command('ban') & filters.private & filters.incoming & filters.user(OWNER_ID))
async def ban(c: Client, m: Message):
    text = "Here are the banned users:\n\n"
    banned_user_ids = await db.get_banned_user_ids()
    for user in banned_user_ids:
        text += f"- `{user}`\n"

    if len(m.command) == 1:
        await m.reply(text)
        return

    if len(m.command) == 2:
        banned_user = await db.ban_user(int(m.command[1]))

        if not banned_user:
            return await m.reply("User not found")

        await m.reply("User banned")
