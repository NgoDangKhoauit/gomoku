from player import HumanPlayer, MCTSPlayer
from engine import Gomoku
from models import Stone
from frontend.renderer import Renderer 

player1 = MCTSPlayer(Stone.BLACK, 9999, 99)
player2 = HumanPlayer(Stone.WHITE, 9999, 99)
renderer = Renderer()
game = Gomoku(player1, player2, renderer)
game.play()