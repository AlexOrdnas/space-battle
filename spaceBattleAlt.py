from random import randint

from pygame.font import Font
from pygame.time import delay, Clock
from pygame.draw import rect
from pygame.event import post, Event, get as get_events
from pygame.transform import rotate, scale
from pygame.display import set_mode, set_caption, set_icon, update
from pygame.image import load
from pygame.key import get_pressed
from pygame.constants import (
	USEREVENT, K_a, K_w, K_d, K_s, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_LCTRL,
	K_RCTRL, QUIT, KEYDOWN, K_ESCAPE, K_r, K_f)
from pygame import init, Rect, quit

init()
WIDTH, HEIGHT = 900, 500
SCREEN = set_mode((WIDTH, HEIGHT))
set_caption("Space Battle")
set_icon(load("graphics/spaceIcon.ico").convert_alpha())

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = Font("font/Lato-Bold.ttf", 50)
WINNER_FONT = Font("font/Lato-Bold.ttf", 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 40

HEAL_UP_WIDTH, HEAL_UP_HEIGHT = 30, 30
HEAL_UP_X, HEAL_UP_Y = randint(50, 850), randint(50, 450)

YELLOW_HIT = USEREVENT + 1
RED_HIT = USEREVENT + 2

YELLOW_SPACESHIP = rotate(scale(load(
	"graphics/spaceship_yellow.png").convert_alpha(),
	(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP = rotate(scale(load(
	"graphics/spaceship_red.png").convert_alpha(),
	(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = scale(load("graphics/space.png"), (WIDTH, HEIGHT))

#SHOOT_SOUND = mixer.Sound("Desktop/Visual Studio Code Files/Space Battle/sounds/laser_shoot_sfx.mp3")
#HIT_SOUND = mixer.Sound("Desktop/Visual Studio Code Files/Space Battle/sounds/explosion_sfx.mp3")

HEAL_UP = scale(
	load("graphics/heal_up.png").convert_alpha(),
	(HEAL_UP_WIDTH, HEAL_UP_HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    SCREEN.blit(SPACE, (0, 0))
    rect(SCREEN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    SCREEN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    SCREEN.blit(yellow_health_text, (10, 10))

    SCREEN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    SCREEN.blit(RED_SPACESHIP, (red.x, red.y))
    SCREEN.blit(HEAL_UP, (HEAL_UP_X, HEAL_UP_Y))

    for bullet in red_bullets:
        rect(SCREEN, RED, bullet)

    for bullet in yellow_bullets:
        rect(SCREEN, YELLOW, bullet)

    update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[K_d] and yellow.x + VEL + yellow.width - 20 < BORDER.x:
        yellow.x += VEL
    if keys_pressed[K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[K_s] and yellow.y + VEL + yellow.height + 5 < HEIGHT - 15:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[K_RIGHT] and red.x + VEL + red.width - 20 < WIDTH:
        red.x += VEL
    if keys_pressed[K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[K_DOWN] and red.y + VEL + red.height + 5 < HEIGHT - 15:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            post(Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            post(Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner_red(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    update()
    delay(3000)

def draw_winner_yellow(text):
    draw_text = WINNER_FONT.render(text, 1, YELLOW)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    update()
    delay(3000)

def heal_up(heal_list, yellow, heal, yellow_health, red, red_health):
    for heal in heal_list:
        if yellow.colliderect(heal):
            heal_list.clear()
            yellow_health += 5

    for heal in heal_list:
        if red.colliderect(heal):
            heal_list.clear()
            red_health += 5


def main():
    red = Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    heal = Rect(HEAL_UP_X, HEAL_UP_Y, HEAL_UP_WIDTH, HEAL_UP_HEIGHT)

    heal_list = [heal]

    red_bullets = list()
    yellow_bullets = list()

    red_health = 10
    yellow_health = 10

    clock = Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in get_events():
            if event.type == QUIT:
                run = False
                quit()

            if event.type == KEYDOWN:
                if event.key == K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #SHOOT_SOUND()

                if event.key == K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    #SHOOT_SOUND()

                if event.key == K_ESCAPE:
                    quit()

                if event.key == K_r:
                    main()
                
                if event.key == K_f:
                    red_health = 10
                    yellow_health = 10

            if event.type == RED_HIT:
                red_health -= 1
                #HIT_SOUND()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #HIT_SOUND()

        winner_text = str()
        if red_health <= 0:
            winner_text = "YELLOW WON!"

        if yellow_health <= 0:
            winner_text = "RED WON!"

        if winner_text != "":
            if yellow_health <= 0:
                draw_winner_red(winner_text)
            
            if red_health <= 0:
                draw_winner_yellow(winner_text)
            break 
        
        keys_pressed = get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        heal_up(heal_list, yellow, heal, yellow_health, red, red_health)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets,red_health, yellow_health)

if __name__ == "__main__":
    main()
