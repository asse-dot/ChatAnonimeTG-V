from discussionbot.games.Games import Games
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import emoji
import time


class TitTacToe(Games):
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
    cross = "multiply"
    circle = "red_circle"

    def __init__(self, bot: Client, id_group, id_message, id_user, key):
        super().__init__(bot, id_group, id_message, id_user)
        self.key = key
        self.ai = self.cross if key == self.circle else self.circle
        self.table = [
            [
                InlineKeyboardButton(text="-", callback_data="0"),
                InlineKeyboardButton(text="-", callback_data="1"),
                InlineKeyboardButton(text="-", callback_data="2")
            ],
            [
                InlineKeyboardButton(text="-", callback_data="3"),
                InlineKeyboardButton(text="-", callback_data="4"),
                InlineKeyboardButton(text="-", callback_data="5")
            ],
            [
                InlineKeyboardButton(text="-", callback_data="6"),
                InlineKeyboardButton(text="-", callback_data="7"),
                InlineKeyboardButton(text="-", callback_data="8")

            ]
        ]
        self.board = [
            [
                '-',
                '-',
                '-'
            ],
            [
                '-',
                '-',
                '-'
            ],
            [
                '-',
                '-',
                '-'
            ]
        ]
        if self.key == "aivsai":
            self.ai_vs_ai()
            return

        if self.ai == self.cross:
            a = self.take_best_move(self.board.copy())
            self.table[a[0]][a[1]] = InlineKeyboardButton(text=emoji.emojize(":{}:".format(self.ai)),
                                                          callback_data=self.table[a[0]][a[1]].callback_data)
            self.board[a[0]][a[1]] = self.ai
            self.bot.edit_message_text(self.id_group, self.id_message, "Gioca: ",
                                       reply_markup=InlineKeyboardMarkup(self.table))
        else:
            self.bot.edit_message_text(self.id_group, self.id_message, "Gioca: ",
                                       reply_markup=InlineKeyboardMarkup(self.table))

    def ai_vs_ai(self):
        cont = 0
        while True:
            self.ai = self.cross if cont % 2 == 0 else self.circle
            a = self.take_best_move(self.board.copy(), 2) if self.ai == self.cross else  self.take_best_move(self.board.copy(), 8)
            if len(a) != 0:
                self.table[a[0]][a[1]] = InlineKeyboardButton(text=emoji.emojize(":{}:".format(self.ai)),
                                                                callback_data=self.table[a[0]][a[1]].callback_data)
                self.board[a[0]][a[1]] = self.ai
                self.bot.edit_message_text(self.id_group, self.id_message, "Gioca: ", reply_markup=InlineKeyboardMarkup(self.table))

            x = self.check_win(self.board, 0)
            if x != -100:
                if x == 10:
                    self.bot.edit_message_text(self.id_group, self.id_message, "CROCE HA VINTO")
                elif x == -10:
                    self.bot.edit_message_text(self.id_group, self.id_message, "HA VINTO CERCHIO")

                elif x == 0:
                    self.bot.edit_message_text(self.id_group, self.id_message, "PAREGGIO")

                TitTacToe.all_games.pop((self.id_group, self.id_message))
                break

            cont += 1
            time.sleep(2)

    def move_player(self, player, move):

        table_move = TitTacToe.TABLE[str(move)]
        if self.table[table_move[0]][table_move[1]].text == "-":
            self.table[table_move[0]][table_move[1]] = InlineKeyboardButton(text=emoji.emojize(":{}:".format(self.key)),
                                                                callback_data=self.table[table_move[0]][table_move[1]].callback_data)
            self.board[table_move[0]][table_move[1]] = self.key
            self.bot.edit_message_text(self.id_group, self.id_message, "Gioca: ", reply_markup=InlineKeyboardMarkup(self.table))

            #AI move
            a = self.take_best_move(self.board.copy())
            if len(a) != 0:
                self.table[a[0]][a[1]] = InlineKeyboardButton(text=emoji.emojize(":{}:".format(self.ai)),
                                                                callback_data=self.table[a[0]][a[1]].callback_data)
                self.board[a[0]][a[1]] = self.ai
                self.bot.edit_message_text(self.id_group, self.id_message, "Gioca: ", reply_markup=InlineKeyboardMarkup(self.table))

            x = self.check_win(self.board, 0)
            if x != -100:
                if x == 10:
                    self.bot.edit_message_text(self.id_group, self.id_message, "CROCE HA VINTO")
                elif x == -10:
                    self.bot.edit_message_text(self.id_group, self.id_message, "HA VINTO CERCHIO")

                elif x == 0:
                    self.bot.edit_message_text(self.id_group, self.id_message, "PAREGGIO")

                TitTacToe.all_games.pop((self.id_group, self.id_message))

    def take_best_move(self, board, max_deep=-1) -> tuple:
        moves = {}
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    moves[(i, j)] = 0

        for move in moves.keys():
            board[move[0]][move[1]] = self.cross if self.ai == self.cross else self.circle
            moves[move] = self.mini_max(board, False, 0, max_deep) if self.ai == self.cross else self.mini_max(board, True, 0, max_deep)
            board[move[0]][move[1]] = '-'
        print(moves)
        k = -10000 if self.ai == self.cross else 10000
        t = []
        for _ in moves.keys():
            if moves[_] > k and self.ai == self.cross:
                k = moves[_]

            if moves[_] < k and self.ai == self.circle:
                k = moves[_]

        for _ in moves.keys():
            if moves[_] == k: t.append(_)

        return random.choice(t)

    def check_win(self, board, deep) -> int:
        win_state = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1,1), (2, 1)],
            [(0, 2), (1,2), (2,2)],
            [(0, 0), (1,1), (2,2)],
            [(0, 2), (1,1), (2, 0)]
        ]
        C1, C2 = True, True
        for __ in win_state:
            for _ in __:
                C1 = (board[_[0]][_[1]] == self.cross) and C1
                C2 = (board[_[0]][_[1]] == self.circle) and C2

            if C1:
                return 10 - deep
            elif C2:
                return -10 + deep
            C1, C2 = True, True

        draw = True
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-": draw = False
        if draw: return 0

        return -100






    def mini_max(self, board, is_max, deep, max_deep) -> int:
        if deep == max_deep: return 0
        if self.check_win(board, deep) != -100: return self.check_win(board, deep)

        if is_max:
            x = -100000
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = self.cross
                        x = max(x, self.mini_max(board, not is_max, deep + 1, max_deep))
                        board[i][j] = "-"
        else:
            x = 10000
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '-':
                        board[i][j] = self.circle
                        x = min(x, self.mini_max(board, not is_max, deep + 1, max_deep))
                        board[i][j] = "-"
        return x


def min(a, b):
    if a < b: return a
    return b

def max(a, b):
    if a > b: return a
    return b
