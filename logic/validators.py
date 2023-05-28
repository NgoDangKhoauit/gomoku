from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Grid, GameState, Piece

def validate_grid(grid: Grid) -> None:
    if len(grid.cells) != 225:
        raise ValueError("Grid must have 225 cells")

from exceptions import InvalidGameState

def validate_game_state(game_state: GameState) -> None:
    validate_number_of_pieces(game_state.grid)
    validate_starting_piece(game_state.grid, game_state.starting_piece)
    validate_winner(game_state.grid, game_state.starting_piece, game_state.winner)
    
def validate_number_of_pieces(grid: Grid) -> None:
    if abs(grid.b_count - grid.w_count) > 1:
        raise InvalidGameState("Wrong number of black and white pieces")
    
def validate_starting_mark(grid: Grid) -> None:
    if abs(grid.b_count - grid.w_count) > 1:
        raise InvalidGameState("Wrong number of black and white pieces")

def validate_winner(grid: Grid, winner: Piece | None) -> None:
    if winner == Piece.BLACK:
        if grid.b_count <= grid.w_count:
            raise InvalidGameState("Wrong number of black and white pieces")
    
    elif winner == Piece.WHITE:
        if grid.w_count != grid.b_count:
            raise InvalidGameState("Wrong number of black and white pieces")