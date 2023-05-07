from pyrogram import Client, filters, types
from bot.config import ADMINS


@Client.on_message(filters.command('reset_db') & filters.private & filters.incoming & filters.user(ADMINS))
async def reset_db(c: Client, m: types.Message):
    text = "Warning: This will delete all the data from the database, are you sure you want to continue?"
    return await m.reply(text, reply_markup=types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    "Yes", callback_data="reset_db_yes"),
                types.InlineKeyboardButton("No", callback_data="reset_db_no")
            ]
        ]
    ))
