from pyrogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button

class Messages(object):
    START_MESSAGE = "I am a large language model trained by OpenAI. I can understand and generate text in many different languages and styles. I am not a person, but a program designed to assist with a variety of tasks, such as answering questions and providing information. I do not have personal experiences or opinions, and I am not capable of browsing the internet or accessing other external information. I can only provide information based on my pre-existing knowledge and training.\n\nGet started /examples"

    HELP_MESSAGE = "Just send me a message and I will try to answer it"

    ABOUT_MESSAGE = """
**🤖 About Me**

**👤 Name:** {bot_name}
**💻 Version:** {bot_version}
**🗣️ Language:** [Python 3.10.6](https://www.python.org/)
**📚 Library:** [Pyrogram](https://docs.pyrogram.org/)
"""

    GROUP_HELP_MESSAGE = """👋 Hello there! I'm ChatGPT, your friendly neighborhood AI language model. I'm here to help you with any questions or prompts you might have. 

🤖 To use me, **simply mention me in your message** or **type /ask followed by your question or prompt**. I'll do my best to provide a helpful response!

🗣️ Please note that I will only respond when I'm mentioned or when you use the /ask command. This is to ensure that I don't spam the group with unnecessary messages.

🤔 Need some inspiration for what to ask me? Here are some examples:

- `@{bot_username} What is the meaning of life?`
- `@{bot_username} Can you tell me a joke?`
- `@{bot_username} What's the weather like today?`
- `@{bot_username} How do I solve a Rubik's Cube?`
- `@{bot_username} What's the capital of France?`

🌟 I'm constantly learning and improving, so if I don't know the answer to your question right away, don't worry! I'll do my best to find the information you need.

🙏 Thank you for using ChatGPT! Let's learn and explore together."""

class Buttons(object):
    HOME_BUTTONS = Markup(
        [
            [
                Button("Add To Your Group", url="https://telegram.me/{bot_username}?startgroup=true"),
            ],
            [
                Button("Help ℹ️", callback_data="help"),   
                Button("About 🧊", callback_data="about")
            ]
        ]
    )

    HELP_BUTTONS = Markup(
        [
            [
                Button("Home 🏠", callback_data="home"),
                Button("About 🧊", callback_data="about")
            ]
        ]
    )

    ABOUT_BUTTONS = Markup(
        [
            [
                Button("Home 🏠", callback_data="home"),
                Button("Help ℹ️", callback_data="help")
            ]
        ]
    )