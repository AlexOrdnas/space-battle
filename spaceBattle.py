import pygame

pygame.init()
WIDTH, HEIGHT = 900, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")
iconImage = pygame.image.load("graphics/spaceIcon.ico").convert_alpha()
pygame.display.set_icon(iconImage)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

MENU_WHITE = (253, 255, 250)
MENU_BLUE = (51, 102, 153)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.Font("font/Lato-Bold.ttf", 40)
WINNER_FONT = pygame.font.Font("font/Lato-Bold.ttf", 100)
MENU_FONT = pygame.font.Font("font/Lato-Bold.ttf", 50)

FPS = 60
VEL = 5
BULLET_VEL = 12
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load("graphics/spaceship_yellow.png").convert_alpha()
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_ZOOM = pygame.transform.rotozoom(YELLOW_SPACESHIP, 0, 2)
YELLOW_SPACESHIP_RECT = YELLOW_SPACESHIP_ZOOM.get_rect(center = (150, HEIGHT / 2))

RED_SPACESHIP_IMAGE = pygame.image.load("graphics/spaceship_red.png").convert_alpha()
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_ZOOM = pygame.transform.rotozoom(RED_SPACESHIP, 0, 2)
RED_SPACESHIP_RECT = RED_SPACESHIP_ZOOM.get_rect(center = (750, HEIGHT / 2))

SPACE = pygame.transform.scale(pygame.image.load("graphics/space.png").convert_alpha(), (WIDTH, HEIGHT))

SHOOT_SOUND = pygame.mixer.Sound("sounds/laser_shoot_sfx.wav")
SHOOT_SOUND.set_volume(0.5)

HIT_SOUND = pygame.mixer.Sound("sounds/explosion_sfx.wav")
HIT_SOUND.set_volume(0.5)

WIN_MUSIC = pygame.mixer.Sound("sounds/win_sfx.wav")
WIN_MUSIC.set_volume(5)

BACKGROUND_MUSIC = pygame.mixer.Sound("sounds/background_music.wav")
BACKGROUND_MUSIC.set_volume(0.1)
BACKGROUND_MUSIC.play(-1)

MENU_MUSIC = pygame.mixer.Sound("sounds/menu_music.wav")
MENU_MUSIC.set_volume(0.1)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    SCREEN.blit(SPACE, (0, 0))
    pygame.draw.rect(SCREEN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health) , 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " +  str(yellow_health), 1, WHITE)
    SCREEN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    SCREEN.blit(yellow_health_text, (10, 10))

    SCREEN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    SCREEN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(SCREEN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(SCREEN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if pygame.key.get_pressed()[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 20 < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 5 < HEIGHT - 15:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width - 20 < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 5 < HEIGHT - 15:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner_red(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_winner_yellow(text):
    draw_text = WINNER_FONT.render(text, 1, YELLOW)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_winner_green(text):
    draw_text = WINNER_FONT.render(text, 1, GREEN)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()  
    game_active = False
    
    '''
    if game_active == True:    
        MENU_MUSIC.stop()
        BACKGROUND_MUSIC.play(-1)
    else:
        MENU_MUSIC.play(-1)
    '''            
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                                
            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        SHOOT_SOUND.play()

                    if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        SHOOT_SOUND.play()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        pygame.time.delay(1000)
                
                if game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            red_health = 10
                            yellow_health = 10
                            
                    if event.type == pygame.KEYDOWN:    
                        if event.key == pygame.K_m:
                            game_active = False
            
            if game_active:
                if event.type == RED_HIT:
                    red_health -= 1
                    HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                    HIT_SOUND.play()

        if game_active:
            winner_text = ""
            if red_health <= 0:
                winner_text = "YELLOW WON!"

            if yellow_health <= 0:
                winner_text = "RED WON!"
            
            if yellow_health <= 0 and red_health <= 0:
                winner_text = "DRAW!"

            if winner_text != "":
                if yellow_health <= 0:
                    BACKGROUND_MUSIC.stop()
                    WIN_MUSIC.play()
                    draw_winner_red(winner_text)
                
                if red_health <= 0:
                    BACKGROUND_MUSIC.stop()
                    WIN_MUSIC.play()
                    draw_winner_yellow(winner_text)

                if yellow_health <= 0 and red_health <= 0:
                    BACKGROUND_MUSIC.stop()
                    WIN_MUSIC.play()
                    draw_winner_green(winner_text)
                break
            
        if game_active:    
            keys_pressed = pygame.key.get_pressed()
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_movement(keys_pressed, red)

            handle_bullets(yellow_bullets, red_bullets, yellow, red)

            draw_window(red, yellow, red_bullets, yellow_bullets,red_health, yellow_health)
            
        else:
            SCREEN.fill(MENU_BLUE)
            
            top_menu_text = HEALTH_FONT.render("Welcome to SPACE BATTLE" , 1, MENU_WHITE)
            top_menu_text_rect = top_menu_text.get_rect(center = (WIDTH // 2, 40))
            SCREEN.blit(top_menu_text, top_menu_text_rect)

            SCREEN.blit(RED_SPACESHIP_ZOOM, RED_SPACESHIP_RECT)
            SCREEN.blit(YELLOW_SPACESHIP_ZOOM, YELLOW_SPACESHIP_RECT)
            
            bottom_menu_text = HEALTH_FONT.render("Press SPACEBAR to start the game" , 1, MENU_WHITE)
            bottom_menu_text_rect = bottom_menu_text.get_rect(center = (WIDTH // 2, HEIGHT - 40))
            SCREEN.blit(bottom_menu_text, bottom_menu_text_rect)
    
        pygame.display.flip()
        clock.tick(FPS)
    
main()
