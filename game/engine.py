from dataclasses import dataclass
from typing import Callable, TypeAlias
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from players import Player
from renderers import Renderer
from logic.exceptions import InvalidMove
from logic.models import GameState, Grid, Piece
from logic.validators import validate_players

ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class Gomoku:
    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None
    
    def __post_init__(self):
        validate_players(self.player1, self.player2)
    
    def play(self, starting_piece: Piece = Piece.BLACK) -> None:
        game_state = GameState(Grid(), starting_piece)  
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            try:
                game_state = player.get_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)
            
    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_piece == Piece.BLACK:
            return self.player1
        else:
            return self.player2