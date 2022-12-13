import imp
import random
from time import time

from aiogram import Bot, Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command

from loguru import logger

from filters import ChatTypeFilter, ChatAdminFilter
from utilities import strip_indent

from group_data import GroupData
from database import redis

from bot import bot
from config import config


router = Router(name='chat')


groups = {}
rate_limits = {}


@router.message(
    ChatTypeFilter(chat_type=['supergroup', 'group']),
    Command(commands=['clear']),
    ChatAdminFilter(),
)
async def clear(message: Message) -> None:
    """
    This handler will be called when user sends `/clear` command.
    """

    await redis.lrem(f'chat:{message.chat.id}:messages', 0, '*')

    groups[message.chat.id] = GroupData(message.chat.id)

    text = strip_indent("""
        History of this chat has been cleared.
    """)

    await message.reply(text)


@router.message(
    ChatTypeFilter(chat_type=['supergroup', 'group']),
    Command(commands=['generate']),
)
async def generate(message: Message) -> None:
    """
    This handler will be called when user sends `/generate` command.
    """

    if message.chat.id not in groups:
        messages = await redis.lrange(f'chat:{message.chat.id}:messages', 0, -1)

        messages = [message.decode('utf-8') for message in messages]

        groups[message.chat.id] = GroupData(message.chat.id, messages)

    text = groups[message.chat.id].generate()

    if text is None:
        text = strip_indent("""
            I don't have enough data to generate a message.
        """)
    else:
        await redis.incr(f'chat:{message.chat.id}:messages_sent')

    await message.answer(text)


@router.message(
    ChatTypeFilter(chat_type=['supergroup', 'group']),
    Command(commands=['stats', 'statistics', 'info']),
)
async def stats(message: Message) -> None:
    """
    This handler will be called when user sends `/stats` command.
    """

    messages_count: int = await redis.llen(f'chat:{message.chat.id}:messages')
    messages_sent_data = await redis.get(f'chat:{message.chat.id}:messages_sent')

    if messages_sent_data is None:
        messages_sent = 0
    else:
        messages_sent = int(messages_sent_data)


    text = strip_indent("""
        🤖 Information about this chat:
        · I have generated {messages_sent} messages.
        · I have {messages_count} messages in my database.

        Created using aiogram with ❤️ by @totorodevelopment
    """).format(
        messages_sent=messages_sent,
        messages_count=messages_count
    )

    await message.answer(text)


@router.message(
    ChatTypeFilter(chat_type=['supergroup', 'group']),

)
async def fallback(message: Message) -> None:
    if message.text is None:
        return

    text_to_push = message.text.replace("\"", "").replace("\'", "")

    if message.chat.id not in groups:
        messages = await redis.lrange(f'chat:{message.chat.id}:messages', 0, -1)

        messages = [message.decode('utf-8') for message in messages]

        groups[message.chat.id] = GroupData(message.chat.id, messages)

    groups[message.chat.id].add_message(message.text)

    await redis.lpush(f'chat:{message.chat.id}:messages', text_to_push)

    if random.randint(1, 100) > config.MESSAGE_CHANCE:
        return

    if message.chat.id not in rate_limits:
        rate_limits[message.chat.id] = 0

    if time() - rate_limits[message.chat.id] < config.MESSAGE_RATE_LIMIT:
        return

    rate_limits[message.chat.id] = time()

    text = groups[message.chat.id].generate()

    if text is None:
        return

    await redis.incr(f'chat:{message.chat.id}:messages_sent')

    await message.answer(text)


@router.my_chat_member()
async def my_chat_member(event: ChatMemberUpdated) -> None:
    """
    This handler will be called when bot's chat member status is changed.
    """

    logger.debug(
        'Bot\'s chat members status has changed in {chat_id}: {old_status} -> {new_status}',
        chat_id=event.chat.id,
        old_status=event.old_chat_member.status,
        new_status=event.new_chat_member.status
    )

    match event.new_chat_member.status:
        case 'administrator':
            text = strip_indent("""
                Now I'm an administrator in this chat, fron now I will collect messages and generate new funny ones.
            """)

            await bot.send_message(event.chat.id, text)

        case 'member':
            if event.old_chat_member.status == 'administrator':
                text = strip_indent("""
                    I'm not an administrator anymore, I will stop collecting messages and generating new ones.
                """)

                await bot.send_message(event.chat.id, text)
            elif event.old_chat_member.status == 'left':
                messages = await redis.lrange(f'chat:{event.chat.id}:messages', 0, -1)

                messages = [message.decode('utf-8') for message in messages]

                groups[event.chat.id] = GroupData(event.chat.id, messages)

                text = strip_indent("""
                    Thanks for adding me into this chat.

                    Please, make me an administrator to start collecting messages and generating new ones.
                """)

                await bot.send_message(event.chat.id, text)
        case 'left', 'kicked', 'banned':
            del groups[event.chat.id]
