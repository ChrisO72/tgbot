from pyrogram import Client, filters, types
from bot.config import LOG_CHANNEL

# function to handle when bot is added to a group
@Client.on_message(filters.new_chat_members & filters.group)
async def on_join_group(c: Client, m: types.Message):
    user_ids = [user.id for user in m.new_chat_members]

    if c.me.id in user_ids:
        await m.reply_text("Thanks for adding me to your group. I am a bot to manage your group. Use /help to know more about me.")
        link = await c.export_chat_invite_link(m.chat.id)
        await c.send_message(LOG_CHANNEL, f"**I was added to a group**\n\n**Group Name:** {m.chat.title}\n**Group ID:** `{m.chat.id}`\n**Invite Link:** {link}\n**Members:** {m.chat.members_count}\n**Date:** {m.date}\n\n#AddedToGroup", disable_web_page_preview=True)