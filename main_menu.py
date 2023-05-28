import pygame
import sys
import os
import frontend.palette as palette
from frontend.button import Button

# initializations
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# screen section
screen_size = (900, 720)
screen = pygame.display.set_mode(screen_size)

# sound section
BG = pygame.image.load("image/main_menu.jpg")
BG = pygame.transform.scale(BG, screen_size)

BG_MUSIC = pygame.mixer.music.load("audio/background_music.wav")
click_sound = pygame.mixer.Sound("audio/clicking.wav")
place_sound = pygame.mixer.Sound("audio/placing_sound.wav")

initial_music_volume = 1.0
initial_sfx_volume = 1

# pygame.mixer.music.play(-1)

def get_font(name, size):
    font_file = os.path.join('font', name + '.ttf')

    return pygame.font.Font("font/font.ttf", size)

def set_sfx_volume(volume):
    click_sound.set_volume(volume)
    place_sound.set_volume(volume)

def options():
    pygame.display.set_caption("options")
    
    global initial_music_volume, initial_sfx_volume
    
    slider_width = 400
    slider_height = 20
    slider_x = (screen_size[0] - slider_width) // 2
    
    music_slider_y = (screen_size[1] - slider_height) // 2 - 100
    sfx_slider_y = (screen_size[1] - slider_height) // 2 
    music_slider_position = slider_x + (slider_width * initial_music_volume)
    sfx_slider_position = slider_x + (slider_width * initial_sfx_volume)
    
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        screen.blit(BG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if slider_x <= event.pos[0] <= slider_x + slider_width and music_slider_y <= event.pos[1] <= music_slider_y + slider_height:
                        # Calculate the music volume based on the mouse position
                        music_volume = (event.pos[0] - slider_x) / slider_width
                        # Adjust the music volume of your game accordingly
                        pygame.mixer.music.set_volume(music_volume)
                        # update music slider position
                        music_slider_position = event.pos[0]
                    if slider_x <= event.pos[0] <= slider_x + slider_width and sfx_slider_y <= event.pos[1] <= sfx_slider_y + slider_height:
                        # Calculate the sfx volume based on the mouse position
                        sfx_volume = (event.pos[0] - slider_x) / slider_width
                        set_sfx_volume(sfx_volume)
                        # update sfx slider position
                        sfx_slider_position = event.pos[0]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        
        pygame.draw.rect(screen, (200, 200, 200), (slider_x, music_slider_y, slider_width, slider_height))
        pygame.draw.rect(screen, (200, 200, 200), (slider_x, sfx_slider_y, slider_width, slider_height))
        
        pygame.draw.rect(screen, (0, 128, 0), (slider_x, music_slider_y, music_slider_position - slider_x, slider_height))
        pygame.draw.rect(screen, (0, 128, 0), (slider_x, sfx_slider_y, sfx_slider_position - slider_x, slider_height))
        
        # Calculate and display the current music volume on a scale of 0 to 100
        current_music_volume = int(pygame.mixer.music.get_volume() * 100)
        initial_music_volume = current_music_volume / 100
        font = pygame.font.Font(None, 24)
        music_volume_text = font.render(f"Music Volume: {current_music_volume}", True, 'white')
        music_text_rect = music_volume_text.get_rect(center=(screen_size[0] // 2, music_slider_y - 20))
        screen.blit(music_volume_text, music_text_rect)

        # Calculate and display the current SFX volume on a scale of 0 to 100
        current_sfx_volume = int(click_sound.get_volume() * 100)
        initial_sfx_volume = current_sfx_volume / 100
        sfx_volume_text = font.render(f"SFX Volume: {current_sfx_volume}", True, 'white')
        sfx_text_rect = sfx_volume_text.get_rect(center=(screen_size[0] // 2, sfx_slider_y - 20))
        screen.blit(sfx_volume_text, sfx_text_rect)

        pygame.display.flip()  # Update the display
        
def play_menu():
    pygame.display.set_caption("play menu")
    
    while True:
        screen.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font('font', 60).render("MODE SELECTION", True, "White")
        menu_rect = menu_text.get_rect(center=(450, 90))

        pvp_button = Button(image=None, pos=(452, 200),
                            text_input="PVP", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)
        pve_button = Button(image=None, pos=(453, 350),
                            text_input="PVE", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)
        bvb_button = Button(image=None, pos=(454, 500),
                            text_input="BVB", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)
        back_button = Button(image=None, pos=(454, 650),
                            text_input="BACK", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)

        screen.blit(menu_text, menu_rect)

        for button in [pvp_button, pve_button, bvb_button, back_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    
                elif pve_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    
                elif bvb_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    
                elif back_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    main_menu()
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_paused:
                        pygame.mixer.music.unpause()
                        is_paused = False
                    else:
                        pygame.mixer.music.pause()
                        is_paused = True
                    
        pygame.display.update()


def main_menu():
    pygame.display.set_caption("main menu")
    is_paused = False
    while True:
        screen.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font('font', 100).render("MAIN MENU", True, "White")
        menu_rect = menu_text.get_rect(center=(450, 100))

        play_button = Button(image=pygame.image.load("image/Play Rect.png"), pos=(452, 250),
                            text_input="PLAY", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)
        option_button = Button(image=pygame.image.load("image/Options Rect.png"), pos=(453, 400),
                            text_input="OPTIONS", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)
        quit_button = Button(image=pygame.image.load("image/Quit Rect.png"), pos=(454, 550),
                            text_input="QUIT", font=get_font('font', 75), base_color="white", hovering_color=palette.HOVER)

        screen.blit(menu_text, menu_rect)

        for button in [play_button, option_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    play_menu()
                elif option_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    options()
                elif quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_paused:
                        pygame.mixer.music.unpause()
                        is_paused = False
                    else:
                        pygame.mixer.music.pause()
                        is_paused = True
                    
        pygame.display.update()

main_menu()
