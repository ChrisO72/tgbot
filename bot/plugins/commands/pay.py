import html
from typing import Dict

from crypto_pay_api_sdk import cryptopay
from pyrogram import Client, filters
from pyrogram.types import Message, User, Chat, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.raw.types import (
    InputMediaInvoice,
    DataJSON,
    Invoice,
    LabeledPrice,
    UpdateBotPrecheckoutQuery
)
from pyrogram.raw.functions.messages import (
    SendMedia,
    SetBotPrecheckoutResults
)

from bot.config import LOG_CHANNEL, PROVIDER_TOKEN, CRYPTO_PAY_API_KEY, PAYMENT_TESTING
from bot.plugins.handlers import on_checkout_query


@Client.on_message(filters.private & filters.command("pay"))
async def pay_command_handler(bot: Client, msg: Message):
    text = "Choose an option to pay:"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Card",
                    callback_data="card",
                ),
                InlineKeyboardButton(
                    text="Crypto",
                    callback_data="crypto",
                ),
            ],
        ]
    )
    await msg.reply(
        text=text,
        reply_markup=keyboard,
    )


@Client.on_callback_query(filters.regex(r"crypto"))
async def send_invoice_crypto(bot: Client, update: CallbackQuery):
    # default testnet = False
    crypto = cryptopay.Crypto(CRYPTO_PAY_API_KEY, testnet=PAYMENT_TESTING)
    coins = crypto.getCurrencies()
    blockchain_coins = [coin for coin in coins["result"]
                        if coin["is_blockchain"] == True or coin["is_stablecoin"] == True]

    buttons = [
        [
            InlineKeyboardButton(
                text=coin["name"],
                callback_data=f"coin_{coin['code']}",
            )
        ] for coin in blockchain_coins
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text="Choose a coin to pay:",
        reply_markup=keyboard,
    )


@Client.on_callback_query(filters.regex(r"coin_"))
async def send_invoice_coin(bot: Client, update: CallbackQuery):
    coin = update.data.split("_")[1]
    crypto = cryptopay.Crypto(CRYPTO_PAY_API_KEY, testnet=PAYMENT_TESTING)
    coins = crypto.getExchangeRates()
    USD = 100
    sts = await update.message.reply_text(
        "Getting exchange rate...",
    )
    for x in coins["result"]:
        if x['source'] == coin and x['target'] == 'USD':
            rate = x['rate']
            amount = USD / float(rate)
    await sts.delete()
    invoice = crypto.createInvoice(
        asset=coin,
        amount=amount
    )
    invoice_id = invoice["result"]["invoice_id"]
    await update.message.edit_text(
        text="Pay and Enjoy your purchase! ",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Pay ${USD} in {coin}",
                        url=invoice["result"]["pay_url"],
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Payment Done",
                        callback_data=f"check_{invoice_id}",
                    )
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex(r"check_"))
async def check_invoice(bot: Client, update: CallbackQuery):
    invoice_id = update.data.split("_")[1]
    crypto = cryptopay.Crypto(CRYPTO_PAY_API_KEY, testnet=PAYMENT_TESTING)
    invoice =  crypto.getInvoices(params = {"invoice_ids": invoice_id})

    for x in invoice["result"]["items"]:
        if x["invoice_id"] == int(invoice_id):
            invoice = x

    if invoice["status"] == "paid":
        await update.message.edit_text(
            text="You successfully bought something.",
        )
        await bot.send_message(
            LOG_CHANNEL,
            f"User {update.from_user.mention} bought something for ${invoice['amount']} in {invoice['asset']}",
        )
    else:
        await update.answer(
            text="You have not paid yet.",
            show_alert=True,
        )


@Client.on_callback_query(filters.regex(r"card"))
async def send_invoice_card(bot: Client, update: CallbackQuery):
    invoice = Invoice(
        currency="USD",
        prices=[
            LabeledPrice(amount=10000, label="Premium"),
        ],
        test=PAYMENT_TESTING,  # Remove this line for production,
        name_requested=True,
        phone_requested=True,
        email_requested=True,
        flexible=True,
        phone_to_provider=True,
        email_to_provider=True,
        max_tip_amount=500,
        suggested_tip_amounts=[100, 200],
    )

    chat_id = update.message.chat.id
    r = await bot.invoke(
        SendMedia(
            peer=await bot.resolve_peer(chat_id),
            media=InputMediaInvoice(
                title="Pay from card",
                description="Pay and Enjoy Our Service",
                invoice=invoice,
                payload=f"{update.from_user.id}_bought".encode(),
                provider=PROVIDER_TOKEN,
                provider_data=DataJSON(data="{}"),
                start_param="start_param",
            ),
            message="",
            random_id=bot.rnd_id(),
            noforwards=True,
        )
    )


@on_checkout_query
async def process_checkout_query(
    bot: Client,
    query: UpdateBotPrecheckoutQuery,
    users: Dict[int, User],
    chats: Dict[int, Chat],
):
    payload = html.escape(str(query))
    await bot.send_message(
        chat_id=query.user_id, text="You successfully bought our service."
    )
    await bot.send_message(
        LOG_CHANNEL,
        f"User {query.user_id} bought something\n\n{payload}",
    )
    return await bot.invoke(
        SetBotPrecheckoutResults(
            query_id=query.query_id,
            success=True,
            error=None,
        )
    )
