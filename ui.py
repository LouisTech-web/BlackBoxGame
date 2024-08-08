import tkinter as tk
from tkinter import messagebox

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        # Créer le plateau de jeu
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        self.cells = {}
        for i in range(self.game.n + 2):
            for j in range(self.game.n + 2):
                if i == 0 or i == self.game.n + 1 or j == 0 or j == self.game.n + 1:
                    if i == 0:
                        cell = tk.Button(self.board_frame, text="↓", width=4, height=2,
                                        command=lambda i=i, j=j: self.on_laser_click((i-1, j-1), (1, 0)))
                    elif i == self.game.n + 1:
                        cell = tk.Button(self.board_frame, text="↑", width=4, height=2,
                                        command=lambda i=i, j=j: self.on_laser_click((i-1, j-1), (-1, 0)))
                    elif j == 0:
                        cell = tk.Button(self.board_frame, text="→", width=4, height=2,
                                        command=lambda i=i, j=j: self.on_laser_click((i-1, j-1), (0, 1)))
                    elif j == self.game.n + 1:
                        cell = tk.Button(self.board_frame, text="←", width=4, height=2,
                                        command=lambda i=i, j=j: self.on_laser_click((i-1, j-1), (0, -1)))
                else:
                    cell = tk.Button(self.board_frame, width=4, height=2,
                                    command=lambda i=i-1, j=j-1: self.on_cell_click(i-1, j-1))
                cell.grid(row=i, column=j)
                if 0 < i < self.game.n + 1 and 0 < j < self.game.n + 1:
                    self.cells[(i-2, j-2)] = cell

        # Boutons de contrôle
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, padx=10, pady=10)

        self.reset_button = tk.Button(self.control_frame, text="Recommencer", command=self.reset_game)
        self.reset_button.grid(row=0, column=0, padx=5, pady=5)

        # Scores et Round
        self.score_label = tk.Label(self.control_frame, text="Scores: Joueur 1: 0 | Joueur 2: 0")
        self.score_label.grid(row=1, column=0, columnspan=2)
        
        self.round_label = tk.Label(self.control_frame, text=f"Round: 1/5")
        self.round_label.grid(row=2, column=0, columnspan=2)

        # Mise à jour initiale des scores
        self.update_score_label()

    def update_board(self):
        # Mise à jour de l'affichage du plateau
        for (i, j) in self.cells:
            self.cells[(i, j)].config(text='', bg='SystemButtonFace')

    def on_cell_click(self, i, j):
        if self.game.game_status == "placement" and self.game.current_player == 1:
            self.game.place_ball(i, j)
            self.cells[(i, j)].config(text='B', bg='red')
            if len(self.game.ball_positions) == self.game.p:
                messagebox.showinfo("Placement Complete", "Le joueur 1 a placé tous les atomes. C'est maintenant au Joueur 2 de trouver les atomes.")
                self.game.game_status = "recherche"
                self.game.current_player = 2
        elif self.game.game_status == "recherche" and self.game.current_player == 2:
            self.game.make_guess(i, j)
            self.cells[(i, j)].config(text='?', bg='yellow')
            if len(self.game.guesses) == self.game.p:
                if self.game.check_guesses():
                    messagebox.showinfo("Victoire", "Bravo Joueur 2! C'est maintenant le nouveau round.")
                    self.update_score_label()
                    self.next_round()
                else:
                    messagebox.showinfo("Réessaie !", "Tu n'as pas trouvé les atomes. Réessaie.")
                    self.game.guesses = []
                    self.update_board()

    def on_laser_click(self, start_pos, direction):
        if self.game.current_player == 2:
            start_pos = (start_pos[0], start_pos[1])
            direction = (direction[0], direction[1])

            path, result_type = self.game.check_ray(start_pos, direction)

            for pos in path:
                if pos in self.cells:
                    self.cells[pos].config(bg='blue')

            if result_type == "Hit":
                messagebox.showinfo("Touché", "Le laser a touché un atome!")
            elif result_type == "Miss":
                messagebox.showinfo("Manqué", "Le laser a manqué les atomes.")

    def reset_game(self):
        self.game.reset_game()
        self.update_board()
        self.update_score_label()

    def next_round(self):
        if not self.game.is_game_over():
            self.game.reset_game()
            self.update_board()
            self.round_label.config(text=f"Round: {self.game.current_match + 1}/5")
        else:
            print("All rounds completed. Calling end_game.")  # Debugging line
            self.end_game()

    def update_score_label(self):
        total_score_1 = sum(self.game.scores[0])
        total_score_2 = sum(self.game.scores[1])
        self.score_label.config(text=f"Scores: Joueur 1: {total_score_1} | Joueur 2: {total_score_2}")

    def end_game(self):
        total_score_1 = sum(self.game.scores[0])
        total_score_2 = sum(self.game.scores[1])
        
        if total_score_1 > total_score_2:
            winner = "Joueur 1"
        elif total_score_1 < total_score_2:
            winner = "Joueur 2"
        else:
            winner = "Aucun, c'est une égalité !"

        messagebox.showinfo("Fin de Partie", f"Partie terminée ! {winner} a gagné avec un score de {total_score_1} à {total_score_2}.")
