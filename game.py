#game logic

# game.py

class Game:
    def __init__(self, num_players):
        self.num_players = num_players  
        # Create an 8x8 grid.
        # Each cell is a dict with:
        #   - 'owner': None (if unclaimed) or the player id who claimed it.
        #   - 'paint': a dict mapping player ids to the amount of paint they've added.
        self.grid = [
            [
                {'owner': None, 'paint': {i: 0 for i in range(num_players)}}
                for _ in range(8)
            ]
            for _ in range(8)
        ]
        self.finished = False  # Set to True when all squares are claimed.
        self.claimed_squares = [0 for _ in range(num_players)]
        self.threshold = 50  # A square is claimed if a player's paint > 50 units.

    def play(self, player_id, x, y):
        """
        Process a move from player_id on square (x,y).
        Instead of instantly claiming the square, the player "paints" it.
        When a player's accumulated paint exceeds the threshold, the square is claimed.
        """
        # Check if coordinates are valid
        if not (0 <= x < 8 and 0 <= y < 8):
            print("Invalid coordinates.")
            return

        cell = self.grid[y][x]
        # If the square is already claimed, ignore further painting.
        if cell['owner'] is not None:
            print(f"Square ({x},{y}) is already claimed by player {cell['owner']}.")
            return

        # Add paint – here each move adds a fixed amount.
        paint_amount = 51
        cell['paint'][player_id] += paint_amount
        print(f"Player {player_id} painted square ({x},{y}). Total for player {player_id}: {cell['paint'][player_id]}")

        # Check if this player's paint now exceeds the threshold.
        if cell['paint'][player_id] > self.threshold:
            cell['owner'] = player_id
            self.claimed_squares[player_id] += 1
            print(f"Player {player_id} has claimed square ({x},{y})!")

        # Check if all squares are claimed.
        if all(cell['owner'] is not None for row in self.grid for cell in row):
            self.finished = True

    def resetWent(self):
        """
        In a painting game, resetting "went" status might not be as critical.
        If you want to allow rounds of painting without resetting the entire grid,
        you can implement logic here. For now, we’ll simply print a message.
        """
        print("Resetting turns is not required for the painting mechanic.")

    def get_winner(self):
        """
        Determine the winner when the game is finished.
        The winner is the player with the most claimed squares.
        Returns a list of winning player ids (in case of a tie).
        """
        if self.finished:
            max_claimed = max(self.claimed_squares)
            winners = [i for i, count in enumerate(self.claimed_squares) if count == max_claimed]
            return winners
        return None

    def reset_game(self):
        """
        Resets the entire game state, including the grid and claimed counts.
        """
        self.grid = [
            [
                {'owner': None, 'paint': {i: 0 for i in range(self.num_players)}}
                for _ in range(8)
            ]
            for _ in range(8)
        ]
        self.finished = False
        self.claimed_squares = [0 for _ in range(self.num_players)]
        print("Game has been reset!")
