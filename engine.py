from dataclasses import dataclass
from typing import Callable, TypeAlias

from players import Player
from models import GameState, Stone, Grid
from frontend.renderer import Renderer
from exceptions import InvalidMove
import pygame, sys, cv2 
import numpy as np

ErrorHandler: TypeAlias = Callable[[Exception], None]

pygame.init()

@dataclass(frozen=True)
class Gomoku:
    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None
    
    def __post_init__(self) -> None:
        pass
    
    def check_quit(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def play(self, game_state: GameState, screen, board_size=15, cell_size=45) -> None:
        if not game_state.game_over:
            player = self.get_current_player(game_state)
            game_state = player.make_move(game_state=game_state)
            self.renderer.draw_grid(screen, game_state.grid, cell_size)
        return game_state
    
    # def play(self, screen, board_size=15, cell_size=45) -> None:
    #     game_state = GameState(Grid(board_size, cell_size))
    #     while True:
    #         self.check_quit()
    #         while not game_state.game_over:
    #             self.check_quit()

    #             player = self.get_current_player(game_state)
    #             if not game_state.game_over:
    #                 while not player.make_move(game_state=game_state) and not game_state.game_over:
    #                     self.draw_timer(screen, 0, 30)
    #                     game_state = player.make_move(game_state=game_state)
    #                 self.renderer.draw_grid(screen, game_state.grid, cell_size)

                        
    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_stone is Stone.BLACK:
            return self.player1
        else:
            return self.player2

    def drawArcCv2(self, surf, color, center, radius, width, start_angle, end_angle):
        circle_image = np.zeros((radius * 2 + 4, radius * 2 + 4, 4), dtype=np.uint8)
        circle_image = cv2.ellipse(circle_image, (radius + 2, radius + 2),
                                   (radius - width // 2, radius - width // 2), 0, start_angle, end_angle,
                                   (*color, 255), width, lineType=cv2.LINE_AA)
        circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius * 2 + 4, radius * 2 + 4), 'RGBA')
        surf.blit(circle_surface, circle_surface.get_rect(center=center),
                  special_flags=pygame.BLEND_PREMULTIPLIED)
        
    def draw_timer(self, screen, minutes, seconds, x_pos=788, y_pos=100):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 50)
        total_time = minutes * 60 + seconds
        counter = total_time
        text = font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 128, 0))
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)
        
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == timer_event:
                counter -= 1
                minutes = counter // 60
                seconds = counter % 60
                text = font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 128, 0))
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)
                    
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        start_angle = 270  # Starting angle (bottom position)
        end_angle = 270 - (360 * counter / total_time)  # Ending angle based on the remaining time
        self.drawArcCv2(screen, (255, 0, 0), (788, 100), 90, 10, start_angle, end_angle)
        pygame.display.flip()