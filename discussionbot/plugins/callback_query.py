from discussionbot import bot
from discussionbot.databasemanagement.db_session import *
from discussionbot.discussionprocess.JoinProcess import  JoinProcess
from discussionbot.filters import costum_filters as c_filters
from discussionbot.markup.InlineMarkup import InlineMarkup
from discussionbot.dynamicmessages import *

from discussionbot.games import get_games
from discussionbot.games.SequenceGame import SequenceGame
from discussionbot.games.TicTacToe import TitTacToe



from pyrogram.types import CallbackQuery


from pony.orm import *

@bot.on_callback_query(c_filters.callable_discussion_command("/discussion", "/Discussion"))
def on_callback_query_discussion(_, call):
    try:
        discussion = get_discussion(int(call.data))
    except ObjectNotFound:
        bot.answer_callback_query(call.id, text="An error has occurred")
        return
    bot.send_message(call.message.chat.id, discussion.name + "\n" + discussion.topic + "\n" + str(discussion.user_now), reply_markup=InlineMarkup.markup_entry_discussion())
    __ = JoinProcess(int(call.data), str(call.message.chat.id), str(call.message.id + 1), str(call.from_user.id))

@bot.on_callback_query(c_filters.callable_discussion_command("/shop"))
def on_shop_callback(_, call):

    if call.data == "0":
        msg = get_dynamic_message(call.message)
        msg.update(50)

@bot.on_callback_query(c_filters.callable_discussion_command("/sequence_game"))
def on_shop_callback(_, call):

    g: SequenceGame = get_games(call.message)
    if g is None:
        return

    if not g.onLoad:
        g.update_game(call.data)

@bot.on_callback_query(c_filters.callable_discussion_command("/tic_tac_toe"))
def on_tic_tac_toe(_, call : CallbackQuery):
    t : TitTacToe = get_games(call.message)
    if t is None:
        return

    t.move_player(call.message.from_user.id, call.data)

@bot.on_callback_query(c_filters.callable_discussion_command("/connect_4"))
def on_connect_4(_, call : CallbackQuery):

    c = get_games(call.message)
    if c is None:
        return

    c.move_player(call.message.from_user.id, call.data)


@bot.on_callback_query()
def on_call_back_query_discussion_process(_, call):
    if call.data == "join_to_discussion":
        msg = JoinProcess.messages[(str(call.message.chat.id), str(call.message.id))]
        msg.join_user_to_discussion()
        bot.send_message(call.message.chat.id, "Joinato con successo")




