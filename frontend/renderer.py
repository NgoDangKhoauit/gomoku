import abc, sys
import pygame, cv2, os
import numpy as np

from models import GameState, Grid
import frontend.palette as palette
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def round_number(number: int):
    if number % 2:
        return number/2
    return (number + 1)/2
        
class Renderer():
    
    def get_font(self, name, size):
        font_file = os.path.join('font', name + '.ttf')

        return pygame.font.Font("font/font.ttf", size)
    
    def draw_board(screen, board_size, cell_size):
        for i in range(1, board_size + 1):
            pygame.draw.line(screen, palette.BLACK, [cell_size * i, cell_size], [cell_size * i, cell_size*15], 2)
            pygame.draw.line(screen, palette.BLACK, [cell_size, cell_size * i], [cell_size*15, cell_size * i], 2)
            
        pygame.draw.circle(screen, palette.BLACK, [cell_size * 8, cell_size * 8], 5)
        pygame.draw.circle(screen, palette.BLACK, [cell_size * 4, cell_size * 4], 5)
        pygame.draw.circle(screen, palette.BLACK, [cell_size * 12, cell_size * 4], 5)
        pygame.draw.circle(screen, palette.BLACK, [cell_size * 4, cell_size * 12], 5)
        pygame.draw.circle(screen, palette.BLACK, [cell_size * 12, cell_size * 12], 5)
        pygame.display.update()
        
    def board_to_grid(screen, x_pos, y_pos, cell_size):
        if x_pos % cell_size > round_number(x_pos):
            x_pos = (x_pos - x_pos % cell_size) + cell_size
        else:
            x_pos = x_pos - x_pos % cell_size
        
        if y_pos % cell_size > round_number(y_pos):
            y_pos = (y_pos - y_pos % cell_size) + cell_size
        else:
            y_pos = y_pos - y_pos % cell_size
            
        return x_pos, y_pos
        
    def draw_grid(self, screen, grid: Grid, cell_size: int) -> None:
        for row in range(grid.BOARD_SIZE):
            for col in range(grid.BOARD_SIZE):
                if grid.cells[row, col] == 1:
                    pygame.draw.circle(screen, palette.BLACK, [cell_size * (col + 1), cell_size * (row + 1)], cell_size//2)
                elif grid.cells[row, col] == 2:
                    pygame.draw.circle(screen, palette.WHITE, [cell_size * (col + 1), cell_size * (row + 1)], cell_size//2)
        update_rect = pygame.Rect(0, 0, cell_size * grid.BOARD_SIZE, cell_size * grid.BOARD_SIZE)
        pygame.display.update(update_rect)
        
    def drawArcCv2(self, surf, color, center, radius, width, start_angle, end_angle):
        circle_image = np.zeros((radius * 2 + 4, radius * 2 + 4, 4), dtype=np.uint8)
        circle_image = cv2.ellipse(circle_image, (radius + 2, radius + 2),
                                   (radius - width // 2, radius - width // 2), 0, start_angle, end_angle,
                                   (*color, 255), width, lineType=cv2.LINE_AA)
        circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius * 2 + 4, radius * 2 + 4), 'RGBA')
        surf.blit(circle_surface, circle_surface.get_rect(center=center),
                  special_flags=pygame.BLEND_PREMULTIPLIED)
    
    def draw_score(self, player1_score, player2_score, screen, board_size=15, cell_size=45):
        
        y_center = screen.get_height() // 2
        
        p1_center = cell_size * board_size + cell_size
        p1_score_center = cell_size * board_size + (screen.get_width() - cell_size * board_size) // 2
        p1_color = palette.BLACK
        p1_text = self.get_font("Roboto-Medium", 20).render("Player 1", True, p1_color)
        screen.blit(p1_text, (p1_center, y_center - cell_size * 2))

        # Draw Player 1 score
        score_font = pygame.font.Font(None, 45)
        p1_score_text = score_font.render(str(player1_score), True, p1_color)
        screen.blit(p1_score_text, (p1_score_center, y_center - cell_size - 1))

        # Draw "Player 2" text
        p2_color = palette.WHITE
        p2_text = self.get_font("Roboto-Medium", 20).render("Player 2", True, p2_color)
        screen.blit(p2_text, (p1_center, y_center + cell_size * 2 - 20))

        # Draw Player 2 score
        p2_score_text = score_font.render(str(player2_score), True, p2_color)
        screen.blit(p2_score_text, (p1_score_center, y_center + cell_size - 20))
        
    

# screen_size = (700, 700)
# screen = pygame.display.set_mode(screen_size)

# pygame.init()        


# game_state = GameState(Grid(15, cell_size=45))

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # Render the game state
#     a.render(game_state)

#     pygame.display.update()

        
