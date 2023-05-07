from pyrogram import Client, enums, filters
from pyrogram.types import Message

from bot import logger
from bot.config import LOG_CHANNEL
from bot.helpers import add_new_user, get_chatbot, respond, temp
from bot.plugins.filters import check_ban


@Client.on_message(filters.text & (filters.group & (filters.command("ask") | filters.mentioned | filters.reply)) & filters.incoming)
@check_ban
async def prompt_handler(c: Client, m: Message):
    user_id = m.from_user.id if m.from_user else None

    if not user_id:
        return await m.reply("You are not a user, you are a bot or a anonymous admin, you can't use this bot", quote=True)

    chat = None
    if m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        chat = m.chat

    await add_new_user(c, m.from_user.id, m.from_user.mention, chat=chat)

    if m.text.startswith('/') and not m.text.split()[0] == '/ask':
        return
    elif m.text.startswith('/ask'):
        m.text = m.text.replace('/ask', '')
        if not m.text and m.reply_to_message:
            m.text = m.reply_to_message.text
        if not m.text:
            return await m.reply("You need to reply to a message or send a message after /ask", quote=True)
    elif m.mentioned:
        m.text = m.text.replace(f"@{temp.BOT_USERNAME}", '')

    if len(m.text) <= 1:
        return

    chatbot = await get_chatbot(user_id, m.from_user)

    if user_id in temp.USER_PROMPT:
        return await m.reply("Don't make a new request until the old one completes, or /reset and try again", quote=True)

    message = None

    try:
        temp.USER_PROMPT.append(user_id)
        og_response = await respond(chatbot, m.text, m)
        message = f"From User [{m.from_user.id}] - {m.from_user.mention}: {m.text}\n\nFrom Chatbot: {og_response[:4000]}"
    except Exception as e:
        logger.error(e, exc_info=True)
        await m.reply("Something went wrong!", quote=True)
        message = e
    finally:
        temp.USER_PROMPT.remove(
            user_id) if user_id in temp.USER_PROMPT else None
        msg = await m.forward(LOG_CHANNEL) if LOG_CHANNEL else None
        await msg.reply(message) if message and LOG_CHANNEL else None
