from discussionbot.games.Games import Games
from pyrogram.types import Message

def get_games(message : Message)  -> Games:
    try:
        g = Games.all_games[(message.chat.id, message.id)]
    except KeyError:
        return

    return g

def exists_on_grop(group : str) -> bool:

    for game in Games.all_games.values():
        if game.id_group == group:
            return True
    return False