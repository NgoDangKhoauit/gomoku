from game.player import Player, ComputerPlayer
import pygame, sys
import frontend.palette as palette
from frontend.renderer import Renderer
from frontend.button import Button
from dataclasses import dataclass
from game.models import GameState, Stone, Move, Grid


@dataclass(frozen=True)
class Gomoku:
    player1: Player
    player2: Player
    renderer: Renderer
    
    def play(self, place_sound, click_sound, win_sound) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        screen_size = (900, 720)
        screen = pygame.display.set_mode(screen_size)
        game_state = GameState(Grid(15, 45))
        is_paused = False
        prev_game_state = None

        def init_drawing():
            screen.fill(palette.BOARD_COLOR)
            self.renderer.draw_board(screen, 15, 45)
            self.renderer.draw_score(self.player1.score, self.player2.score, screen, player.stone.value)

        def reset_score():
            self.player1.score = 0
            self.player2.score = 0
            
        def reset_remaining_time():
            self.player1.remaining_time = self.player1.minutes_per_player * 60
            self.player2.remaining_time = self.player2.minutes_per_player * 60

        stop = False
        start_angle = 270

        # time per turn
        clock = pygame.time.Clock()
        counter = self.player1.time_per_turn
        timer_event = pygame.USEREVENT + 1
        # every 1 second
        pygame.time.set_timer(timer_event, 1000)
        bonus_time = 0

        # player initialization
        player = self.get_current_player(game_state)
        score = [0, 0]
        gameplay_font = pygame.font.Font(None, 40)
        self.player1.remaining_time = self.player1.minutes_per_player * 60
        self.player2.remaining_time = self.player2.minutes_per_player * 60

        init_drawing()
        p1_area = pygame.Rect(45*15 + 55, 45*4 - 13, 100, 100)
        p2_area = pygame.Rect(45*15 + 55, 45*10 + 10, 100, 100)

        self.renderer.display_total_time(screen, self.player1.remaining_time, player.stone.value)
        self.renderer.display_total_time(screen, self.player2.remaining_time, player.stone.other.value)
        while True:
            # limit to 60 fps
            clock.tick(60)
            
            winner = game_state.winner
            game_mouse_pos = pygame.mouse.get_pos()
            player = self.get_current_player(game_state)
            pygame.display.update()
            
            new_game_button = Button(image=None, pos=(45*15 + 113, 45 + 15), text_input="NEW GAME", 
                                        font=gameplay_font, base_color=palette.BLACK, hovering_color=palette.WHITE)
            continue_button = Button(image=None, pos=(45*15 + 113, 45*3), text_input="CONTINUE",
                                        font=gameplay_font, base_color=palette.BLACK, hovering_color=palette.WHITE)
            undo_button = Button(image=None, pos=(45*15 + 113, 45 *14), text_input="UNDO", 
                                        font=gameplay_font, base_color=palette.BOARD_COLOR, hovering_color=palette.WHITE)
            
            # check if mouse is hovering over button
            for button in [new_game_button, continue_button, undo_button]:
                button.changeColor(game_mouse_pos)
                button.update(screen)  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # button clicking
                elif event.type == pygame.KEYDOWN:
                    # click p to pause 
                    if event.key == pygame.K_p:
                        is_paused = not is_paused

                    # click esc to go back to main menu
                    if event.key == pygame.K_ESCAPE:
                        from main import main_menu
                        main_menu()

                # mouse clicking
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # new game
                    if new_game_button.checkForInput(game_mouse_pos):
                        click_sound.play()
                        reset_score()
                        reset_remaining_time()
                        counter = self.player1.time_per_turn

                        stop = False
                        game_state = GameState(Grid(15, 45))
                        init_drawing()
                        
                        self.renderer.display_total_time(screen, self.player1.remaining_time, player.stone.value)
                        self.renderer.display_total_time(screen, self.player2.remaining_time, player.stone.other.value)
                        continue
                    
                    # continue
                    elif continue_button.checkForInput(game_mouse_pos):
                        click_sound.play()
                        if stop is True:
                            reset_remaining_time()
                            counter = self.player1.time_per_turn

                            stop = False
                            game_state = GameState(Grid(15, 45))
                            init_drawing()
                            self.renderer.display_total_time(screen, self.player1.remaining_time, player.stone.value)
                            self.renderer.display_total_time(screen, self.player2.remaining_time, player.stone.other.value)
                            continue
                    
                    # undo
                    elif undo_button.checkForInput(game_mouse_pos) and not stop:
                        click_sound.play()
                        if game_state.game_not_started or winner is not None:
                            continue
                        game_state = prev_game_state
                        
                        if player is self.player1:
                            self.player1.remaining_time += bonus_time
                        else:
                            self.player2.remaining_time += bonus_time
                        
                        bonus_time = 0
                        init_drawing()
                        self.renderer.draw_grid(screen, game_state.grid, cell_size=45)
                        self.renderer.display_total_time(screen, self.player1.remaining_time, self.player1.stone.value)
                        self.renderer.display_total_time(screen, self.player2.remaining_time, self.player2.stone.value)
                        if not isinstance(self.player1, ComputerPlayer):
                            self.renderer.drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*5), 40, 5, start_angle, end_angle)
                        if not isinstance(self.player2, ComputerPlayer):
                            self.renderer.drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*11 + 10), 40, 5, start_angle, end_angle)
                    
                # timing
                elif event.type == timer_event and not stop and not is_paused:
                    counter -= 1
                    bonus_time += 1
                    end_angle = 270 - (360 * counter / self.player1.time_per_turn)
                    player.remaining_time -= 1
                    
                    if player is self.player1:
                        screen.fill(palette.BOARD_COLOR, p1_area)
                        if not isinstance(player, ComputerPlayer):
                            self.renderer.drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*5), 40, 5, start_angle, end_angle)
                    if player is self.player2:
                        screen.fill(palette.BOARD_COLOR, p2_area)
                        if not isinstance(player, ComputerPlayer):
                            self.renderer.drawArcCv2(screen, palette.BLACK, (45*15 + 113, 45*11 + 10), 40, 5, start_angle, end_angle)
                        
                    self.renderer.display_total_time(screen, player.remaining_time, player.stone.value)
                    
                    
                    if player.remaining_time <= 0 or counter <= 0:
                        winner = self.get_other_player(game_state).stone
                        stop = True

                # making a move
                if winner is None and not stop and not is_paused:
                    # player
                    if not isinstance(player, ComputerPlayer):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if not new_game_button.checkForInput(game_mouse_pos):
                                    if not undo_button.checkForInput(game_mouse_pos):    
                                        if not continue_button.checkForInput(game_mouse_pos):
                                            move = player.make_move(game_state)

                                            if move is None:
                                                continue
                                            place_sound.play()
                                            counter = self.player1.time_per_turn
                                            prev_game_state = game_state
                                            game_state = move
                                            self.renderer.draw_grid(screen, game_state.grid, cell_size=45)
                                            
                    # computer
                    else:
                        if game_state.game_not_started:
                            move = game_state.make_move_to(7, 7).after_state
                            elapsed_time = 0
                        else:
                            import time 
                            start_time = time.time()
                            move = player.make_move(game_state)
                            end_time = time.time()
                            elapsed_time = int(end_time - start_time) - 1
                            if move is None:
                                continue
                        
                        place_sound.play()
                        counter = self.get_other_player(game_state).time_per_turn
                        player.remaining_time -= elapsed_time
                        prev_game_state = game_state
                        game_state = move
                        self.renderer.draw_grid(screen, game_state.grid, cell_size=45)
                        
                if isinstance(self.player1, ComputerPlayer) or isinstance(self.player2, ComputerPlayer):
                    counter = player.time_per_turn
                # check for winner
                if winner is not None:
                    win_sound.play()
                    if winner is self.player1.stone:
                        self.player1.score += 1
                    else:
                        self.player2.score += 1
                    
                    screen.fill(palette.BOARD_COLOR)
                    self.renderer.draw_board(screen, 15, 45)
                    self.renderer.draw_grid(screen, game_state.grid, cell_size=45)
                    self.renderer.display_total_time(screen, self.player1.remaining_time, self.player1.stone.value)
                    self.renderer.display_total_time(screen, self.player2.remaining_time, self.player2.stone.value)
                    game_state = GameState(Grid(15, 45))
                    winner = game_state.winner # None
                    stop = True
            self.renderer.draw_score(self.player1.score, self.player2.score, screen, player.stone.value)
            
    def get_current_player(self, game_state: GameState) -> Player:
        return self.player1 if game_state.current_stone == Stone.BLACK else self.player2
    
    def get_other_player(self, game_state: GameState) -> Player:
        return self.player2 if game_state.current_stone == Stone.BLACK else self.player1