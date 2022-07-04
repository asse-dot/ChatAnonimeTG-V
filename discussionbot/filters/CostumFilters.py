from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery


class CostumFilters(object):

    def __init__(self, bot: Client):
        self.bot = bot
        self.process_create_discussion = {}

    def callable_discussion_command(self, *args):
        def callable_discussion(_, __, update : CallbackQuery):

            return bool(
                self.bot.get_messages(update.message.chat.id, update.message.id - 2).text in args)

        return filters.create(callable_discussion, "discussion_command")



    def discussion_create_list(self, **kwargs):
        def callable_discussion_create(_, __, update):
            if self.process_create_discussion.__contains__(update.chat.id):
                return kwargs[self.process_create_discussion[update.chat.id][0]] == self.process_create_discussion[update.chat.id][1]

            return False

        return filters.create(callable_discussion_create, "discussion_list_process")
