class Game:
    def __init__(self, n, p):
        self.n = n  # Taille du plateau
        self.p = p  # Nombre de balles à placer
        self.ball_positions = []
        self.guesses = []
        self.current_player = 1  # 1 = Placement, 2 = Recherche
        self.scores = [[0 for _ in range(5)] for _ in range(2)]  # Scores pour 2 joueurs sur 5 manches
        self.current_match = 0
        self.game_status = "placement"  # placement ou recherche
        self.hide_player = 1  # Le joueur qui cache les boules dans le round actuel

    def place_ball(self, x, y):
        if len(self.ball_positions) < self.p and self.current_player == self.hide_player:
            self.ball_positions.append((x, y))

    def make_guess(self, x, y):
        if len(self.guesses) < self.p and self.current_player != self.hide_player:
            self.guesses.append((x, y))

    def check_guesses(self):
        correct_guesses = set(self.guesses) & set(self.ball_positions)
        if len(correct_guesses) == self.p:
            self.scores[self.current_player - 1][self.current_match] = len(correct_guesses)  # Enregistre le score du joueur actuel
            return True
        return False

    def reset_game(self):
        self.ball_positions = []
        self.guesses = []
        self.current_player = 1
        self.game_status = "placement"
        self.hide_player = 1 if self.current_match % 2 == 0 else 2  # Alterner les joueurs qui cachent les boules
        self.current_match += 1

    def check_ray(self, start_pos, direction):
        from laser import check_ray_path
        path, result_type = check_ray_path(start_pos, direction, self.n, self.ball_positions)
        return path, result_type

    def is_game_over(self):
        return self.current_match >= 5
