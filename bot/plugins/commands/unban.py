from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import OWNER_ID
from database import db

@Client.on_message(filters.command('unban') & filters.private & filters.incoming & filters.user(OWNER_ID))
async def unban(c: Client, m: Message):
    text = "Here are the banned users:\n\n"
    banned_user_ids = await db.get_banned_user_ids()
    for user in banned_user_ids:
        text += f"- `{user}`\n"

    if len(m.command) != 2:
        await m.reply(text)
        return

    unabanned_user = await db.unban_user(int(m.command[1]))
    if not unabanned_user:
        await m.reply(f"User {m.command[1]} not banned or not found")
        return

    await m.reply("User unbanned")
