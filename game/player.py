from game.models import GameState, Stone, Move, Grid
import abc
from game.exceptions import InvalidMove
import time, sys, os
import pygame
from frontend.button import Button
from frontend.renderer import Renderer
import frontend.palette as palette
import numpy as np
import cv2
from typing import List, Optional
import random, multiprocessing

class Player(metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int) -> None:
        self.stone = stone
        self.time_per_turn = time_per_turn
        self.minutes_per_player = minutes_per_player
        self.remaining_time = minutes_per_player * 60
        self.score = 0
    
    def make_move(self, game_state: GameState) -> Move:
        if self.stone is game_state.current_stone:
            move = self.get_move(game_state)
            if move is None:
                return None
            return move.after_state
    
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state"""

class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int, delay_second=1) -> None:
        super().__init__(stone, time_per_turn, minutes_per_player)
        self.delay_second = delay_second
        
    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_second)
        return self.get_computer_move(game_state)
    
    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer player's move in the given game state"""

class HumanPlayer(Player):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int) -> None:
        super().__init__(stone, time_per_turn, minutes_per_player)
        
    def get_move(self, game_state: GameState) -> Move | None:
        index = board_to_index(pygame.mouse.get_pos())
        return game_state.make_move_to(x=index[1], y=index[0])

class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.make_random_move()

class MinimaxComputerPlayer(ComputerPlayer):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int, 
                 delay_second=0, max_depth=2, num_processes=multiprocessing.cpu_count() - 1) -> None:
        super().__init__(stone, time_per_turn, minutes_per_player)
        self.minimax = Minimax(max_depth=max_depth, num_processes=num_processes)
        
    def get_computer_move(self, game_state: GameState) -> Move | None:
        best_move = self.minimax.get_best_move(game_state)
        return best_move

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

import multiprocessing
class Minimax:
    
    def __init__(self, max_depth: int = 3, num_processes: int = multiprocessing.cpu_count()):
        self.max_depth = max_depth
        self.num_processes = num_processes
        self.transposition_table = {}

    def evaluate(self, state: GameState, stone: Stone) -> int:
        if state.winner == stone:
            return 1
        elif state.winner == stone.other:
            return -1
        else:
            return 0

    def zobrist_hash(self, state: GameState) -> int:
        hash_key = state.grid.cells.tobytes()
        return hash_key

    def lookup_transposition_table(self, state: GameState) -> Optional[int]:
        hash_key = self.zobrist_hash(state)
        return self.transposition_table.get(hash_key)

    def store_transposition_table(self, state: GameState, score: int):
        hash_key = self.zobrist_hash(state)
        self.transposition_table[hash_key] = score

    def minimax(self, state: GameState, depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
        transposition_score = self.lookup_transposition_table(state)
        if transposition_score is not None:
            return transposition_score

        if depth == 0 or state.game_over:
            eval_score = self.evaluate(state, state.current_stone)
            self.store_transposition_table(state, eval_score)
            return eval_score

        if maximizing_player:
            max_eval = float("-inf")
            for move in state.get_possible_moves():
                new_state = move.after_state
                eval_score = self.minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            self.store_transposition_table(state, max_eval)
            return max_eval
        else:
            min_eval = float("inf")
            for move in state.get_possible_moves():
                new_state = move.after_state
                eval_score = self.minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            self.store_transposition_table(state, min_eval)
            return min_eval
    
    def evaluate_move(self, move, max_depth, alpha, beta):
        new_state = move.after_state
        eval_score = self.minimax(new_state, max_depth, alpha, beta, False)
        return eval_score

    def get_best_move(self, state):
        possible_moves = state.get_possible_moves()
        if not possible_moves:
            return None

        best_score = float("-inf")
        best_move = None
        alpha = float("-inf")
        beta = float("inf")

        pool = multiprocessing.Pool(processes=self.num_processes)
        eval_scores = pool.starmap(self.evaluate_move, [(move, self.max_depth, alpha, beta) for move in possible_moves])
        pool.close()

        for i, move in enumerate(possible_moves):
            if eval_scores[i] > best_score:
                best_score = eval_scores[i]
                best_move = move
            alpha = max(alpha, eval_scores[i])

        return best_move

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
# best_move = minimax.get_best_move(state)
# end_time = time.time()
# elapsed_time = end_time - start_time
# if best_move is not None:
#     state = best_move.after_state
#     print("Best move:", best_move.cell_index)
#     print("elapsed_time:", elapsed_time)
# else:
#     print("No possible moves.")
    
# print(state.grid.cells)
