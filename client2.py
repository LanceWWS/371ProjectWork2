import pygame
from network import network  # your network class
import pickle

WIDTH = 640
ROWS = 8
SQ_SIZE = WIDTH // ROWS

pygame.init()
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Multiplayer Grid Claim")
font = pygame.font.SysFont("comicsans", 40)
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

def draw_grid(win, grid):
    win.fill((255, 255, 255))
    for y in range(ROWS):
        for x in range(ROWS):
            rect = pygame.Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(win, (200, 200, 200), rect, 1)
           
            cell = grid[y][x]
            # If a square is claimed, fill it with the owner's color.
            if cell['owner'] is not None:
                pygame.draw.rect(win, colors[cell['owner'] % len(colors)], rect.inflate(-8, -8))
            else:
                # Optionally, you could visualize partial painting here.
                # For simplicity, we're not drawing partial paint.
                pass
    pygame.display.update()

def display_winner(win, winner):
    win.fill((255, 255, 255))
    if isinstance(winner, list):
        win_text = "Winner(s): " + ", ".join(f"Player {w}" for w in winner)
    else:
        win_text = f"Winner: Player {winner}"
    text = font.render(win_text, True, (0, 0, 0))
    # Center the text
    text_rect = text.get_rect(center=(WIDTH // 2, WIDTH // 2))
    win.blit(text, text_rect)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    
    try:
        n = network()
        p = int(n.getP())  # player ID
        print("You are player", p)
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        pygame.quit()
        return
        
    game_over_displayed = False
    connection_lost = False
    
    while run:
        clock.tick(30)
        
        if not connection_lost:
            try:
                game = n.send("get")  # get game state
                if game:
                    draw_grid(win, game.grid)
                    # Check if the game is finished
                    if game.finished:
                        winner = game.get_winner()
                        display_winner(win, winner)
                        game_over_displayed = True
            except Exception as e:
                print(f"Connection error: {e}")
                connection_lost = True
                # Display connection lost message
                win.fill((255, 255, 255))
                text = font.render("Connection to server lost", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, WIDTH // 2))
                win.blit(text, text_rect)
                pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Only allow moves if the game isn't finished and connection is active
            if not game_over_displayed and not connection_lost and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0] // SQ_SIZE
                y = pos[1] // SQ_SIZE
                move = f"{x},{y}"
                print(f"Sending move: {move}")
                try:
                    game = n.send(move)
                except Exception as e:
                    print(f"Error sending move: {e}")
                    connection_lost = True
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()