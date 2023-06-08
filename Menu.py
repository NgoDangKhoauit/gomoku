import pygame
import sys
import os
import frontend.palette as palette
from frontend.button import Button
from pvp import pvp

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

initial_music_volume = 1
initial_sfx_volume = 1

# pygame.mixer.music.play(-1)


def get_font(name, size):
    font_file = os.path.join('font', name + '.ttf')

    return pygame.font.Font("font/font.ttf", size)


def set_sfx_volume(volume):
    click_sound.set_volume(volume)
    place_sound.set_volume(volume)


def pve_selection():
    pygame.display.set_caption("pve selection")

    font = pygame.font.Font(None, )

    levels = ["Easy", "Medium", "Hard"]
    time_per_turn = [10, 20, 30, -1, -2]
    min_per_player = [2, 5, 7, 10, -1, -2]

    curr_select = 0
    selected_level = 0
    selected_time = 0
    selected_min = 0

    while True:
        screen.blit(BG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    curr_select -= 1
                    if curr_select < 0:
                        curr_select = 3 - 1
                elif event.key == pygame.K_DOWN:
                    curr_select += 1
                    if curr_select > 3 - 1:
                        curr_select = 0

                elif event.key == pygame.K_LEFT:
                    if curr_select == 0:
                        selected_level -= 1
                        if selected_level < 0:
                            selected_level = len(levels) - 1

                    elif curr_select == 1:
                        selected_time -= 1
                        if selected_time < 0:
                            selected_time = len(time_per_turn) - 1

                    elif curr_select == 2:
                        selected_min -= 1
                        if selected_min < 0:
                            selected_min = len(min_per_player) - 1

                elif event.key == pygame.K_RIGHT:
                    if curr_select == 0:
                        selected_level += 1
                        if selected_level > len(levels) - 1:
                            selected_level = 0

                    elif curr_select == 1:
                        selected_time += 1
                        if selected_time > len(time_per_turn) - 1:
                            selected_time = 0

                    elif curr_select == 2:
                        selected_min += 1
                        if selected_min > len(min_per_player) - 1:
                            selected_min = 0

                elif event.key == pygame.K_ESCAPE:
                    options()

        difficulty_spacing = screen_size[0] // len(levels)
        time_spacing = screen_size[0] // len(time_per_turn)
        min_spacing = screen_size[0] // len(min_per_player)

        center_x = screen_size[0] // 2
        center_y = screen_size[1] // 2

        font = pygame.font.Font(None, 48)

        text_color = palette.WHITE

        for i, difficulty in enumerate(levels):
            text_color = palette.WHITE
            text = font.render(difficulty, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (center_x + (i - selected_level)
                                * difficulty_spacing, center_y)
            screen.blit(text, text_rect)

        for i, time in enumerate(time_per_turn):
            text_color = palette.WHITE
            text = font.render(str(time), True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (center_x + (i - selected_time)
                                * time_spacing, center_y + 50)
            screen.blit(text, text_rect)

        for i, min in enumerate(time_per_turn):
            text_color = palette.WHITE
            text = font.render(str(min), True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (center_x + (i - selected_min)
                                * min_spacing, center_y + 100)
            screen.blit(text, text_rect)

        pygame.display.flip()


def pvp_selection():
    pygame.display.set_caption("pvp selection")

    font = pygame.font.Font(None,)

    time_per_turn = [10, 20, 30, "inf", "custom"]
    min_per_player = [2, 5, 7, 10, "inf", "custom"]

    curr_select = 0
    selected_time = 0
    selected_min = 0

    custom_time = ""
    time_rect = pygame.Rect(
        screen_size[0] // 2 - 50, screen_size[1] // 8 + 100, 100, 32)
    custom_min = ""
    min_rect = pygame.Rect(
        screen_size[0] // 2 - 50, screen_size[1] // 8 + 300, 100, 32)

    while True:
        screen.blit(BG, (0, 0))

        pvp_mouse_pos = pygame.mouse.get_pos()

        time_button = Button(image=None, pos=(screen_size[0]//2, screen_size[1]//8),
                             text_input="Time per turn", font=get_font('Roboto-Medium', 40), base_color="white", hovering_color=palette.BLACK)

        min_button = Button(image=None, pos=(screen_size[0]//2, screen_size[1] // 8 + 200),
                            text_input="Minutes per player", font=get_font('Roboto-Medium', 40), base_color="white", hovering_color=palette.BLACK)

        for button in [time_button, min_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # up arrow key to change selection
                if event.key == pygame.K_UP:
                    curr_select -= 1
                    if curr_select < 0:
                        curr_select = 1

                # down arrow key to change selection
                elif event.key == pygame.K_DOWN:
                    curr_select += 1
                    if curr_select > 1:
                        curr_select = 0

                # left arrow key to change value
                elif event.key == pygame.K_LEFT:
                    # time per turn
                    if curr_select == 0:
                        selected_time -= 1
                        if selected_time < 0:
                            selected_time = len(time_per_turn) - 1

                    # minutes per player
                    elif curr_select == 1:
                        selected_min -= 1
                        if selected_min < 0:
                            selected_min = len(min_per_player) - 1

                # right arrow key to change value
                elif event.key == pygame.K_RIGHT:
                    # time per turn
                    if curr_select == 0:
                        selected_time += 1
                        if selected_time > len(time_per_turn) - 1:
                            selected_time = 0

                    # minutes per player
                    elif curr_select == 1:
                        selected_min += 1
                        if selected_min > len(min_per_player) - 1:
                            selected_min = 0

                # confirm and start the game
                elif event.key == pygame.K_ESCAPE:
                    play_menu()

                # go back to main menu
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # converting time per turn to int
                    if selected_time == len(time_per_turn) - 1:
                        time_value = int(custom_time)
                    elif selected_time == len(time_per_turn) - 2:
                        time_value = 99999
                    else:
                        time_value = time_per_turn[selected_time]
                    
                    # converting minutes per player to int
                    if selected_min == len(min_per_player) - 1:
                        min_value = int(custom_min)
                    elif selected_min == len(min_per_player) - 2:
                        min_value = 99999
                    else:
                        min_value = min_per_player[selected_min]
                    pvp(time_value, min_value)

                # custom time per turn
                if selected_time == len(time_per_turn) - 1:
                    if curr_select == 0:
                        if event.key == pygame.K_BACKSPACE:
                            custom_time = custom_time[:-1]
                        else:
                            custom_time += event.unicode
                # custom minutes per player
                if selected_min == len(min_per_player) - 1:
                    if curr_select == 1:
                        if event.key == pygame.K_BACKSPACE:
                            custom_min = custom_min[:-1]
                        else:
                            custom_min += event.unicode

                # check if the custom value is valid
                if selected_time == len(time_per_turn) - 1 or selected_min == len(min_per_player) - 1:
                    if curr_select == 0:
                        try:
                            time_value = int(custom_time)
                            if time_value > 900:
                                raise ValueError
                        except ValueError:
                            custom_time = ""
                    elif curr_select == 1:
                        try:
                            min_value = int(custom_min)
                            if time_value > 900:
                                raise ValueError
                        except ValueError:
                            custom_min = ""

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if time_button.checkForInput(pvp_mouse_pos):
                    click_sound.play()
                    curr_select = 0
                    # right click to increase value
                    if event.button == 3:
                        selected_time += 1
                        if selected_time > len(time_per_turn) - 1:
                            selected_time = 0
                            
                    # left click to decrease value
                    elif event.button == 1:
                        selected_time -= 1
                        if selected_time < 0:
                            selected_time = len(time_per_turn) - 1

                elif min_button.checkForInput(pvp_mouse_pos):
                    click_sound.play()
                    curr_select = 1
                    
                    # right click to increase value
                    if event.button == 3:
                        selected_min += 1
                        if selected_min > len(min_per_player) - 1:
                            selected_min = 0
                            
                    # left click to decrease value
                    elif event.button == 1:
                        selected_min -= 1
                        if selected_min < 0:
                            selected_min = len(min_per_player) - 1

        time_spacing = screen_size[0] // len(time_per_turn)
        min_spacing = screen_size[0] // len(min_per_player)

        center_x = screen_size[0] // 2
        center_y = screen_size[1] // 8

        font = pygame.font.Font(None, 48)

        text_color = palette.WHITE

        # Display time per turn
        for i, time in enumerate(time_per_turn):
            text_color = palette.RED if curr_select == 0 else palette.WHITE
            text = font.render(str(time), True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (center_x + (i - selected_time)
                                * time_spacing, center_y + 50)
            screen.blit(text, text_rect)

        if selected_time == len(time_per_turn) - 1:
            custom_time_text = font.render(custom_time, True, palette.WHITE)
            custom_time_width = max(50, custom_time_text.get_width())

            # Expand the time_rect on both sides
            time_rect_width = custom_time_width + 20  # Adjust the width as needed
            time_rect.left = center_x - time_rect_width // 2
            time_rect.width = time_rect_width

            # Display custom_time text within the expanded time_rect
            text_time = font.render(custom_time, True, palette.WHITE)
            text_time_rect = text_time.get_rect(center=time_rect.center)
            screen.blit(text_time, text_time_rect)
            pygame.draw.rect(screen, palette.WHITE, time_rect, 2)

        # Display minutes per player
        for i, min in enumerate(min_per_player):
            text_color = palette.RED if curr_select == 1 else palette.WHITE
            text = font.render(str(min), True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (center_x + (i - selected_min)
                                * min_spacing, center_y + 250)
            screen.blit(text, text_rect)

        if selected_min == len(min_per_player) - 1:
            custom_min_text = font.render(custom_min, True, palette.WHITE)
            custom_min_width = max(50, custom_min_text.get_width())

            # Expand the time_rect on both sides
            min_rect_width = custom_min_width + 20  # Adjust the width as needed
            min_rect.left = center_x - min_rect_width // 2
            min_rect.width = min_rect_width

            # Display custom_time text within the expanded time_rect
            text_min = font.render(custom_min, True, palette.WHITE)
            text_min_rect = text_min.get_rect(center=min_rect.center)
            screen.blit(text_min, text_min_rect)
            pygame.draw.rect(screen, palette.WHITE, min_rect, 2)

        pygame.display.flip()


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

        pygame.draw.rect(screen, (200, 200, 200), (slider_x,
                         music_slider_y, slider_width, slider_height))
        pygame.draw.rect(screen, (200, 200, 200), (slider_x,
                         sfx_slider_y, slider_width, slider_height))

        pygame.draw.rect(screen, (0, 128, 0), (slider_x, music_slider_y,
                         music_slider_position - slider_x, slider_height))
        pygame.draw.rect(screen, (0, 128, 0), (slider_x, sfx_slider_y,
                         sfx_slider_position - slider_x, slider_height))

        # Calculate and display the current music volume on a scale of 0 to 100
        current_music_volume = int(pygame.mixer.music.get_volume() * 100)
        initial_music_volume = current_music_volume / 100
        font = pygame.font.Font(None, 24)
        music_volume_text = font.render(
            f"Music Volume: {current_music_volume}", True, 'white')
        music_text_rect = music_volume_text.get_rect(
            center=(screen_size[0] // 2, music_slider_y - 20))
        screen.blit(music_volume_text, music_text_rect)

        # Calculate and display the current SFX volume on a scale of 0 to 100
        current_sfx_volume = int(click_sound.get_volume() * 100)
        initial_sfx_volume = current_sfx_volume / 100
        sfx_volume_text = font.render(
            f"SFX Volume: {current_sfx_volume}", True, 'white')
        sfx_text_rect = sfx_volume_text.get_rect(
            center=(screen_size[0] // 2, sfx_slider_y - 20))
        screen.blit(sfx_volume_text, sfx_text_rect)

        pygame.display.flip()  # Update the display


def play_menu():
    pygame.display.set_caption("play menu")

    while True:
        screen.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font('font', 60).render(
            "MODE SELECTION", True, "White")
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
                    pvp_selection()
                elif pve_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    pve_selection()
                elif bvb_button.checkForInput(menu_mouse_pos):
                    click_sound.play()

                elif back_button.checkForInput(menu_mouse_pos):
                    click_sound.play()
                    main_menu()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

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
                             text_input="PLAY", font=get_font('font', 75), base_color=palette.WHITE, hovering_color=palette.HOVER)
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
