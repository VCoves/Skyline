# Skyline Telegram Bot

It is a python Telegram Bot that parses expressions with antlr4 in order to build Skylines.
It supports saving and loading Skylines, even after the bot goes offline.
Detailed explanation [here](https://gebakx.github.io/SkylineBot/)

## Getting started
First send /start via to the Telegram [bot](http://t.me/VicMacBot),
Use /help to see all commands and description on operations
To run the bot you need a token and previously compile the grammar Skyline.g with compile.bat (you need to have the antlr4 executable in the path or in the same folder)

### Prerequisites
matplotlib==3.1.1
python-telegram-bot==12.
antlr4-python3-runtime==4.8
which you can download from this link:  [antlr4](https://pypi.org/project/antlr4-python3-runtime/) 
The rest of the libraries are standard for Python 3, my exact version was [Python 3.7.2](https://www.python.org/downloads/release/python-372/)

## Built With

* [Python 3](https://www.python.org/)
* [antlr4](https://www.antlr.org/)

## Authors

* **Vicente Coves Beneyto** - [VCoves](https://github.com/VCoves)

## License

This project is licensed under the MIT License