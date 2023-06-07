import enum
import random
import re
import os
import sys
from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional, TYPE_CHECKING
import numpy as np
import time

class InvalidGameState(Exception):
    """Raised when the game state is invalid."""


class InvalidMove(Exception):
    """Raised when the move is invalid."""


class UnknownGameScore(Exception):
    """Raised when the game score is unknown."""

class Stone(enum.Enum):
    BLACK = 1
    WHITE = 2

    @property
    def other(self) -> "Stone":
        return Stone.BLACK if self is Stone.WHITE else Stone.WHITE


@dataclass
class Grid:
    # BOARD_SIZE: int 
    cells: np.ndarray
    cell_size: int

    def __init__(self, board_size: int, cell_size: int = 50):
        self.BOARD_SIZE = board_size
        self.cells = np.zeros((board_size, board_size), dtype=int)
        self.cell_size = cell_size
        self.validate_grid()
        
    def validate_grid(self) -> None:
        if self.BOARD_SIZE < 5:
            raise ValueError("BOARD_SIZE must be greater than or equal to 5")

        if self.cells.shape != (self.BOARD_SIZE, self.BOARD_SIZE):
            raise ValueError("cells shape does not match the BOARD_SIZE")

    @cached_property
    def black_count(self) -> int:
        return np.count_nonzero(self.cells == Stone.BLACK.value)

    @cached_property
    def white_count(self) -> int:
        return np.count_nonzero(self.cells == Stone.WHITE.value)

    @cached_property
    def empty_count(self) -> int:
        return np.count_nonzero(self.cells == 0)
    
    def update(self, new_cell):
        self.cells = new_cell
    
    def __str__(self) -> str:
        return "\n".join(" ".join(map(str, row)) for row in self.cells)
            

@dataclass(frozen=True)
class Move:
    stone: Stone
    cell_index: tuple
    before_state: "GameState"
    after_state: "GameState"


@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_stone: Stone = Stone.BLACK

    @cached_property
    def current_stone(self) -> Stone:
        if self.grid.black_count == self.grid.white_count:
            return self.starting_stone
        else:
            return self.starting_stone.other

    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == self.grid.BOARD_SIZE ** 2

    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie

    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0

    @cached_property
    def winner(self) -> Stone | None:
        for stone in Stone:
            if self.check_connect_five(stone.value):
                return stone

        return None

    def check_connect_five(self, value) -> bool:
        # Check rows
        for row in range(self.grid.BOARD_SIZE):
            for col in range(self.grid.BOARD_SIZE - 4):
                if np.all(self.grid.cells[row, col:col+5] == value):
                    return True

        # Check columns
        for col in range(self.grid.BOARD_SIZE):
            for row in range(self.grid.BOARD_SIZE - 4):
                if np.all(self.grid.cells[row:row+5, col] == value):
                    return True

        # Check diagonals
        for row in range(self.grid.BOARD_SIZE - 4):
            for col in range(self.grid.BOARD_SIZE - 4):
                if np.all(np.diag(self.grid.cells[row:row+5, col:col+5]) == value):
                    return True
                if np.all(np.diag(np.fliplr(self.grid.cells)[row:row+5, col:col+5]) == value):
                    return True

        return False

    def make_move_to(self, x: int, y: int) -> Optional[Move]:
        try:
            if x < 0 or y < 0 or x >= self.grid.BOARD_SIZE or y >= self.grid.BOARD_SIZE or self.grid.cells[x, y] != 0:
                raise InvalidMove("Invalid move")

            new_cells = np.copy(self.grid.cells)
            new_cells[x, y] = self.current_stone.value

            new_grid = Grid(board_size=self.grid.BOARD_SIZE)
            new_grid.cells = new_cells  # Assign the new cells directly to the existing grid
            new_state = GameState(new_grid, self.starting_stone)
            move = Move(self.current_stone, (x, y), self, new_state)

            return move
        except InvalidMove:
            return None

    def get_possible_moves(self) -> List[Move]:
        possible_moves = []
        for i in range(self.grid.BOARD_SIZE):
            for j in range(self.grid.BOARD_SIZE):
                if self.grid.cells[i, j] == 0:
                    move = self.make_move_to(i, j)
                    if move is not None:
                        possible_moves.append(move)
        return possible_moves

    def make_random_move(self) -> Optional[Move]:
        possible_moves = self.get_possible_moves()
        if not possible_moves:
            return None

        move = random.choice(possible_moves)
        return move

    def get_score(self) -> int:
        if self.tie:
            return 0
        if self.winner is None:
            raise UnknownGameScore("Cannot determine game score before it's over")

        return 1 if self.winner == self.starting_stone else -1