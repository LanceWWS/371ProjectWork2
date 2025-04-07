#game logic

GRID_SIZE = 8
SQUARE_SIZE = 80

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.current_player = 0
        self.grid = [[{'owner': None, 'paint': {i: 0 for i in range(num_players)}} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def paint(self, x, y, player_id, amount=5):
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return
        cell = self.grid[y][x]
        if cell['owner'] is not None:
            return

        cell['paint'][player_id] += amount
        total = sum(cell['paint'].values())

        if total > (SQUARE_SIZE * SQUARE_SIZE) / 2:
            if cell['paint'][player_id] > total / 2:
                cell['owner'] = player_id
                self.current_player = (self.current_player + 1) % self.num_players

    def get_scores(self):
        scores = [0] * self.num_players
        for row in self.grid:
            for cell in row:
                if cell['owner'] is not None:
                    scores[cell['owner']] += 1
        return scores

    def is_game_over(self):
        total_claimed = sum(1 for row in self.grid for cell in row if cell['owner'] is not None)
        return total_claimed == GRID_SIZE * GRID_SIZE

    def get_winner(self):
        scores = self.get_scores()
        max_score = max(scores)
        return [i for i, s in enumerate(scores) if s == max_score]