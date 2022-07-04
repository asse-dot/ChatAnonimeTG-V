from pyrogram import Client

class DynamicMessage(object):

    messages = {}

    def __init__(self, bot : Client, owner : str, chat : str, message_id : str):

        self.bot = bot
        self.owner = owner
        self.chat = chat
        self.message_id = message_id

        DynamicMessage.messages[(self.chat, self.message_id)] = self


class TokenMessage(DynamicMessage):

    def __init__(self, bot : Client, owner : str, chat : str, message_id : str, markup):
        super().__init__(bot, owner, chat, message_id)
        self.token = 0
        self.markup = markup

    def update(self, n):
        self.token += n
        self.update_message()

    def reset(self, n):
        self.token = n
        self.update_message()

    def update_message(self):
        self.bot.edit_message_text(self.chat, self.message_id,  "Hai a disposizione: " + str(self.token),
                                   reply_markup=self.markup)


