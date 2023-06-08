from models import GameState, Stone, Move, Grid
import abc
from exceptions import InvalidMove
import time, sys, os
import pygame
from frontend.button import Button
from frontend.renderer import Renderer
import frontend.palette as palette
import numpy as np
import cv2

class Player(metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int) -> None:
        self.stone = stone
        self.time_per_turn = time_per_turn
        self.minutes_per_player = minutes_per_player
        
def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
def board_to_index(index: tuple):
    x, y = index
    
    x = x if x >= 45 else 45
    x = x if x <= 675 else 675
    y = y if y >= 45 else 45
    y = y if y <= 675 else 675
    
    if x % 45 > 23:
        x = (x - x%45) + 45
    else:
        x = x - x%45

    if y % 45 > 23:
        y = (y - y%45) + 45
    else:
        y = y - y%45
    
    x /= 45
    y /= 45
    x = x if x >= 0 else 0
    y = y if y >= 0 else 0

    return int(x) - 1, int(y) - 1

def display_total_time(screen, total_time, curr_stone):
    if total_time < 0:
        total_time = 0
    minutes = total_time // 60
    seconds = total_time % 60
    if minutes > 99:
        minutes = 99
        seconds = 59
    time_string = f"{minutes:02d}:{seconds:02d}"
    time_surf = pygame.font.Font(None, 30).render(time_string, True, palette.BLACK)
    if curr_stone == 1:
        time_rect = time_surf.get_rect(center=(45*15 + 113, 45*5))
    else:
        time_rect = time_surf.get_rect(center=(45*15 + 113, 45*11 + 10))

    screen.blit(time_surf, time_rect)

def drawArcCv2(surf, color, center, radius, width, start_angle, end_angle):
    circle_image = np.zeros((radius * 2 + 4, radius * 2 + 4, 4), dtype=np.uint8)
    circle_image = cv2.ellipse(circle_image, (radius + 2, radius + 2),
                               (radius - width // 2, radius - width // 2), 0, start_angle, end_angle,
                               (*color, 255), width, lineType=cv2.LINE_AA)
    circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius * 2 + 4, radius * 2 + 4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center=center),
              special_flags=pygame.BLEND_PREMULTIPLIED)
    

def pvp(time_per_turn, minutes_per_player):
    print(time_per_turn, minutes_per_player)
    pygame.init()
    screen_size = (900, 720)
    screen = pygame.display.set_mode(screen_size)
    game_state = GameState(Grid(15, 45))
    
    def init_drawing():
        screen.fill(palette.BOARD_COLOR)
        renderer.draw_board(screen, 15, 45)
        renderer.draw_score(score[0], score[1], screen, game_state.current_stone.value)
    
    stop = False
    start_time = 0
    start_angle = 270
    
    # time per turn
    clock = pygame.time.Clock()
    counter = time_per_turn
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    
    # player initialization
    player = game_state.current_stone
    score = [0, 0]
    gameplay_font = pygame.font.Font(None, 40)
    p1_total_time = minutes_per_player * 60
    p2_total_time = minutes_per_player * 60
    counter = time_per_turn
    
    renderer = Renderer()
    
    init_drawing()
    count = 0
    p1_area = pygame.Rect(45*15 + 55, 45*4 - 13, 100, 100)
    p2_area = pygame.Rect(45*15 + 55, 45*10 + 10, 100, 100)

    display_total_time(screen, p1_total_time, game_state.current_stone.value)
    display_total_time(screen, p1_total_time, game_state.current_stone.other.value)
    while True:
        clock.tick(60)
        winner = game_state.winner
        game_mouse_pos = pygame.mouse.get_pos()
        
        pygame.display.update()
        new_game_button = Button(image=None, pos=(45*15 + 113, 45 + 15), text_input="NEW GAME", 
                                    font=gameplay_font, base_color=palette.BOARD_COLOR, hovering_color=palette.WHITE)
        continue_button = Button(image=None, pos=(45*15 + 113, 45*3), text_input="CONTINUE",
                                    font=gameplay_font, base_color=palette.BOARD_COLOR, hovering_color=palette.WHITE)
        
        for button in [new_game_button, continue_button]:
            button.changeColor(game_mouse_pos)
            button.update(screen)  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         MainMenu.main_menu()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # new game
                if new_game_button.checkForInput(game_mouse_pos):
                    score = [0, 0]
                    p1_total_time = minutes_per_player * 60
                    p2_total_time = minutes_per_player * 60
                    counter = time_per_turn
                    
                    start_time = pygame.time.get_ticks()
                    stop = False
                    game_state = GameState(Grid(15, 45))
                    init_drawing()
                    display_total_time(screen, p1_total_time, game_state.current_stone.value)
                    display_total_time(screen, p1_total_time, game_state.current_stone.other.value)
                    continue
                
                # continue
                elif continue_button.checkForInput(game_mouse_pos) and stop is True:
                    p1_total_time = minutes_per_player * 60
                    p2_total_time = minutes_per_player * 60
                    counter = time_per_turn
                    
                    stop = False
                    start_time = pygame.time.get_ticks()
                    game_state = GameState(Grid(15, 45))
                    init_drawing()
                    display_total_time(screen, p1_total_time, game_state.current_stone.value)
                    display_total_time(screen, p1_total_time, game_state.current_stone.other.value)
                    continue
            
            # timing
            elif event.type == timer_event and not stop:
                counter -= 1
                end_angle = 270 - (360 * counter / time_per_turn)
                if game_state.current_stone == Stone.BLACK:
                    p1_total_time -= 1
                    screen.fill(palette.BOARD_COLOR, p1_area)
                    display_total_time(screen, p1_total_time, game_state.current_stone.value)
                    drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*5), 40, 5, start_angle, end_angle) 
                    if p1_total_time <= 0 or counter <= 0:
                        winner = Stone.WHITE
                        stop = True
                    
                else:
                    p2_total_time -= 1
                    screen.fill(palette.BOARD_COLOR, p2_area)
                    display_total_time(screen, p2_total_time, game_state.current_stone.value)
                    drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*11 + 10), 40, 5, start_angle, end_angle)
                    if p2_total_time <= 0 or counter <= 0:
                        winner = Stone.BLACK
                        stop = True
                    
            if winner is None and not stop:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if not new_game_button.checkForInput(game_mouse_pos):
                            if not continue_button.checkForInput(game_mouse_pos):
                                if game_state.current_stone == Stone.BLACK:
                                    start_time = pygame.time.get_ticks()
                                index = board_to_index(pygame.mouse.get_pos())
                                move = game_state.make_move_to(x=index[1], y=index[0])
                                
                                if move is None:
                                    continue
                                counter = time_per_turn
                                game_state = move.after_state
                                renderer.draw_grid(screen, game_state.grid, cell_size=45)
            
            if winner is not None:
                score[winner.value - 1] += 1
                screen.fill(palette.BOARD_COLOR)
                renderer.draw_board(screen, 15, 45)
                renderer.draw_grid(screen, game_state.grid, cell_size=45)
                display_total_time(screen, p1_total_time, game_state.current_stone.value)
                display_total_time(screen, p1_total_time, game_state.current_stone.other.value)
                game_state = GameState(Grid(15, 45))
                winner = game_state.winner # None
                # renderer.draw_score(score[0], score[1], screen, game_state.current_stone.value)
                stop = True
        renderer.draw_score(score[0], score[1], screen, game_state.current_stone.value)
 
