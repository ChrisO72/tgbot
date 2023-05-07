import uvloop
uvloop.install()

from bot.plugins import web_server
from bot.helpers import temp
from bot.config import *

from pyrogram import Client, errors
import asyncio
import datetime
import logging
import logging.config

from aiohttp import web



# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "Chat-GPT-3",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="bot/plugins")
        )

    async def start(self):

        temp.START_TIME = datetime.datetime.now()

        try:
            await super().start()
        except errors.FloodWait as e:
            logger.warning(f"Sleeping for {e.value} seconds")
            logger.warning(f"Bot is restarting after {e.value} seconds")
            await asyncio.sleep(e.value)
            await super().start()
        except Exception as e:
            logger.error(e, exc_info=True)
            exit(1)

        me = await self.get_me()
        self.owner = await self.get_users(int(OWNER_ID))
        self.username = f'@{me.username}'
        temp.BOT_USERNAME = me.username
        temp.FIRST_NAME = me.first_name

        logger.info('Bot started')

        if WEB_SERVER:
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app, host=bind_address, port=PORT).start()
            logger.info('Server started')

    async def stop(self, *args):
        await super().stop()
        logger.info('Bot Stopped Bye')
