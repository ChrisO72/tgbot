from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from database import db
from bot.config import OWNER_ID


@Client.on_message(filters.private & filters.incoming & filters.command('reset_account') & filters.user(OWNER_ID))
async def reset_account(c: Client, m: Message):
    users = await db.get_all_users()
    async for user in users:
        await db.update_user(user['user_id'], dict(total_messages_today=0, last_message_time=datetime.now().strftime("%d/%m/%Y"), total_words_today=0))
    await m.reply("All accounts have been reset")
