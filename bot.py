import datetime
import os
import pickle

# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from cl.Skyline import Skyline
from cl.SkylineLexer import SkylineLexer
from cl.SkylineParser import SkylineParser
from cl.EvalVisitor import EvalVisitor
from antlr4 import InputStream, CommonTokenStream


def parseExpr(update, context):
    input_stream = InputStream(update.message.text)
    lexer = SkylineLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SkylineParser(token_stream)
    tree = parser.root()
    # print(tree.toStringTree(recog=parser))
    uid = str(update.effective_chat.id)

    if uid not in context.user_data:
        context.user_data[uid] = EvalVisitor()
    visitor = context.user_data[uid]
    s = visitor.visit(tree)

    fileName = str(update.effective_chat.id)+'.png'
    s.draw(fileName)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(fileName, 'rb'))

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=s.stats())
    os.remove(fileName)
    # text=update.message.text)

# defineix una funció que saluda i que s'executarà
# quan el bot rebi el missatge /start


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello there!\nUse /help to see available commands.")


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("Commands:"
              "\n/start : start conversation with bot"
              "\n/help : show list of all possible commands and brief documentation"
              "\n/author : show author name and email"
              "\n/lst: show defined identifiers and their area"
              "\n/clean: delete all defined identifiers"
              "\n/save id: save a defined Skyline with identifier 'id' to a file 'id.sky'"
              "\n/load id: load and define a Skyline from the file 'id.sky'"
              "\nBuild Skyline operations:"
              "\n(start,height,end) : Skyline with height, start, and end being integers"
              "\n[(start,height,end),(a,b,c),...] : Skyline several buildings"
              "\n{n,h,w,xmin,xmax} : Skyline with n Buildings with height=[0,h], width=[1,w] and start=[xmin,xmax]"
              "\nSupports operations: "
              "\nSkyline * Skyline to find intersection"
              "\nSkyline + Skyline to find union"
              "\nSkyline * N : N(integer)=[0,inf), replicate Skyline N times and to the right."
              "\nSkyline + N : N(integer)=[0,inf), move N units to the right"
              "\nSkyline - N : N(integer)=[0,inf), move N units to the left"
              "\n-Skyline : show mirrored Skyline with respect to the y axis"
              "\nid := Skyline"
              ))


def author(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Mi autor es Vicente Coves Beneyto, \
    \ncorreo: vicente.coves@est.fib.upc.edu")


def lst(update, context):
    uid = str(update.effective_chat.id)
    if uid not in context.user_data:
        context.user_data[uid] = EvalVisitor()
    st = context.user_data[uid].symbolTable
    msg = "\n".join([skID + " has area = " +
                     str(st[skID].area) for skID in st])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="IDs and their info: \n" + msg)


def clean(update, context):
    uid = str(update.effective_chat.id)
    if uid not in context.user_data:
        context.user_data[uid] = EvalVisitor()
    context.user_data[uid].symbolTable = {}
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="All Skylines have been deleted")


def exit(update, context, msg):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg)


def save(update, context):
    try:
        # filePath = ./persistence/uid/id.sky
        skID = (context.args[0])
        uid = str(update.effective_chat.id)
        if uid not in context.user_data:
            context.user_data[uid]
            return exit(update, context, ": Empty table")
        if skID not in context.user_data[uid].symbolTable:
            return exit(update, context, ": Identifier does not exist")
        original = os.getcwd()
        if not os.path.exists("persistence"):
            os.mkdir("persistence")
        os.chdir("persistence")
        if not os.path.exists(uid):
            os.mkdir(uid)
        os.chdir(uid)
        fileName = skID + '.sky'
        with open(fileName, "wb") as f:
            pickle.dump(context.user_data[uid].symbolTable[skID], f)
        os.chdir(original)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=skID + ' saved succesfully')
    except Exception:
        exit(update, context, "💣 : la liaste güei")


def load(update, context):
    try:
        skID = (context.args[0])
        uid = str(update.effective_chat.id)
        original = os.getcwd()
        if not os.path.exists("persistence"):
            os.mkdir("persistence")
        os.chdir("persistence")
        if not os.path.exists(uid):
            os.mkdir(uid)
        os.chdir(uid)
        fileName = skID + '.sky'
        if not os.path.exists(fileName):
            raise Exception("file not found")
        with open(fileName, "rb") as f:
            context.user_data[uid].symbolTable[skID] = pickle.load(f)
        os.chdir(original)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=skID + ' loaded succesfully')
    except Exception:
        exit(update, context, "💣 : la liaste güei")


def time(update, context):
    message = str(datetime.datetime.now())
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="La time es " + message)


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('lst', lst))
dispatcher.add_handler(CommandHandler('clean', clean))
dispatcher.add_handler(CommandHandler('save', save))
dispatcher.add_handler(CommandHandler('load', load))
dispatcher.add_handler(CommandHandler('time', time))
dispatcher.add_handler(MessageHandler(Filters.text, parseExpr))

# engega el bot
updater.start_polling()
