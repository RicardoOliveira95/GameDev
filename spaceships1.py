import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
PAUSE_FONT = pygame.font.SysFont('comicsans', 80)
MENU_FONT = pygame.font.SysFont('comicsans', 60)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_flinch_timer, yellow_flinch_timer, is_paused):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    if red_flinch_timer > 0:
        red_flinch_timer -= 1
    if yellow_flinch_timer > 0:
        yellow_flinch_timer -= 1

    if red_flinch_timer % 20 < 10:  # Flashing effect for flinching
        WIN.blit(RED_SPACESHIP, (red.x, red.y))
    if yellow_flinch_timer % 20 < 10:
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    if is_paused:
        pause_text = PAUSE_FONT.render("PAUSED", 1, WHITE)
        WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width() /
                              2, HEIGHT/2 - pause_text.get_height()/2))

    pygame.display.update()

    return red_flinch_timer, yellow_flinch_timer


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < BORDER.x:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

def red_handle_bot_movement(red, yellow, red_bullets):
    # Bot-controlled player
    direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    if direction == 'UP' and red.y - VEL > 0:
        red.y -= VEL
    if direction == 'DOWN' and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL
    if direction == 'LEFT' and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if direction == 'RIGHT' and red.x + VEL + red.width < WIDTH:
        red.x += VEL

    # Bot shooting
    if len(red_bullets) < MAX_BULLETS:
        bullet = pygame.Rect(
            red.x, red.y + red.height // 2 - 2, 10, 5)
        red_bullets.append(bullet)

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


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_menu():
    WIN.fill(BLACK)
    title_text = MENU_FONT.render("Game Menu", 1, WHITE)
    singleplayer_text = MENU_FONT.render("1 Player", 1, WHITE)
    multiplayer_text = MENU_FONT.render("2 Players", 1, WHITE)
    quit_text = MENU_FONT.render("(Q) Quit", 1, WHITE)

    title_pos = (WIDTH/2 - title_text.get_width()/2, HEIGHT/4 - title_text.get_height()/2)
    singleplayer_pos = (WIDTH/2 - singleplayer_text.get_width()/2, HEIGHT/2 - singleplayer_text.get_height()/2)
    multiplayer_pos = (WIDTH/2 - multiplayer_text.get_width()/2, HEIGHT/2 + multiplayer_text.get_height())
    quit_pos = (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + multiplayer_text.get_height()*2)

    WIN.blit(title_text, title_pos)
    WIN.blit(singleplayer_text, singleplayer_pos)
    WIN.blit(multiplayer_text, multiplayer_pos)
    WIN.blit(quit_text, quit_pos)

    pygame.display.update()

def single_player_game():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    red_flinch_timer = 0
    yellow_flinch_timer = 0

    clock = pygame.time.Clock()
    is_paused = False

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_p:  # Pause the game
                    is_paused = not is_paused

                if event.key == pygame.K_q:  # Quit the game
                    run = False
                    pygame.quit()

            if event.type == RED_HIT:
                if red_flinch_timer == 0:  # Only apply flinch effect if not already flinching
                    red_health -= 1
                    red_flinch_timer = FPS * 2  # Set the flinch timer to 2 seconds

            if event.type == YELLOW_HIT:
                if yellow_flinch_timer == 0:
                    yellow_health -= 1
                    yellow_flinch_timer = FPS * 2

        if red_health <= 0:
            draw_winner("Yellow Wins!")
            break

        if yellow_health <= 0:
            draw_winner("Red Wins!")
            break

        if not is_paused:
            keys_pressed = pygame.key.get_pressed()
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_bot_movement(red, yellow, red_bullets)

            handle_bullets(yellow_bullets, red_bullets, yellow, red)

        red_flinch_timer, yellow_flinch_timer = draw_window(
            red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_flinch_timer, yellow_flinch_timer, is_paused)

def multiplayer_game():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    red_flinch_timer = 0
    yellow_flinch_timer = 0

    clock = pygame.time.Clock()
    is_paused = False

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_p:  # Pause the game
                    is_paused = not is_paused

                if event.key == pygame.K_q:  # Quit the game
                    run = False
                    pygame.quit()

            if event.type == RED_HIT:
                if red_flinch_timer == 0:  # Only apply flinch effect if not already flinching
                    red_health -= 1
                    red_flinch_timer = FPS * 2  # Set the flinch timer to 2 seconds

            if event.type == YELLOW_HIT:
                if yellow_flinch_timer == 0:
                    yellow_health -= 1
                    yellow_flinch_timer = FPS * 2

        if red_health <= 0:
            draw_winner("Yellow Wins!")
            break

        if yellow_health <= 0:
            draw_winner("Red Wins!")
            break

        if not is_paused:
            keys_pressed = pygame.key.get_pressed()
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_movement(keys_pressed, red)
            handle_bullets(yellow_bullets, red_bullets, yellow, red)

        red_flinch_timer, yellow_flinch_timer = draw_window(
            red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_flinch_timer, yellow_flinch_timer, is_paused)


def main():
    clock = pygame.time.Clock()
    run = True
    intro = True

    while run:
        clock.tick(FPS)

        if intro:
            draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if intro:
                    if event.key == pygame.K_1:  # 1 Player
                        intro = False
                        print("1 Player Selected")
                        single_player_game()

                    if event.key == pygame.K_2:  # 2 Players
                        intro = False
                        print("2 Players Selected")
                        multiplayer_game()

                    if event.key == pygame.K_q:  # Quit
                        run = False
                        pygame.quit()

if __name__ == "__main__":
    main()
