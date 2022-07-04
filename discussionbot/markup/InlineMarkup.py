from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from discussionbot.databasemanagement.db_session import *

class InlineMarkup(object):

    @staticmethod
    def markup_discussion_list():
        button = []
        for discussion in get_all_discussion():
            button.append([InlineKeyboardButton(
                discussion.name + " " + str(discussion.user_now) + "/" + str(discussion.max_user),
                callback_data=str(discussion.id)), ])

        return InlineKeyboardMarkup(button)

    @staticmethod
    def markup_token_shop():
        button = [
            [
                InlineKeyboardButton("0", callback_data="0"),
            ]
        ]

        return InlineKeyboardMarkup(button)

    @staticmethod
    def markup_entry_discussion():
        button = [
            [
                InlineKeyboardButton("Join", callback_data="join_to_discussion"),
            ],

            [
                InlineKeyboardButton("Delete", callback_data="delete_join_discussion"),
            ]
        ]

        return InlineKeyboardMarkup(button)
