# Overview

The Chat-GPt3 bot is a Telegram bot that uses the GPT-3 language model to answer user questions. It is built with Python 3.10.6 and the pyrogram library

## Requirements

To use the Chat-GPt3 bot, you will need the following:

- A Telegram account and the Telegram app installed on your device
- An API ID and hash from Telegram (see [here](https://core.telegram.org/api/obtaining_api_id) for more information)

- A bot token from Telegram (see [here](https://core.telegram.org/bots#6-botfather) for more information)
- A database URL to store user information (using MongoDb)

- The owner ID of the bot

- A log channel ID for the bot to post log messages

## Required Variables

| Variable Name             | Value                                                                                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `API_ID` (required)       | Telegram api_id obtained from <https://my.telegram.org/apps>.                                                                                                  |
| `API_HASH` (required)     | Telegram api_hash obtained from <https://my.telegram.org/apps>.                                                                                                |
| `BOT_TOKEN` (required)    | Create a bot using @BotFather, and get the Telegram API token.                                                                                                 |
| `OWNER_ID` (required)     | ID of Owner.                                                                                                                                                   |
| `DATABASE_URL` (required) | [mongoDB](https://www.mongodb.com) URI. Get this value from [mongoDB](https://www.mongodb.com). For more help watch this [video](https://youtu.be/1G1XwEOnxxo) |
| `LOG_CHANNEL` (optional)  | A log channel ID for the bot to post log messages                                                                                                              |
| `CRYPTO_PAY_API_KEY` (required)  | Get the API key for crypto payment through [Crypto Pay](https://t.me/CryptoBot). Type /pay and click on Create app                                                                                                    |
| `PROVIDER_TOKEN` (required)  | Get API key for card payment from [Bot Father](https://t.me/botfather)                                                                                                      |
| `PAYMENT_TESTING` (True or False) (optional)  | Set True if you are just testing the payment integration, Note: You have to enter test keys if you set this var to True                                                                                                          |

## Usage

To use the Chat-GPt3 bot, send it a message in a private chat. Then, make a prompt and the bot will reply with an answer.

Here are some examples of prompts you can use:

    Got any creative ideas for a 10 year old’s birthday?
    How do I make an HTTP request in Javascript?
    Explain quantum computing in simple terms
    Make a simple Flask Server
    Write a blog on time Managament
    Write a simple telegram bot
    Debug this code
    Suggest Some Horror Movies

In addition to answering user questions, the Chat-GPt3 bot also supports the following commands:

    start - Start the bot and receive a welcome message.
    pay - Get the payment link for the bot.
    examples - Display some examples of prompts you can use with the bot.
    ban - Ban a user from using the bot.
    unban - Unban a user from using the bot.

## Deploy

You can deploy this bot anywhere.

| Name   | Deploy                                                                                                                                                                                                                       |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Replit | [Deploy](https://replit.com/github/kevinnadar22/Chat-GPT3-Bot)                                                                                                                                                               |
| Heroku | [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kevinnadar22/Chat-GPT3-Bot)                                                                                   |
| Koyeb  | [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/apps/deploy?type=git&repository=kevinnadar22/Chat-GPT3-Bot&name=Chat-GPT3-Bot&run_command=python3%20-m%20main&branch=main) |
| VPS    | Deploy On Your own                                                                                                                                                                                                           |

## License

The Chat-GPt3 bot is licensed under the MIT License. See LICENSE for more information.

## Credits

- [Kevin](https://github.com/kevinnadar22)
