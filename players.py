from models import GameState, Stone, Move
import abc
from exceptions import InvalidMove
import time, sys, os
import pygame

class Player(metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone) -> None:
        self.stone = stone
        
    def make_move(self, game_state: GameState) -> GameState:
        if self.stone is game_state.current_stone:
            move = self.get_move(game_state)
            while move is None and not game_state.game_over:
                move = self.get_move(game_state)
            return move.after_state
        else:
            raise InvalidMove("Not your turn")
        
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state"""
   
class HumanPlayer(Player):
    def __init__(self, stone: Stone, time, sec) -> None:
        super().__init__(stone)
    
    def get_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        try:
                            index = board_to_index(pygame.mouse.get_pos())
                        except ValueError:
                            print("wrong cooridnates")
                        else:
                            try:
                                return game_state.make_move_to(x=index[1], y=index[0])
                            except InvalidMove:
                                print("Invalid move")
        
class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone, delay_seconds: float = 0.25) -> None:
        super().__init__(stone)
        self.delay_seconds = delay_seconds
        
    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)
    
    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer player's move in the given game state"""
        
class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.make_random_move()
    
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