from typing import Dict, List

from pyrogram import Client, ContinuePropagation
from pyrogram.types import Update, User, Chat
from pyrogram.raw.types import UpdateBotPrecheckoutQuery


_on_checkout_query_handlers: List[callable] = []


def on_checkout_query(func: callable):
    _on_checkout_query_handlers.append(func)
    return func


@Client.on_raw_update()
async def _raw(bot: Client, update: Update, users: Dict[int, User], chats: Dict[int, Chat]):
    # print(type(x) for x in (update, users, chats))
    # print(update, users, chats)

    if isinstance(update, UpdateBotPrecheckoutQuery):
        for handler in _on_checkout_query_handlers:
            await handler(bot, update, users, chats)
    else:
        raise ContinuePropagation()


