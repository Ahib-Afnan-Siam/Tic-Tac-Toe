import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.player_mode = 'HUMAN'  # 'HUMAN' or 'AI'
        self.create_board()

    def create_board(self):
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text='', font=('Arial', 20), width=6, height=2,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

        self.mode_label = tk.Label(self.master, text="Mode: Human vs Human", font=('Arial', 14))
        self.mode_label.grid(row=3, columnspan=3, pady=10)

    def make_move(self, row, col):
        index = 3 * row + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.show_winner_message(f"Player {self.current_player} wins!")
                self.reset_board()
            elif ' ' not in self.board:
                self.show_winner_message("It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.player_mode == 'AI' and self.current_player == 'O':
                    self.ai_move()

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        self.make_move(best_move // 3, best_move % 3)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == player:
                return True
        return False

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.config(text='')
        self.current_player = 'X'

    def show_winner_message(self, message):
        messagebox.showinfo("Tic Tac Toe", message)

    def change_mode(self):
        if self.player_mode == 'HUMAN':
            self.player_mode = 'AI'
            self.mode_label.config(text="Mode: Human vs AI")
        else:
            self.player_mode = 'HUMAN'
            self.mode_label.config(text="Mode: Human vs Human")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)

    mode_button = tk.Button(root, text="Toggle Mode", font=('Arial', 12), command=game.change_mode)
    mode_button.grid(row=4, columnspan=3, pady=10)

    root.mainloop