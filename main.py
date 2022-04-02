import pygame, os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1800, 1000
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 45, 55

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

SCORE_TEXT = pygame.font.SysFont("comicsans", 40)
WINNER_TEXT = pygame.font.SysFont("comicsans", 150)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)) , 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)) , 270)

FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))

BORDER = pygame.Rect((WIDTH//2 - 5), 0, 10, HEIGHT)     


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_score, red_score, winner_text):
    WIN.blit(BACKGROUND, (0, 0))

    yellow_score_text = SCORE_TEXT.render("Score: " + str(yellow_score), 1, WHITE)
    red_score_text = SCORE_TEXT.render("Score: " + str(red_score), 1, WHITE)
    WIN.blit(yellow_score_text, (10, 10))
    WIN.blit(red_score_text, (WIDTH - red_score_text.get_width() - 10, 10))

    pygame.draw.rect(WIN, BLACK, BORDER)
    #pygame.draw.rect(WIN, YELLOW, yellow)
    #pygame.draw.rect(WIN, RED, red)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)    

    if winner_text != "":
        winner_text = WINNER_TEXT.render(winner_text, 1, WHITE)
        WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))

    pygame.display.update()


def bullet_handle(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x + 10 > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def yellow_movement_handle(keys, yellow):
    if keys[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys[pygame.K_s] and yellow.y + SPACESHIP_HEIGHT < HEIGHT: # DOWN
        yellow.y += VEL    
    if keys[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys[pygame.K_d] and yellow.x + VEL + SPACESHIP_WIDTH < BORDER.x: # RIGHT
        yellow.x += VEL


def red_movement_handle(keys, red):
    if keys[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys[pygame.K_DOWN] and red.y + VEL + SPACESHIP_HEIGHT < HEIGHT: # DOWN
        red.y += VEL    
    if keys[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if keys[pygame.K_RIGHT] and red.x + SPACESHIP_WIDTH < WIDTH: # RIGHT
        red.x += VEL


def main():
    yellow = pygame.Rect(200, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(WIDTH - 200 - SPACESHIP_WIDTH, HEIGHT - SPACESHIP_HEIGHT - 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_score = 10
    red_score = 10

    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH - 15, yellow.y + SPACESHIP_HEIGHT//2, 10, 5)
                    yellow_bullets.append(bullet)
                    FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + 5, red.y + SPACESHIP_HEIGHT//2, 10, 5)
                    red_bullets.append(bullet)
                    FIRE_SOUND.play()                    

            if event.type == YELLOW_HIT:
                yellow_score -= 1
                HIT_SOUND.play()

            if event.type == RED_HIT:
                red_score -= 1
                HIT_SOUND.play()

        winner = ""
        if yellow_score <= 0:
            winner = "Red Wins!"
        elif red_score <= 0:
            winner = "Yellow Wins!"

        if winner != "":
            draw_window(yellow, red, yellow_bullets, red_bullets, yellow_score, red_score, winner)
            pygame.time.delay(5000)
            break


        keys_pressed = pygame.key.get_pressed()
        
        yellow_movement_handle(keys_pressed, yellow)
        red_movement_handle(keys_pressed, red)
        bullet_handle(yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_score, red_score, winner)
        

    return


if __name__ == "__main__":
    while True:
        main()
