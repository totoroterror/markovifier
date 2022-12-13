# Markovifier

Simple Python bot that can generate funny messages in Telegram chats based on previous messages using markov chain.

## Building docker image

1. Make sure that docker is installed
2. Run `docker build -t tag .` (replace `tag` with your image name)

## Dependencies

- aiogram · *3.0.0b6* · telegram api wrapper
- markovify · markov chain library
- redis · library to store all previous messages in chat
- loguru · simple logger

## Support me

You can support my further developments or support this project by buying me a coffee or pizza.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/totoroterror)
