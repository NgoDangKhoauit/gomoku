from frontend.renderer import Renderer 
from models import Stone, InvalidMove
from engine import Gomoku
from players import RandomComputerPlayer, Player, HumanPlayer
from typing import Callable, TypeAlias
import sys, os
import time, cv2
import numpy as np

import pygame
import math

from models import GameState, Grid, Stone
import frontend.palette as palette

# screen_size = (900, 720)
# screen = pygame.display.set_mode(screen_size)

# ErrorHandler: TypeAlias = Callable[[Exception], None]

# # def play(cell_size):
# #     game_state = GameState

# def get_current_player(game_state: GameState) -> Player:
#         if game_state.current_stone is Stone.BLACK:
#             return player1
#         else:
#             return player2

# grid = Grid(board_size=15, cell_size=45)
# game_state = GameState(grid)
# player1 = HumanPlayer(Stone.BLACK, 1, 1)
# player2 = HumanPlayer(Stone.WHITE, 1, 1)

# clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 50)
# minutes = 1
# seconds = 30
# total_time = minutes * 60 + seconds
# counter = total_time
# text = font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 128, 0))

# timer_event = pygame.USEREVENT + 1
# pygame.time.set_timer(timer_event, 1000)

# screen.fill(palette.BOARD_COLOR)
# Renderer.draw_board(screen, 15, 45)
# game_state = GameState(Grid(15, 45))
# renderer = Renderer()

# player1_score = 0
# player2_score = 0

# renderer.draw_score(player1_score, player2_score, screen)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()


#     if game_state.game_over:
#         pass
#     player = get_current_player(game_state)
    
#     game_state = player.make_move(game_state=game_state)
#     renderer.draw_score(player1_score, player2_score, screen, game_state.current_stone.value)
#     player1_score += 1
#     renderer.draw_grid(screen=screen, grid=game_state.grid, cell_size=45)

player1 = HumanPlayer(Stone.BLACK, 1, 1)
player2 = HumanPlayer(Stone.WHITE, 1, 1)
renderer = Renderer()

a = Gomoku(player1, player2, renderer)
a.play()