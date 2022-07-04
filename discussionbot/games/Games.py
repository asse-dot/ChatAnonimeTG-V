from pyrogram import Client

class Games(object):

    all_games = {}

    def __init__(self, bot : Client,  id_group, id_message, user_id):
        self.bot = bot
        self.id_group = id_group
        self.id_message = id_message
        self.user_id = user_id
        Games.all_games[(self.id_group, self.id_message)] = self

    def check_is_owner(self, user_id : str) -> bool:
        return user_id == self.user_id
