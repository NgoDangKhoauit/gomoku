from models import GameState, Stone, Move, Grid
import abc
from exceptions import InvalidMove
import time, sys, os
import pygame
from frontend.button import Button
from frontend.renderer import Renderer
import frontend.palette as palette
import numpy as np
import cv2
from typing import List, Optional
import random

class Player(metaclass=abc.ABCMeta):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int) -> None:
        self.stone = stone
        self.time_per_turn = time_per_turn
        self.minutes_per_player = minutes_per_player
    
    def make_move(self, game_state: GameState) -> Move:
        if self.stone is game_state.current_stone:
            move = self.get_move(game_state)
            if move is None:
                return None
            return move.after_state
    
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state"""

class HumanPlayer(Player):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int) -> None:
        super().__init__(stone, time_per_turn, minutes_per_player)
        
    def get_move(self, game_state: GameState) -> Move | None:
        index = board_to_index(pygame.mouse.get_pos())
        return game_state.make_move_to(x=index[1], y=index[0])

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

import numpy as np
import copy


class MCTSPlayer(Player):
    def __init__(self, stone: Stone, time_per_turn: int, minutes_per_player: int, exploration_constant: float = 1.4) -> None:
        super().__init__(stone, time_per_turn, minutes_per_player)
        self.exploration_constant = exploration_constant
    
    def get_move(self, game_state: GameState) -> Move | None:
        start_time = time.time()
        while time.time() - start_time < self.time_per_turn:
            mcts = MCTS(game_state, self.exploration_constant)
            best_move = mcts.get_best_move()
            if best_move is None:
                return None
            game_state = best_move.after_state

        return game_state

class MCTS:
    def __init__(self, initial_state: GameState, exploration_constant: float = 1.4):
        self.initial_state = initial_state
        self.exploration_constant = exploration_constant

    def get_best_move(self) -> Move | None:
        root_node = Node(state=self.initial_state)

        for _ in range(1000):  # Perform 1000 MCTS simulations (you can adjust this value as needed)
            selected_node = self.select_node(root_node)
            expanded_node = self.expand_node(selected_node)
            score = self.simulate_node(expanded_node)
            self.backpropagate(expanded_node, score)

        best_child = self.select_best_child(root_node)
        return best_child.move if best_child else None

    def select_node(self, node: "Node") -> "Node":
        while node.is_fully_expanded() and not node.is_terminal():
            node = self.select_best_child(node)
        return node

    def expand_node(self, node: "Node") -> "Node":
        if node.is_terminal():
            return node

        untried_moves = node.get_untried_moves()
        if untried_moves:
            random_move = random.choice(untried_moves)
            new_state = random_move.after_state
            new_node = Node(state=new_state, move=random_move, parent=node)
            node.add_child(new_node)
            return new_node

        best_child = self.select_best_child(node)
        return best_child

    def simulate_node(self, node: "Node") -> float:
        state = node.state
        while not state.game_over:
            move = state.make_random_move()
            state = move.after_state
        return self.get_score(state)

    def backpropagate(self, node: "Node", score: float) -> None:
        while node:
            node.update_stats(score)
            node = node.parent

    def select_best_child(self, node: "Node") -> Optional["Node"]:
        children = node.children
        if not children:
            return None

        total_visits = sum(child.visits for child in children)
        best_score = float("-inf")
        best_child = None

        for child in children:
            child_score = child.get_score(self.exploration_constant, total_visits)
            if child_score > best_score:
                best_score = child_score
                best_child = child

        return best_child

    @staticmethod
    def get_score(state: GameState) -> float:
        if state.tie:
            return 0.5
        winner = state.winner
        if winner is None:
            pass
        if winner is state.starting_stone:
            return 1.0
        return 0.0


class Node:
    def __init__(self, state: GameState, move: Move = None, parent: "Node" = None):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0.0

    def is_fully_expanded(self) -> bool:
        return len(self.get_untried_moves()) == 0

    def is_terminal(self) -> bool:
        return self.state.game_over

    def get_untried_moves(self) -> List[Move]:
        return self.state.get_possible_moves()

    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def update_stats(self, score: float) -> None:
        self.visits += 1
        self.score += score

    def get_score(self, exploration_constant: float, total_visits: int) -> float:
        exploitation = self.score / self.visits
        exploration = exploration_constant * np.sqrt(np.log(total_visits) / self.visits)
        return exploitation + exploration



