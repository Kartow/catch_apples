import pygame
from sys import exit
from random import randint

def apples_movement(a_list):
    global game_state

    if a_list:
        for a_rect in a_list:
            a_rect.y += 3
            screen.blit(apple_surf, a_rect)

            if a_rect.bottom > 360:
                game_state = False
        
        return a_list
    else:
        return []
    
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Catch the Apples')
clock = pygame.time.Clock()

game_state = True

move_left = False
move_right = False

#ziemia
ground_surf = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surf.get_rect(bottomleft = (0, 400))

#niebo
sky_surf = pygame.image.load('graphics/sky.png').convert()
sky_rect = sky_surf.get_rect(topleft = (0,0))

#steve
player_surf = pygame.image.load('graphics/steve.png').convert_alpha()
player_surf = pygame.transform.scale_by(player_surf, 0.2)
player_rect = player_surf.get_rect(midbottom = (400, 360))

#jablko
apple_surf = pygame.image.load('graphics/apple.png').convert_alpha()
apple_surf = pygame.transform.scale_by(apple_surf, 0.3)

apple_rect_list = []

apple_timer = pygame.USEREVENT + 1
pygame.time.set_timer(apple_timer, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False

        if event.type == apple_timer and game_state:
            apple_rect_list.append(apple_surf.get_rect(center = (randint(50, 750), -50)))

    if game_state:

        #generuje ziemie i niebo
        screen.blit(sky_surf,sky_rect)
        screen.blit(ground_surf,ground_rect)

        #generuje gracza
        screen.blit(player_surf,player_rect)
        
        apple_rect_list = apples_movement(apple_rect_list)
        
        #poruszanie gracza
        if move_right and player_rect.right <= 800:
            player_rect.x += 8
        if move_left and player_rect.left >= 0:
            player_rect.x -= 8

    pygame.display.update()
    clock.tick(60)