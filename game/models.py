import enum
import random
import os
import sys
from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional, TYPE_CHECKING
import numpy as np
import time
from game.exceptions import InvalidMove, InvalidGameState, UnknownGameScore

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
    
    def test(self) -> int:
        return self.grid.empty_count

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

# import multiprocessing
# class Minimax:
    
#     def __init__(self, max_depth: int = 3, num_processes: int = multiprocessing.cpu_count()):
#         self.max_depth = max_depth
#         self.num_processes = num_processes
#         self.transposition_table = {}

#     def evaluate(self, state: GameState, stone: Stone) -> int:
#         if state.winner == stone:
#             return 1
#         elif state.winner == stone.other:
#             return -1
#         else:
#             return 0

#     def zobrist_hash(self, state: GameState) -> int:
#         hash_key = state.grid.cells.tobytes()
#         return hash_key

#     def lookup_transposition_table(self, state: GameState) -> Optional[int]:
#         hash_key = self.zobrist_hash(state)
#         return self.transposition_table.get(hash_key)

#     def store_transposition_table(self, state: GameState, score: int):
#         hash_key = self.zobrist_hash(state)
#         self.transposition_table[hash_key] = score

#     def minimax(self, state: GameState, depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
#         transposition_score = self.lookup_transposition_table(state)
#         if transposition_score is not None:
#             return transposition_score

#         if depth == 0 or state.game_over:
#             eval_score = self.evaluate(state, state.current_stone)
#             self.store_transposition_table(state, eval_score)
#             return eval_score

#         if maximizing_player:
#             max_eval = float("-inf")
#             for move in state.get_possible_moves():
#                 new_state = move.after_state
#                 eval_score = self.minimax(new_state, depth - 1, alpha, beta, False)
#                 max_eval = max(max_eval, eval_score)
#                 alpha = max(alpha, eval_score)
#                 if beta <= alpha:
#                     break  # Beta cutoff
#             self.store_transposition_table(state, max_eval)
#             return max_eval
#         else:
#             min_eval = float("inf")
#             for move in state.get_possible_moves():
#                 new_state = move.after_state
#                 eval_score = self.minimax(new_state, depth - 1, alpha, beta, True)
#                 min_eval = min(min_eval, eval_score)
#                 beta = min(beta, eval_score)
#                 if beta <= alpha:
#                     break  # Alpha cutoff
#             self.store_transposition_table(state, min_eval)
#             return min_eval
    
# def evaluate_move(move, max_depth, alpha, beta):
#     new_state = move.after_state
#     eval_score = minimax.minimax(new_state, max_depth, alpha, beta, False)
#     return eval_score

# def get_best_move(minimax, state):
#     possible_moves = state.get_possible_moves()
#     if not possible_moves:
#         return None

#     best_score = float("-inf")
#     best_move = None
#     alpha = float("-inf")
#     beta = float("inf")

#     pool = multiprocessing.Pool(processes=minimax.num_processes)
#     eval_scores = pool.starmap(evaluate_move, [(move, minimax.max_depth, alpha, beta) for move in possible_moves])
#     pool.close()

#     for i, move in enumerate(possible_moves):
#         if eval_scores[i] > best_score:
#             best_score = eval_scores[i]
#             best_move = move
#         alpha = max(alpha, eval_scores[i])

#     return best_move

# grid = Grid(15)
# state = GameState(grid)

# move = state.make_move_to(0, 0)
# state = move.after_state
# move = state.make_move_to(1, 0)
# state = move.after_state
# move = state.make_move_to(0, 1)
# state = move.after_state
# move = state.make_move_to(1, 1)
# state = move.after_state
# move = state.make_move_to(0, 2)
# state = move.after_state
# move = state.make_move_to(1, 2)
# state = move.after_state
# move = state.make_move_to(0, 3)
# state = move.after_state
# move = state.make_move_to(1, 3)
# state = move.after_state


# minimax = Minimax(max_depth=2)
# import time
# # Get the best move
# start_time = time.time()
# best_move = get_best_move(minimax, state)
# end_time = time.time()
# elapsed_time = end_time - start_time
# if best_move is not None:
#     state = best_move.after_state
#     print("Best move:", best_move.cell_index)
#     print("elapsed_time:", elapsed_time)
# else:
#     print("No possible moves.")