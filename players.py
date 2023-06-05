from models import GameState, Stone, Move
import abc
from exceptions import InvalidMove
import time

class Player(metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone) -> None:
        self.stone = stone
        
    def make_move(self, game_state: GameState) -> GameState:
        if self.stone is game_state.current_stone:
            move = self.get_move(game_state)
            return move.after_state
        else:
            raise InvalidMove("Not your turn")
        
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state"""
        
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