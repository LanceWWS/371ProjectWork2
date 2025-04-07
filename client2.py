import pygame
from network import network  # your class
import pickle

WIDTH = 640
ROWS = 8
SQ_SIZE = WIDTH // ROWS

pygame.init()
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Multiplayer Grid Claim")

colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

def draw_grid(win, grid):
    win.fill((255, 255, 255))
    for y in range(ROWS):
        for x in range(ROWS):
            rect = pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(win, (200, 200, 200), rect, 1)
            if grid[y][x] != -1:
                pygame.draw.rect(win, colors[grid[y][x] % len(colors)], rect.inflate(-8, -8))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = network()
    print("player get", n.getP())  # player ID
    p = int(n.getP())  # player ID

    while run:
        clock.tick(30)
        try:
            game = n.send("get")  # get game state
        except:
            print("Couldn't get game state")
            break

        if game:
            draw_grid(win, game.grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // SQ_SIZE, pos[1] // SQ_SIZE
                move_str = f"{x},{y}"
                try:
                    game = n.send(move_str)
                except:
                    print("Failed to send move")

    pygame.quit()

main()
