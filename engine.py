import pygame 
from dataclasses import dataclass
from typing import Callable, TypeAlias
import sys, os
from players import Player
import frontend.palette as palette
from frontend.renderer import Renderer
from models import GameState, Grid, Stone

ErrorHandler: TypeAlias = Callable[[Exception], None]

pygame.init()

@dataclass(frozen=True)
class Gomoku:
    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None
    
    def play(self) -> None:
        screen_size = (900, 720)
        screen = pygame.display.set_mode(screen_size)
        
        screen.fill(palette.BOARD_COLOR)
        Renderer.draw_board(screen, 15, 45)
        game_state = GameState(Grid(15, 45))
        renderer = Renderer()
        
        player1_score = 0
        player2_score = 0
        renderer.draw_score(player1_score, player2_score, screen)
        start_time = 0
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            start_time = pygame.time.get_ticks()
            renderer.display_time(400, 400, 10, start_time, screen)
            game_state = player.make_move(game_state)
            self.renderer.draw_score(player1_score, player2_score, screen, game_state.current_stone.value)
            renderer.draw_grid(screen=screen, grid=game_state.grid, cell_size=45)   
            
    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_stone is Stone.BLACK:
            return self.player1
        else:
            return self.player2 
        
    def display_time(self, start_time, duration, screen):
        current_time = pygame.time.get_ticks() - start_time
        remaining_time = duration - current_time
        if remaining_time <= 0:
            remaining_time = 0
            
        seconds = int(current_time / 1000)
        minutes = int(seconds / 60)
        seconds = seconds % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        time_surf = pygame.font.Font(None, 30).render(time_string, True, palette.BLACK)
        time_rect = time_surf.get_rect(center=(400, 400))
        screen.blit(time_surf, time_rect)