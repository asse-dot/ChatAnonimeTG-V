from PIL import Image
from discussionbot.games.Games import Games
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import InputMediaPhoto
import time

import random


class Connect4(Games):
    board_img__ = "assests/board4.jpg"
    board = Image.open(r"assests/board4.jpg")
    p1 = Image.open(r"assests/p1.jpg")
    p2 = Image.open(r"assests/p2.jpg")
    pa_1 = 15
    pa_2 = 20
    d = 70

    STORAGE = -1001533273497

    def __init__(self, bot: Client, id_group, id_message, user_id, key):
        super().__init__(bot, id_group, id_message, user_id)
        self.key = key
        self.ai = "yellow" if key == "red" else "red"
        self.buttons = ["A5", "B5", "C5", "D5", "E5", "F5", "G5"]
        self.markup = self.create_markup(key, self.buttons)
        self.red, self.yellow = [], []
        self.bot.delete_messages(id_group, id_message - 1)
        with open(self.board_img__, "rb") as pic:
            self.bot.send_photo(id_group, pic, reply_markup=self.markup)
        with open(f"assests/{str(self.id_group) + str(self.id_message)}.jpg", 'a'): pass

        if key == "aivsai":
            self.ai_vs_ai()
            return

    def ai_vs_ai(self):
        cont = 0
        while True:
            self.ai = "red" if cont % 2 == 0 else "yellow"
            a = self.take_best_move(self.parse_board()) if cont != 0 else self.take_best_move(self.parse_board(), 2)
            if self.ai == "red":
                self.red.append(a)
            elif self.ai == "yellow":
                self.yellow.append(a)
            img = self.board_img()
            with open(img, "rb") as pic:
                pic = self.bot.send_photo(self.STORAGE, pic)
                self.bot.edit_message_media(self.id_group, self.id_message, media=InputMediaPhoto(pic.photo.file_id))

            x = self.check_win(self.parse_board(), 0)
            if x != -100:
                if x == 10:
                    self.bot.edit_message_text(self.id_group, self.id_message, "ROSSO HA VINTO")
                elif x == -10:
                    self.bot.edit_message_text(self.id_group, self.id_message, "GIALLO HA VINTO")
                elif x == 0:
                    self.bot.edit_message_text(self.id_group, self.id_message, "PAREGGIO")
                Connect4.all_games.pop((self.id_group, self.id_message))
                break

            time.sleep(2)
            cont += 1

    def move_player(self, player, move):
        if len(move) >= 3:  # Check if move have a negative number
            self.bot.answer_callback_query(text="Questa colonna è completamente occupata", show_alert=True)
            return
        if self.key == "red":
            self.red.append(move)
            self.buttons[self.buttons.index(move)] = move[0] + str(int(move[1]) - 1)
            self.markup = self.create_markup(self.key, self.buttons)
            img = self.board_img()
            with open(img, "rb") as pic:
                pic = self.bot.send_photo(self.STORAGE, pic)
                self.bot.edit_message_media(self.id_group, self.id_message, media=InputMediaPhoto(pic.photo.file_id),
                                            reply_markup=self.markup)

            a = self.take_best_move(self.parse_board())

            self.yellow.append(a)
            self.buttons[self.buttons.index(a)] = a[0] + str(int(a[1]) - 1)
            self.markup = self.create_markup(self.key, self.buttons)
            img = self.board_img()
            with open(img, "rb") as pic:
                pic = self.bot.send_photo(self.STORAGE, pic)
                self.bot.edit_message_media(self.id_group, self.id_message, media=InputMediaPhoto(pic.photo.file_id),
                                            reply_markup=self.markup)

        x = self.check_win(self.parse_board(), 0)
        if x != -100:
            if x == 10:
                self.bot.edit_message_text(self.id_group, self.id_message, "ROSSO HA VINTO")
            elif x == -10:
                self.bot.edit_message_text(self.id_group, self.id_message, "GIALLO")
            elif x == 0:
                self.bot.edit_message_text(self.id_group, self.id_message, "PAREGGIO")
            Connect4.all_games.pop((self.id_group, self.id_message))

    def take_best_move(self, board, max_deep=6):
        moves = {}
        for i in range(7):
            _ = self.index_fp(board, i)
            if _ != -1:
                moves[(i, _)] = 0
        print(moves)
        for move in moves.keys():
            board[move[0]][move[1]] = 1 if self.ai == "red" else 2
            moves[move] = self.mini_max(board, False, 0, -10000, 10000,
                                        max_deep) if self.ai == "red" else self.mini_max(board, True, 0, -10000, 1000,
                                                                                         max_deep)
            board[move[0]][move[1]] = 0
        print(moves)

        k = 10000 if self.ai == "yellow" else -1000
        t = []
        for _ in moves.keys():
            if moves[_] < k and self.ai == "yellow":
                k = moves[_]

            if moves[_] > k and self.ai == "red":
                k = moves[_]

        for _ in moves.keys():
            if moves[_] == k: t.append(_)

        e_move = random.choice(t)
        return [
            ['A0', 'A1', 'A2', 'A3', 'A4', 'A5'],
            ['B0', 'B1', 'B2', 'B3', 'B4', 'B5'],
            ['C0', 'C1', 'C2', 'C3', 'C4', 'C5'],
            ['D0', 'D1', 'D2', 'D3', 'D4', 'D5'],
            ['E0', 'E1', 'E2', 'E3', 'E4', 'E5'],
            ['F0', 'F1', 'F2', 'F3', 'F4', 'F5'],
            ['G0', 'G1', 'G2', 'G3', 'G4', 'G5']
        ][e_move[0]][e_move[1]]

    def check_win(self, board, deep):
        for i in range(7):
            for j in range(6):
                if j + 3 < 6:
                    C1 = (board[i][j] == 1 and board[i][j + 1] == 1 and board[i][j + 2] == 1 and board[i][j + 3] == 1)
                    C2 = (board[i][j] == 2 and board[i][j + 1] == 2 and board[i][j + 2] == 2 and board[i][j + 3] == 2)
                    if C1:
                        return 10 - deep
                    elif C2:
                        return -10 + deep
                if i + 3 < 7:
                    C1 = (board[i][j] == 1 and board[i + 1][j] == 1 and board[i + 2][j] == 1 and board[i + 3][j] == 1)
                    C2 = (board[i][j] == 2 and board[i + 1][j] == 2 and board[i + 2][j] == 2 and board[i + 3][j] == 2)
                    if C1:
                        return 10 - deep
                    elif C2:
                        return -10 + deep
                if i + 3 < 7 and j + 3 < 6:
                    C1 = (board[i][j] == 1 and board[i + 1][j + 1] == 1 and board[i + 2][j + 2] == 1 and board[i + 3][
                        j + 3] == 1)
                    C2 = (board[i][j] == 2 and board[i + 1][j + 1] == 2 and board[i + 2][j + 2] == 2 and board[i + 3][
                        j + 3] == 2)
                    if C1:
                        return 10 - deep
                    elif C2:
                        return -10 + deep

                if i - 3 >= 0 and j - 3 >= 0:
                    C1 = (board[i][j] == 1 and board[i - 1][j - 1] == 1 and board[i - 2][j - 2] == 1 and board[i - 3][
                        j - 3] == 1)
                    C2 = (board[i][j] == 2 and board[i - 1][j - 1] == 2 and board[i - 2][j - 2] == 2 and board[i - 3][
                        j - 3] == 2)
                    if C1:
                        return 10 - deep
                    elif C2:
                        return -10 + deep

                if i - 3 >= 0 and j + 3 < 6:
                    C1 = (board[i][j] == 1 and board[i - 1][j + 1] == 1 and board[i - 2][j + 2] == 1 and board[i - 3][
                        j + 3] == 1)
                    C2 = (board[i][j] == 2 and board[i - 1][j + 1] == 2 and board[i - 2][j + 2] == 2 and board[i - 3][
                        j + 3] == 2)
                    if C1:
                        return 10 - deep
                    elif C2:
                        return -10 + deep

                if i + 3 < 7 and j - 3 >= 0:
                    C1 = (board[i][j] == 1 and board[i + 1][j - 1] == 1 and board[i + 2][j - 2] == 1 and board[i + 3][
                        j - 3] == 1)
                    C2 = (board[i][j] == 2 and board[i + 1][j - 1] == 2 and board[i + 2][j - 2] == 2 and board[i + 3][
                        j - 3] == 2)
                    if C1:
                        return 10 - deep
                    elif C2:
                        return -10 + deep

        draw = True
        for i in range(7):
            for j in range(6):
                if board[i][j] == 0:
                    draw = False
                    break

        if draw: return 0

        return -100

    def mini_max(self, board, is_max, deep, alfa, beta, max_deep) -> int:
        c = self.check_win(board, deep)
        if deep == max_deep: return 0
        if c != -100: return c
        if is_max:
            x = -10000
            for i in range(7):
                _ = self.index_fp(board, i)
                if _ == -1: continue
                board[i][_] = 1
                x = max(self.mini_max(board, not is_max, deep + 1, alfa, beta, max_deep), x)
                alfa = max(alfa, x)
                board[i][_] = 0
                if beta <= alfa: break

        else:
            x = 10000
            for i in range(7):
                _ = self.index_fp(board, i)
                if _ == -1: continue
                board[i][_] = 2
                x = min(self.mini_max(board, not is_max, deep + 1, alfa, beta, max_deep), x)
                beta = min(beta, x)
                board[i][_] = 0
                if beta <= alfa: break

        return x

    def index_fp(self, board, col):
        i = 5
        while board[col][i] != 0:
            i -= 1
            if i == -1: return -1

        return i

    def create_markup(self, key, buttons: list):
        markup = []
        for pos in buttons:
            markup.append(InlineKeyboardButton(text=key, callback_data=pos))

        return InlineKeyboardMarkup([markup])

    def board_img(self):
        __str = "ABCDEFG"
        tiles = {}
        h = self.pa_2
        for i in range(6):
            n = self.pa_1
            for j in range(7):
                tiles[__str[j] + str(i)] = (n, h)
                n += self.d

            h += self.d

        games = self.board.copy()

        for _ in self.red:
            games.paste(self.p1, tiles[_])
        for _ in self.yellow:
            games.paste(self.p2, tiles[_])

        games.save(f"assests/{str(self.id_group) + str(self.id_message)}.jpg")
        return f"assests/{str(self.id_group) + str(self.id_message)}.jpg"

    def parse_board(self) -> list:
        l = [
            ['A0', 'A1', 'A2', 'A3', 'A4', 'A5'],
            ['B0', 'B1', 'B2', 'B3', 'B4', 'B5'],
            ['C0', 'C1', 'C2', 'C3', 'C4', 'C5'],
            ['D0', 'D1', 'D2', 'D3', 'D4', 'D5'],
            ['E0', 'E1', 'E2', 'E3', 'E4', 'E5'],
            ['F0', 'F1', 'F2', 'F3', 'F4', 'F5'],
            ['G0', 'G1', 'G2', 'G3', 'G4', 'G5']
        ]

        for __ in l:
            for _ in __:
                if _ in self.red:
                    l[l.index(__)][__.index(_)] = 1
                elif _ in self.yellow:
                    l[l.index(__)][__.index(_)] = 2
                else:
                    l[l.index(__)][__.index(_)] = 0

        return l
