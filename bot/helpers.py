import asyncio
import datetime
import random
import textwrap
from contextlib import suppress

from pyrogram import emoji, errors

from bot.config import (LOADING_TEXTS, LOG_CHANNEL, OPENAI_API_KEY,
                        SYSTEM_PROMPT)
from database.user_db import db
from utils.chatbot import Chatbot


class temp(object):
    BOT_USERNAME = None
    FIRST_NAME = None
    START_TIME = None
    USERS_INFO = {}
    USER_PROMPT = []
    USER_AUDIO = []


async def get_chatbot(user_id: int, user_dict=None) -> Chatbot:
    chatbot = temp.USERS_INFO.get(user_id)
    system_prompt = SYSTEM_PROMPT.format(
        username=temp.BOT_USERNAME,
        user_dict=user_dict
    )
    if not chatbot:
        chatbot = Chatbot(api_key=OPENAI_API_KEY, system_prompt=system_prompt)
        temp.USERS_INFO[user_id] = chatbot

    return temp.USERS_INFO[user_id]


async def async_function(func, *args, **kwargs):
    """ Run a function in an executor """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def respond(chatbot: Chatbot, prompt: str, message) -> str:
    del_msg = await message.reply(emoji.THOUGHT_BALLOON, quote=True)
    try:
        start_time = datetime.datetime.now()
        res_task = asyncio.create_task(asyncio.to_thread(chatbot.ask, prompt))

        wait_time = 1
        while not res_task.done():
            now = datetime.datetime.now()
            diff = (now - start_time) + datetime.timedelta(seconds=wait_time)
            if diff.total_seconds() > 5:
                text = random.choice(LOADING_TEXTS)
                with suppress(Exception):
                    await del_msg.edit_text(f"{emoji.THOUGHT_BALLOON} {text}\nThis may take a while...")
                await asyncio.sleep(1)
                wait_time *= 2

        og_response = await (await res_task)
        res = textwrap.wrap(og_response, 4000, replace_whitespace=False)
        for mes in res:
            try:
                await reply_text(message, mes)
            except errors.FloodWait as e:
                await asyncio.sleep(e.value)
                await reply_text(message, mes)
        await del_msg.delete()
        return og_response
    except Exception as e:
        raise e
    finally:
        await del_msg.delete()


async def reply_text(message, text: str, **kwargs):
    try:
        return await message.reply_text(text, disable_web_page_preview=True, quote=True, **kwargs)
    except errors.FloodWait as e:
        x = await message.reply_text(f"Sleeping for {e.value} seconds")
        print(f"Sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        await x.delete()
        return await message.reply_text(text, disable_web_page_preview=True, quote=True, **kwargs)
    except errors.MessageNotModified:
        pass
    except errors.BadRequest:
        pass


async def add_new_user(c, user_id, mention, chat=None):
    is_user = await db.user_exists(user_id)
    if not is_user:
        await db.create_user(user_id)
        text = f"New user joined!\n\nUser ID: `{user_id}`\nMention: {mention}"
        if chat:
            text += f"\nChat: {chat.title} `{chat.id}`"
            link = await c.export_chat_invite_link(chat.id)
            text += f"\nGroup Link: {link}"
        await c.send_message(LOG_CHANNEL, text, disable_web_page_preview=True)


async def reset_users(app):
    users = await db.get_all_users()
    async for user in users:
        await db.update_user(user['user_id'], dict(total_messages_today=0, last_message_time=datetime.now().strftime("%d/%m/%Y"), total_words_today=0))
        await app.send_message(user["user_id"], "Your stats have been reset!, you can now start chatting again")

    await app.send_message(LOG_CHANNEL, "All users stats have been reset!")
