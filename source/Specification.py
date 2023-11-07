# This is the file to declare the setting variables.
import pygame

# Window
APP_WIDTH, APP_HEIGHT = 610, 670
APP_CAPTION = r"Pacman"
FPS = 60

# File result
file_result = open(f"../output/result.txt", "w")


# Background
HOME_BACKGROUND = r"../Assets/bg/home_bg.png"
ABOUT_BACKGROUND = r"../Assets/bg/about_bg.png"


# Screen state
STATE_HOME = "home"
STATE_PLAYING = "playing"
STATE_ABOUT = "about"
STATE_LEVEL = "level"
STATE_SETTING = "setting"


# Home screen
HOME_BG_WIDTH, HOME_BG_HEIGHT = APP_WIDTH, APP_HEIGHT - 410
START_POS = pygame.Rect(((APP_WIDTH - 300)/ 2) , 325, 300, 50)
SETTING_POS = pygame.Rect(((APP_WIDTH - 300)/ 2), 405, 300, 50)
ABOUT_POS = pygame.Rect(((APP_WIDTH - 300)/ 2), 485, 300, 50)
EXIT_POS = pygame.Rect(((APP_WIDTH - 300)/ 2), 565, 300, 50)


# Level screen
LEVEL_1_POS = pygame.Rect(150, 320, 300, 50)
LEVEL_2_POS = pygame.Rect(150, 390, 300, 50)
LEVEL_3_POS = pygame.Rect(150, 460, 300, 50)
LEVEL_4_POS = pygame.Rect(150, 530, 300, 50)
LEVEL_5_POS = pygame.Rect(150, 600, 300, 50)
BACK_LEVEL_POS = pygame.Rect(500, 600, 70, 50)


# About screen
BACK_POS = pygame.Rect(225, 530, 150, 50)


# Setting screen
OK_POS = pygame.Rect(255, 620, 100, 50)
TRIANGLE_1_POS = [[360, 620], [360, 670], [403.3, 645]]
TRIANGLE_2_POS = [[250, 620], [250, 670], [206.7, 645]]


# Play screen

SPEED = 250

# Color
BACKGROUND_COLOR = (65, 98, 132)
LIGHT_GREY = (170, 170, 170)
DARK_GREY = (75, 75, 75)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TOMATO = (255, 99, 71)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
