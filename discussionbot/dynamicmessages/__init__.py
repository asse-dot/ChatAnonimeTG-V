from discussionbot.dynamicmessages.DynamicMessage import DynamicMessage
from pyrogram.types import Message

def get_dynamic_message(message : Message) -> DynamicMessage:

    return DynamicMessage.messages[(message.chat.id, message.id)]