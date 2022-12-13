from loguru import logger

from bot import bot, dp

from handlers import chat, private


def main() -> None:
    dp.include_router(chat)
    dp.include_router(private)

    dp.run_polling(bot)


if __name__ == '__main__':
    logger.info('Starting bot...')
    main()
