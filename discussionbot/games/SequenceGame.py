from discussionbot.games.Games import Games
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import emoji
import random
import time


class SequenceGame(Games):
    INITIAL_ATTEMPTS = 3
    TABLE = {
        "0": (0, 0),
        "1": (0, 1),
        "2": (0, 2),
        "3": (1, 0),
        "4": (1, 1),
        "5": (1, 2),
        "6": (2, 0),
        "7": (2, 1),
        "8": (2, 2)

    }

    def __init__(self, bot: Client, id_group, id_message, id_user):
        super().__init__(bot, id_group, id_message, id_user)
        self.attempts = SequenceGame.INITIAL_ATTEMPTS
        self.buttons = [
            [
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="0"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="1"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="2")
            ],
            [
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="3"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="4"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="5")
            ],
            [
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="6"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="7"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="8")

            ]
        ]
        self.sequence = self.generate_sequence()
        self.currButton = 0
        self.onLoad = True
        self.init_table_tg()

    def init_table_tg(self):
        _str = "Memorizza la sequenza: "
        self.bot.edit_message_text(self.id_group, self.id_message, _str,
                                   reply_markup=InlineKeyboardMarkup(self.buttons))
        time.sleep(2)
        for t in self.sequence:
            self.buttons[t[0]][t[1]] = InlineKeyboardButton(text=emoji.emojize(":blue_square:"),
                                                            callback_data=self.buttons[t[0]][t[1]].callback_data)
            self.bot.edit_message_text(self.id_group, self.id_message, _str,
                                       reply_markup=InlineKeyboardMarkup(self.buttons))
            time.sleep(2)

        self.buttons = [
            [
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="0"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="1"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="2")
            ],
            [
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="3"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="4"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="5")
            ],
            [
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="6"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="7"),
                InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="8")

            ]
        ]
        self.bot.edit_message_text(self.id_group, self.id_message, "Ora prova tu: \n Tentativi: " + str(self.attempts),
                                   reply_markup=InlineKeyboardMarkup(self.buttons))
        self.onLoad = False

    def generate_sequence(self) -> list:

        g = []
        l = [i for i in range(9)]
        for i in range(9):
            n = random.choice(l)
            l.remove(n)
            g.append(SequenceGame.TABLE[str(n)])

        return g

    def update_game(self, button: str):

        if SequenceGame.TABLE[button] == self.sequence[self.currButton]:
            t = self.sequence[self.currButton]
            self.buttons[t[0]][t[1]] = InlineKeyboardButton(text=emoji.emojize(":blue_square:"),
                                                            callback_data=self.buttons[t[0]][t[1]].callback_data)
            self.bot.edit_message_text(self.id_group, self.id_message,
                                       "Ora prova tu: \n Tentativi: " + str(self.attempts),
                                       reply_markup=InlineKeyboardMarkup(self.buttons))
            self.currButton += 1
            if self.currButton == 8:
                self.bot.edit_message_text(self.id_group, self.id_message,
                                           "Hai vinto!!")
                SequenceGame.all_games.pop((self.id_group, self.id_message))

        else:
            self.attempts -= 1
            if self.attempts <= 0:
                self.bot.edit_message_text(self.id_group, self.id_message,
                                           "Mi dispiace, hai perso!")
                SequenceGame.all_games.pop((self.id_group, self.id_message))
            else:
                self.buttons = [
                    [
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="0"),
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="1"),
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="2")
                    ],
                    [
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="3"),
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="4"),
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="5")
                    ],
                    [
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="6"),
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="7"),
                        InlineKeyboardButton(text=emoji.emojize(":red_square:"), callback_data="8")

                    ]
                ]
                self.bot.edit_message_text(self.id_group, self.id_message,
                                           "Ora prova tu: \n Tentativi: " + str(self.attempts),
                                           reply_markup=InlineKeyboardMarkup(self.buttons))
                self.currButton = 0
