#game logic

class Game:
    def __init__(self, num_players):
        # Initialize the game with the number of players
        self.num_players = num_players
        self.grid = [[-1 for _ in range(8)] for _ in range(8)]  # 8x8 grid, -1 represents unclaimed squares
        self.turns = [0 for _ in range(num_players)]  # Track whether each player has made a move
        self.finished = False  # Flag to track if the game is finished
        self.current_turn = 0  # Which player's turn it is
        self.claimed_squares = [0 for _ in range(num_players)]  # Track how many squares each player has claimed
        self.ready = False  # Tracks if the game is ready to start (e.g., waiting for all players)

    def play(self, player_id, x, y):
        """Handle a move for a player (claim a grid square)."""
        if self.grid[y][x] == -1:  # If the cell is unclaimed
            self.grid[y][x] = player_id  # Mark the cell as owned by the player
            self.claimed_squares[player_id] += 1  # Increase the number of squares the player owns
            self.turns[player_id] = 1  # Mark that this player has made their move

            # Optional: Check if game is finished (i.e., all cells are filled)
            if all(cell != -1 for row in self.grid for cell in row):
                self.finished = True
                print("Game over! All squares are claimed.")
            else:
                self.next_turn()  # Move to the next player after a valid move
        else:
            print(f"Cell ({x},{y}) is already claimed!")

    def next_turn(self):
        """Move to the next player's turn."""
        self.current_turn = (self.current_turn + 1) % self.num_players  # Alternate between players
        print(f"Player {self.current_turn}'s turn!")

    def resetWent(self):
        """Reset the 'went' status for all players, for example, at the beginning of a new round."""
        self.turns = [0 for _ in range(self.num_players)]  # Reset everyone's turn status
        self.current_turn = 0  # Start with the first player
        print("Turns have been reset!")

    def get_winner(self):
        """Determine who has claimed the most squares and declare the winner."""
        if self.finished:
            max_claimed = max(self.claimed_squares)
            winner = self.claimed_squares.index(max_claimed)
            return winner
        else:
            return None  # Game is not finished yet

    def reset_game(self):
        """Reset the game to its initial state."""
        self.grid = [[-1 for _ in range(8)] for _ in range(8)]  # Reset the grid
        self.turns = [0 for _ in range(self.num_players)]  # Reset turn status
        self.claimed_squares = [0 for _ in range(self.num_players)]  # Reset claimed squares
        self.finished = False  # Reset the game finished flag
        self.current_turn = 0  # Start with the first player
        print("Game has been reset!")
