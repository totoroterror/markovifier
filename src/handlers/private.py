from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.chat_type import ChatTypeFilter
from utilities import strip_indents


router = Router(name='private')


@router.message(
    ChatTypeFilter(chat_type="private"),
    Command(commands=["start"]),
)
async def private(message: Message) -> None:
    """
    This handler will be called when user sends `/start` or `/help` command.
    """

    if message.from_user is None:
        return

    text = strip_indents("""
        Hello there, {user}!

        I'm a bot that can generate funny messages based on previous messages in the chat.

        Actually, I don't work in private chats yet, so you can't use me there.

        But you can use me in groups, where I can generate funny messages based on previous messages in the chat.
    """).format(
        user=message.from_user.mention_html()
    )

    await message.reply(text)


@router.message(
    ChatTypeFilter(chat_type="private"),
)
async def fallback(message: Message) -> None:
    text = strip_indents("""
        I don't work in private chats yet, so you can't use me there.
    """)

    await message.reply(text)
