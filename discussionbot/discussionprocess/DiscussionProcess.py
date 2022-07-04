from typing import Dict, Any

from discussionbot.databasemanagement.db_session import *

class DiscussionProcess(object):

    all_discussion_process = {}

    def __init__(self, user: str):
        self.user = user
        DiscussionProcess.all_discussion_process[user] = self

        # Attributi per discussione
        self.name = None
        self.topic = None
        self.max_user = None

    def create_discussion(self):
        add_discussion(self.name, self.topic, self.max_user, self.user)
        DiscussionProcess.all_discussion_process.pop(self.user)