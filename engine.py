from player import Player
import pygame, sys
import frontend.palette as palette
from frontend.renderer import Renderer
from frontend.button import Button
from dataclasses import dataclass
from models import GameState, Stone, Move, Grid


@dataclass(frozen=True)
class Gomoku:
    player1: Player
    player2: Player
    renderer: Renderer
    
    def play(self) -> None:
        print(self.player1.time_per_turn, self.player1.minutes_per_player)
        pygame.init()
        screen_size = (900, 720)
        screen = pygame.display.set_mode(screen_size)
        game_state = GameState(Grid(15, 45))
        is_paused = False

        def init_drawing():
            screen.fill(palette.BOARD_COLOR)
            self.renderer.draw_board(screen, 15, 45)
            self.renderer.draw_score(score[0], score[1], screen, player.stone.value)

        stop = False
        start_angle = 270

        # time per turn
        clock = pygame.time.Clock()
        counter = self.player1.time_per_turn
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)

        # player initialization
        player = self.get_current_player(game_state)
        score = [0, 0]
        gameplay_font = pygame.font.Font(None, 40)
        p1_total_time = self.player1.minutes_per_player * 60
        p2_total_time = self.player2.minutes_per_player * 60


        init_drawing()
        count = 0
        p1_area = pygame.Rect(45*15 + 55, 45*4 - 13, 100, 100)
        p2_area = pygame.Rect(45*15 + 55, 45*10 + 10, 100, 100)

        self.renderer.display_total_time(screen, p1_total_time, player.stone.value)
        self.renderer.display_total_time(screen, p1_total_time, player.stone.other.value)
        while True:
            clock.tick(60)
            winner = game_state.winner
            game_mouse_pos = pygame.mouse.get_pos()
            player = self.get_current_player(game_state)

            pygame.display.update()
            
            new_game_button = Button(image=None, pos=(45*15 + 113, 45 + 15), text_input="NEW GAME", 
                                        font=gameplay_font, base_color=palette.BLACK, hovering_color=palette.WHITE)
            continue_button = Button(image=None, pos=(45*15 + 113, 45*3), text_input="CONTINUE",
                                        font=gameplay_font, base_color=palette.BLACK, hovering_color=palette.WHITE)

            # check if mouse is hovering over button
            for button in [new_game_button, continue_button]:
                button.changeColor(game_mouse_pos)
                button.update(screen)  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        is_paused = not is_paused
                
                    while is_paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    is_paused = not is_paused

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # new game
                    if new_game_button.checkForInput(game_mouse_pos):
                        score = [0, 0]
                        p1_total_time = self.player1.minutes_per_player * 60
                        p2_total_time = self.player2.minutes_per_player * 60
                        counter = self.player1.time_per_turn

                        stop = False
                        game_state = GameState(Grid(15, 45))
                        init_drawing()
                        
                        self.renderer.display_total_time(screen, p1_total_time, player.stone.value)
                        self.renderer.display_total_time(screen, p1_total_time, player.stone.other.value)
                        continue
                    
                    # continue
                    elif continue_button.checkForInput(game_mouse_pos) and stop is True:
                        p1_total_time = self.player1.minutes_per_player * 60
                        p2_total_time = self.player2.minutes_per_player * 60
                        counter = self.player1.time_per_turn

                        stop = False
                        game_state = GameState(Grid(15, 45))
                        init_drawing()
                        self.renderer.display_total_time(screen, p1_total_time, player.stone.value)
                        self.renderer.display_total_time(screen, p1_total_time, player.stone.other.value)
                        continue
                    
                # timing
                elif event.type == timer_event and not stop:
                    counter -= 1
                    end_angle = 270 - (360 * counter / self.player1.time_per_turn)
                    if game_state.current_stone == Stone.BLACK:
                        p1_total_time -= 1
                        screen.fill(palette.BOARD_COLOR, p1_area)
                        self.renderer.display_total_time(screen, p1_total_time, player.stone.value)
                        self.renderer.drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*5), 40, 5, start_angle, end_angle) 
                        if p1_total_time <= 0 or counter <= 0:
                            winner = Stone.WHITE
                            stop = True

                    else:
                        p2_total_time -= 1
                        screen.fill(palette.BOARD_COLOR, p2_area)
                        self.renderer.display_total_time(screen, p2_total_time, player.stone.value)
                        self.renderer.drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*11 + 10), 40, 5, start_angle, end_angle)
                        if p2_total_time <= 0 or counter <= 0:
                            winner = Stone.BLACK
                            stop = True

                # making a move
                if winner is None and not stop:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            if not new_game_button.checkForInput(game_mouse_pos):
                                if not continue_button.checkForInput(game_mouse_pos):
                                    move = player.make_move(game_state)

                                    if move is None:
                                        continue
                                    counter = self.player1.time_per_turn
                                    game_state = move
                                    self.renderer.draw_grid(screen, game_state.grid, cell_size=45)

                # check for winner
                if winner is not None:
                    score[winner.value - 1] += 1
                    
                    screen.fill(palette.BOARD_COLOR)
                    self.renderer.draw_board(screen, 15, 45)
                    self.renderer.draw_grid(screen, game_state.grid, cell_size=45)
                    self.renderer.display_total_time(screen, p1_total_time, player.stone.value)
                    self.renderer.display_total_time(screen, p1_total_time, player.stone.other.value)
                    game_state = GameState(Grid(15, 45))
                    winner = game_state.winner # None
                    stop = True
            self.renderer.draw_score(score[0], score[1], screen, player.stone.value)
            
    def get_current_player(self, game_state: GameState) -> Player:
        return self.player1 if game_state.current_stone == Stone.BLACK else self.player2