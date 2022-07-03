import pygame
from pygame.locals import *
import random
from sys import exit
pygame.font.init()

window_size = (600, 600) #tamanho da janela
pixel_size = 10 # tamanho do pixel do jogo 

points = 0
record = 0
font = pygame.font.SysFont("Arial", 15, bold=True, italic=False)
message = ""
message2 = ""

def collision(pos1, pos2):
    return pos1 == pos2

def off_limits(pos):
    if 0 <= pos[0]< window_size[0] and 0 <= pos[1] < window_size[1]:
        return False
    else:
        return True

def random_on_grid():
    x = random.randint(0, window_size[0])
    y = random.randint(0, window_size[1])
    return x // pixel_size * pixel_size, y // pixel_size * pixel_size 

pygame.init()

pygame.mixer.music.set_volume(0.1)
collision_sound = pygame.mixer.Sound('tomi.mp3')
points_10 = pygame.mixer.Sound('elegosta.mp3')
lost = pygame.mixer.Sound('cavalo.mp3')

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake")

snake_position = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((pixel_size, pixel_size))
snake_surface.fill((0, 0, 0))
snake_direction = K_LEFT

def restart_game():
    global snake_position
    global apple_position
    global snake_direction
    snake_position = [(250, 50), (260, 50), (270, 50)]
    snake_direction = K_LEFT
    apple_position = random_on_grid()
    

apple_surface = pygame.Surface((pixel_size, pixel_size))
apple_surface.fill((255, 0, 0))
apple_position = random_on_grid()

while True:
    pygame.time.Clock().tick(15)
    screen.fill((139, 150, 110))
    message = f'Score: {points}'
    message2 = f'Record: {record}'
    text_formatted = font.render(message, True, (0,0,0))
    text_formatted2 = font.render(message2, True, (0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key

    screen.blit(apple_surface, apple_position)

    if collision(apple_position, snake_position[0]):
        snake_position.append((-10, -10))
        apple_position = random_on_grid()
        collision_sound.play()
        points += 1
        
        if points > record:
            record = points
        if (points % 10) == 0:
            points_10.play()
        if (points % 10) == 0:
            collision_sound.stop()

    for pos in snake_position:
        screen.blit(snake_surface, pos)

    for i in range(len(snake_position)-1 , 0, -1):
        if collision(snake_position[0], snake_position[i]):
            points = 0
            lost.play()
            restart_game()
        snake_position[i] = snake_position[i-1]
        

    if off_limits(snake_position[0]):
        points = 0
        lost.play()
        restart_game()

    if snake_direction == K_UP:
        snake_position[0] = (snake_position[0][0], snake_position[0][1] - pixel_size)
    elif snake_direction == K_DOWN:
        snake_position[0] = (snake_position[0][0], snake_position[0][1] + pixel_size)
    elif snake_direction == K_LEFT:
        snake_position[0] = (snake_position[0][0] - pixel_size, snake_position[0][1] )
    elif snake_direction == K_RIGHT:
        snake_position[0] = (snake_position[0][0] + pixel_size, snake_position[0][1] )

    screen.blit(text_formatted, (121, 10))
    screen.blit(text_formatted2, (416, 10))

    pygame.display.update()
    