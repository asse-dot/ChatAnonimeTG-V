from discussionbot.databasemanagement.db_session import *

class JoinProcess(object):

    messages = {}

    def __init__(self, discussion_id : int, chat_id : str, message_id : str, user : str):
        self.discussion_id = discussion_id
        self.chat_id = chat_id
        self.message_id = message_id
        self.user = user

        JoinProcess.messages[(self.chat_id, self.message_id)] = self

    def join_user_to_discussion(self):
        add_user_to_discussion(self.user, self.discussion_id)
        #JoinProcess.messages.pop((self.chat_id, self.message_id))
