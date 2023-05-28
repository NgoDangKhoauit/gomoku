from __future__ import annotations
import enum
from dataclasses import dataclass
from functools import cached_property

from validators import validate_game_state, validate_grid

BOARD_SIZE = 15

class Piece(str, enum.Enum):
    BLACK = 'b'
    WHITE = 'w'
    
    @property
    def other(self) -> Piece:
        return Piece.BLACK if self == Piece.WHITE else Piece.WHITE
    
@dataclass(frozen=True)
class Grid:
    cells: str = " " * (BOARD_SIZE ** 2)
    
    def __post_init__(self) -> None:
        validate_grid(self)
    
    @cached_property
    def b_count(self) -> int:
        return self.cells.count(Piece.BLACK)
    
    @cached_property
    def w_count(self) -> int:
        return self.cells.count(Piece.WHITE)
    
    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")

@dataclass(frozen=True)
class Move:
    piece: Piece
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"
    
@dataclass(frozen=True)
class GameState:
    piece: Piece
    starting_piece: Piece = Piece.BLACK
    
    def __post_init__(self) -> None:
        validate_game_state(self)

    @cached_property
    def current_piece(self) -> Piece:
        if self.grid.b_count == self.grid.w_count:
            return self.starting_piece
        else:
            return self.starting_piece.other
        
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 225
    
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0
    
    @cached_property
    def winner(self) -> Piece | None:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # right, down, diagonal (down-right), diagonal (down-left)
        for direction in directions:
            if self.check_direction(direction):
                return self.current_piece.other

        return None

    def check_direction(self, direction: tuple[int, int]) -> bool:
        dx, dy = direction
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece = self.grid.cells[i * BOARD_SIZE + j]
                if piece != " ":
                    for k in range(1, 5):
                        ni, nj = i + k * dx, j + k * dy
                        if not (0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE):
                            break
                        if self.grid.cells[ni * BOARD_SIZE + nj] != piece:
                            break
                    else:
                        return True
        return False
    
    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.grid.cells[i * BOARD_SIZE + j] == " ":
                        moves.append(self.make_move_to(i * BOARD_SIZE + j))
        return moves
    
    def make_move_to(self, index: int) -> Move:
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        new_cells = list(self.grid.cells)
        new_cells[index] = self.current_piece.value
        
        new_grid = Grid("".join(new_cells))
        
        return Move(
            piece=self.current_piece,
            cell_index=index,
            before_state=self,
            after_state=GameState(
                piece=self.current_piece.other,
                starting_piece=self.starting_piece,
                grid=new_grid
            ),
        )
        