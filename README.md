# Markovifier

Simple Python bot that can generate funny messages in Telegram chats based on previous messages using markov chain.

## Commands

- `/generate` · generate new message bypassing random chance and generation rate limit.
- `/statistics` (aliases: `/info`, `/stats`) · display chat's statistics
- `/clear` (chat admin only) · clear history of messages

## Installation

### Local machine

1. Install [Python 3.11](https://www.python.org/downloads/) or higher.
2. Install dependencies from `requirements.txt` (using `pip install -r requirements.txt`)
3. Launch `src/main.py` (using `python src/main.py`)

### Docker
#### Building docker image

1. Make sure that docker is installed
2. Run `docker build -t tag .` (replace `tag` with your image name)
3. Launch built docker image

## Dependencies

- aiogram · *3.0.0b6* · telegram api wrapper
- markovify · markov chain library
- redis · library to store all previous messages in chat
- loguru · simple logger

## Contributing

Pull Requests are always welcome!

## Support me

You can support my further developments or support this project by buying me a coffee or pizza.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/totoroterror)
