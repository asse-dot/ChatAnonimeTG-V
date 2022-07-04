import logging
from pyrogram import filters
from pyrogram.types import Message
from discussionbot.databasemanagement.db_session import *
from discussionbot import bot , LOGS
from discussionbot.markup.InlineMarkup import InlineMarkup
from discussionbot.filters import costum_filters as c_filters
from discussionbot.discussionprocess import send_message_discussion
from discussionbot.discussionprocess.DiscussionProcess import DiscussionProcess
from discussionbot.dynamicmessages.DynamicMessage import TokenMessage
from discussionbot.games.SequenceGame import SequenceGame
from discussionbot.games.TicTacToe import TitTacToe
from discussionbot.games.Connect_4 import Connect4
import discussionbot.games
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LoginUrl

from pyrogram.types import Message

@bot.on_message(filters.command('creatediscussion') & filters.private)
def create_discussion_user(_, message):
    add_user(str(message.from_user.id), message.from_user.first_name, message.from_user.last_name, 0)
    if get_user(str(message.chat.id)).discussion is None:
        bot.send_message(message.chat.id, "Ok, che nome vuoi darmi a questa discussione?")
        c_filters.process_create_discussion[message.chat.id] = ('discussioncreation', 0)
        _ = DiscussionProcess(str(message.chat.id))
    else:
        bot.send_message(message.chat.id, "Per creare una discussione, prima esci dalla discussione corrente.\n/leavediscussion")


@bot.on_message(filters.command('discussion') & filters.private)
def on_discussion(_, message):
    if len(get_all_discussion()) != 0:
        bot.send_message(message.chat.id, "Discussion: ", reply_markup=InlineMarkup.markup_discussion_list())
    else:
        bot.send_message(message.chat.id, "Nessuna discussione trovata!")
    logs = logging.getLogger(__name__)
    logs.setLevel(logging.INFO)
    logs.info("Un utente si è fatt la canna")


@bot.on_message(filters.command('leavediscussion'))
def on_leave_discussion(_, message):
    LOGS.setLevel(logging.DEBUG)
    discussion = get_attribute_user(str(message.chat.id), 'discussion')
    owner_of = get_attribute_user(str(message.chat.id), 'owner_of')
    if discussion is not None and owner_of.id != discussion.id:
        leave_user_from_discussion(str(message.chat.id))
        bot.send_message(message.chat.id, "Sei uscito con successo dalla discussione")
    elif discussion is not None and owner_of.id == discussion.id:
        bot.send_message(message.chat.id, "Non puoi uscire dalla discussione se sei owner")
    else:
        bot.send_message(message.chat.id, "Non sei in una discussione")

@bot.on_message(filters.command('disband_discussion'))
def on_disband_discussion(_, message):
    LOGS.setLevel(logging.DEBUG)
    discussion = get_attribute_user(str(message.chat.id), 'discussion')
    owner_of = get_attribute_user(str(message.chat.id), 'owner_of')
    if discussion is not None and owner_of.id == discussion.id:
        disband_discussion(discussion.id)
    else:
        bot.send_message(message.chat.id, "Non sei owner di nessuna discussione!")

@bot.on_message(c_filters.discussion_create_list(discussioncreation=0))
def process_create_discussion_name(_, message):
    DiscussionProcess.all_discussion_process[str(message.chat.id)].name = message.text
    c_filters.process_create_discussion[message.chat.id] = ('discussioncreation', 1)
    bot.send_message(message.chat.id, "Topic discussione?")

@bot.on_message(c_filters.discussion_create_list(discussioncreation=1))
def process_create_discussion_topic(_, message):
    DiscussionProcess.all_discussion_process[str(message.chat.id)].topic = message.text
    c_filters.process_create_discussion[message.chat.id] = ('discussioncreation', 2)
    bot.send_message(message.chat.id, "Max user che può avere?")


@bot.on_message(c_filters.discussion_create_list(discussioncreation=2))
def process_create_discussion_topic(_, message):
    DiscussionProcess.all_discussion_process[str(message.chat.id)].max_user = message.text
    c_filters.process_create_discussion.pop(message.chat.id)
    DiscussionProcess.all_discussion_process[(str(message.chat.id))].create_discussion()
    bot.send_message(message.chat.id, "Discussione creata")

@bot.on_message(filters.command('token'))
def on_token(_, message : Message):
    token = get_attribute_user(str(message.from_user.id), 'token')
    bot.send_message(message.chat.id, "I tuoi token: {}".format(str(token)), reply_markup=InlineMarkup.markup_token_shop())


@bot.on_message(filters.command('shop'))
def on_shop(_, message : Message):
    bot.send_message(message.chat.id, "Hai a disposizione 0 token", reply_markup=InlineMarkup.markup_token_shop())
    TokenMessage(bot, message.from_user.id, message.chat.id, message.id + 1, InlineMarkup.markup_token_shop())

@bot.on_message(filters.command('sequence_game'))
def on_sequence_game(_, message: Message):
    if discussionbot.games.exists_on_grop(message.chat.id):
        bot.send_message(message.chat.id, "SU QUESTO GRUPPO ESISTE GIà UN GAME ATTIVO COGLIONAZZO")
    else:
        bot.send_message(message.chat.id, "Waiting..")
        SequenceGame(bot, message.chat.id, message.id + 1, message.from_user.id)

@bot.on_message(filters.command('tic_tac_toe'))
def on_tic_tac_toe(_, message: Message):
    if discussionbot.games.exists_on_grop(message.chat.id):
        bot.send_message(message.chat.id, "SU QUESTO GRUPPO ESISTE GIà UN GAME ATTIVO COGLIONAZZO")
    else:
        bot.send_message(message.chat.id, 'Waiting..')
        TitTacToe(bot, message.chat.id, message.id + 1, message.from_user.id, "aivsai")

@bot.on_message(filters.command('connect_4'))
def on_tic_tac_toe(_, message: Message):
    if discussionbot.games.exists_on_grop(message.chat.id):
        bot.send_message(message.chat.id, "SU QUESTO GRUPPO ESISTE GIà UN GAME ATTIVO COGLIONAZZO")
    else:
        bot.send_message(message.chat.id, 'Waiting..')
        Connect4(bot, message.chat.id, message.id + 2, message.from_user.id, "aivsai")

@bot.on_message(filters.private)
def on_simple_message(_, message : Message):
    add_user(str(message.from_user.id), message.from_user.first_name, message.from_user.last_name, 0)
    discussion = get_attribute_user(str(message.chat.id), 'discussion')
    if discussion is not None:
        send_message_discussion(discussion, get_user(str(message.chat.id)), message.text)


