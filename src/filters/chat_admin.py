from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery, InlineQuery, ChatMemberUpdated
from aiogram.exceptions import TelegramForbiddenError

from bot import bot


class ChatAdminFilter(Filter):
    def __init__(self):
        pass

    async def __call__(self, obj: Union[Message, CallbackQuery, InlineQuery, ChatMemberUpdated]) -> bool:
        if obj.from_user is None:
            return False

        if isinstance(obj, Message):
            chat = obj.chat
        elif isinstance(obj, CallbackQuery) and obj.message:
            chat = obj.message.chat
        elif isinstance(obj, ChatMemberUpdated):
            chat = obj.chat
        else:
            return False

        if chat.type == 'private':
            return False

        chat_ids = [chat.id]

        try:
            admins = [member.user.id for chat_id in chat_ids for member in await bot.get_chat_administrators(chat_id)]
        except TelegramForbiddenError:
            return False

        return obj.from_user.id in admins

