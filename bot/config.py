import os

from dotenv import load_dotenv

load_dotenv()

# Mandatory variables for the bot to start
API_ID = int(os.environ.get("API_ID"))  # API ID from https://my.telegram.org/auth
API_HASH = os.environ.get("API_HASH")  # API Hash from https://my.telegram.org/auth
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Bot token from @BotFather
DATABASE_URL = os.environ.get("DATABASE_URL", None)  # mongodb uri from https://www.mongodb.com/
OWNER_ID = int(os.environ.get("OWNER_ID"))  # id of the owner
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)  # openai api key from https://beta.openai.com/account/api-keys
PROVIDER_TOKEN = os.environ.get("PROVIDER_TOKEN", None)  # from @BotFather
CRYPTO_PAY_API_KEY = os.environ.get("CRYPTO_PAY_API_KEY", None)  # from https://t.me/CryptoBot

#  Optional variables
PAYMENT_TESTING = os.environ.get("PAYMENT_TESTING", False) == "True"
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Chat-GPT")
ADMINS = ([int(x) for x in os.environ.get("ADMINS", "0").split(",")])
ADMINS.append(OWNER_ID)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))
WEB_SERVER = os.environ.get("WEB_SERVER", False)
PORT = int(os.environ.get("PORT", 5000))
LOADING_TEXTS = [
    "Loading...",
    "Thinking...",
    "Processing...",
    "Getting response...",
    "Getting response from DynoGPT...",
    "Hold on...",
]
SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    "You are a Telegram AI Chat bot, your name is DynoGPT, Your Username: @{username}, you are chatting to {user_dict}",
) 
