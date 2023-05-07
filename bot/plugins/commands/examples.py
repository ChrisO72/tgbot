from pyrogram import Client, filters
from pyrogram.types import Message

from bot.plugins.filters import check_ban


@Client.on_message(filters.command('examples') & filters.private & filters.incoming)
@check_ban
async def examples(c: Client, m: Message):
    txt = """Here are some examples to get started with:
    
1) `Got any creative ideas for a 10 year old’s birthday?`
2) `How do I make an HTTP request in Javascript?`
3) `Explain quantum computing in simple terms`
4) `Make a simple Flask Server`
5) `Write a blog on time Managament`
6) `Write a simple telegram bot`
7) `Debug this code`
8) `Suggest Some Horror Movies`"""
    await m.reply(txt)
