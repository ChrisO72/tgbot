from pyrogram import Client, filters, types
from database import db


@Client.on_callback_query(filters.regex("^reset_db_yes$"))
async def reset_db_yes(c: Client, m: types.CallbackQuery):
    await m.answer("Deleting all data from the database...")
    await m.message.delete()
    await db.reset_db()
    return await m.message.reply("Successfully deleted all data from the database")


@Client.on_callback_query(filters.regex("^reset_db_no$"))
async def reset_db_no(c: Client, m: types.CallbackQuery):
    await m.answer("Reset DB process cancelled")
    return await m.message.delete()
