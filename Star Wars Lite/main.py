import pygame, sys
from pygame import mixer
import os
import time
import random
import warnings
from structs import elements, root, sprites

warnings.filterwarnings("ignore")

pygame.font.init()
pygame.init()
mixer.init()
pygame.display.set_caption("Star Wars Lite")

mixer.music.load(r"sounds\main_music.mp3")
mixer.music.play(-1)

def game_menu():

    title_font = pygame.font.Font(r"fonts\Starjedi.ttf", 60)
    menu_font = pygame.font.Font(r"fonts\Starjedi.ttf", 40)

    run = True
    while run:
        
        sprites.WINDOW.blit(sprites.BACKGROUND, (0, 0))
        title_text = title_font.render("Star Wars Lite", 1, (255, 255, 0))

        play_btn = elements.button('assets\menu\play-active.png', 'assets\menu\play-inactive.png', 295,"play")
        options_btn = elements.button('assets\menu\options-active.png', 'assets\menu\options-inactive.png', 355,"options")
        exit_btn = elements.button('assets\menu\exit-active.png', 'assets\menu\exit-inactive.png', 415,"exit")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        sprites.WINDOW.blit(title_text, (sprites.WIDTH / 2 - title_text.get_width() / 2, 30))

        pygame.display.update()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_menu()
    