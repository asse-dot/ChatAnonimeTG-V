from discussionbot.databasemanagement.db_session import *
from discussionbot import bot

def send_message_discussion(discussion: Discussion, ignore: User, message: str) -> None:
    l = discussion.get_all_users()
    for user in l:
        # if user.id_tg == ignore.id_tg:

        if get_user_owner_of(user.id_tg).id != discussion.id:
            bot.send_message(user.id_tg, "user" + str(l.index(user) + 1) + ": " + message)
        else:
            bot.send_message(user.id_tg, "Owner: " + message)
