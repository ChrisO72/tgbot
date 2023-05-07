import functools

from pyrogram import Client
from pyrogram.types import Message

from database import db


def check_ban(func):
    @functools.wraps(func)
    async def wrapper(client: "Client", message: "Message"):
        chat_id = getattr(message.from_user, "id", None)
        
        if chat_id in await db.get_banned_user_ids():
            await message.reply_text("You are banned from this bot")
            return 
            
        return await func(client, message)
    return wrapper
