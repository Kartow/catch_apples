import pygame
from sys import exit
from random import randint

def display_score():
    score_surf = score_font.render(f'Score: {score}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center = (400, 60))
    screen.blit(score_surf, score_rect)

def menu_score():
    menu_surf = menu_font.render(f'Your score: {score}', False, (255, 255, 255))
    menu_rect = menu_surf.get_rect(center = (400, 30))
    screen.blit(menu_surf, menu_rect)

def display_best(a):
    best_surf = score_font.render(f'Best score: {best_score}', False, (132, 222, 165))
    if a == 'koniec':
        best_rect = best_surf.get_rect(center = (400, 80))
    else:
        best_rect = best_surf.get_rect(center = (400, 100))
    screen.blit(best_surf, best_rect)

def apples_movement(a_list):
    global game_state, score, best_score

    if a_list:
        for a_rect in a_list:
            if a_rect.colliderect(player_rect):
                a_list.remove(a_rect)
                score += 1
            a_rect.y += 3
            screen.blit(apple_surf, a_rect)
            if a_rect.bottom > 360:
                game_state = 2

        return a_list
    else:
        return []

def golden_apples_movement(ga_list):
    global score

    if ga_list:
        for ga_rect in ga_list:
            if ga_rect.colliderect(player_rect):
                ga_list.remove(ga_rect)
                score += 3
            ga_rect.y += 3
            screen.blit(golden_apple_surf, ga_rect)
            if ga_rect.bottom > 360:
                ga_list.remove(ga_rect)
        
        return ga_list
    else:
        return []

def speed_fall():
    speed_rect.center = (randint(50, 750), -50)

    

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Catch the Apples')
icon_surf = pygame.image.load('graphics/icon.png').convert_alpha()
pygame.display.set_icon(icon_surf)
clock = pygame.time.Clock()
score_font = pygame.font.Font('font/Pixeltype.ttf', 60)
menu_font = pygame.font.Font('font/Pixeltype.ttf', 80)
title_font = pygame.font.Font('font/Pixeltype.ttf', 110)

game_state = 0
#0 - start, 1 - gra, 2 - przegrales

aaa = 0

start_time = 0
current_time = 0
    
score = 0

speed = 8

is_speed = False
speed_time_start = -5000

with open('best_score.txt', 'r') as best_score_file:
    best_score = int(best_score_file.read())

move_left = False
move_right = False


#tytuł
title_surf = title_font.render('Catch the Apples', False, (255, 255, 255))
title_rect = title_surf.get_rect(center = (400, 40))

#instrukcje
instruction_surf = menu_font.render('Press SPACE to play', False, (255, 255, 255))
instruction_rect = instruction_surf.get_rect(center = (400, 350))

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

player_menu_surf = pygame.image.load('graphics/steve.png').convert_alpha()
player_menu_surf = pygame.transform.scale_by(player_menu_surf, 0.4)
player_menu_rect = player_menu_surf.get_rect(center = (400, 200))

#speed_boost
speed_surf = pygame.image.load('graphics/speed.png').convert_alpha()
speed_surf = pygame.transform.scale_by(speed_surf, 0.3)
speed_rect = speed_surf.get_rect(center = (0, -50))

#jablko
apple_surf = pygame.image.load('graphics/apple.png').convert_alpha()
apple_surf = pygame.transform.scale_by(apple_surf, 0.3)

apple_menu_surf = pygame.image.load('graphics/apple.png').convert_alpha()
apple_menu_surf = pygame.transform.rotozoom(apple_menu_surf, 30, 0.7)
apple_menu_rect = apple_menu_surf.get_rect(center = (500, 200))

golden_apple_surf = pygame.image.load('graphics/golden_apple.png').convert_alpha()
golden_apple_surf = pygame.transform.scale_by(golden_apple_surf, 0.3)

gapple_menu_surf = pygame.image.load('graphics/golden_apple.png').convert_alpha()
gapple_menu_surf = pygame.transform.rotozoom(gapple_menu_surf, 330, 0.7)
gapple_menu_rect = gapple_menu_surf.get_rect(center = (300, 200))

apple_rect_list = []
golden_apple_rect_list = []

apple_timer_interval = 2000
apple_timer = pygame.USEREVENT + 1
pygame.time.set_timer(apple_timer, apple_timer_interval)

golden_apple_timer = pygame.USEREVENT + 2
pygame.time.set_timer(golden_apple_timer, 5000)

speed_timer = pygame.USEREVENT + 3
pygame.time.set_timer(speed_timer, 5000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('best_score.txt','w') as best_score_file:
                best_score_file.write(str(best_score))
            pygame.quit()
            exit()
        if game_state == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_s:
                    is_speed = True
                    speed_fall()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 1
                score = 0
                speed = 8
                start_time = current_time
                apple_timer_interval = 2000
                apple_rect_list = []
                golden_apple_rect_list = []
                move_right = False
                move_left = False
                player_rect.midbottom = (400, 360)

        if event.type == apple_timer and game_state == 1:
            apple_rect_list.append(apple_surf.get_rect(center = (randint(50, 750), -50)))
            apple_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(apple_timer, apple_timer_interval)
        
        if event.type == golden_apple_timer and game_state == 1:
            if randint(1, 5) == 1:
                golden_apple_rect_list.append(golden_apple_surf.get_rect(center = (randint(50, 750), -50)))
        
        if event.type == speed_timer and game_state == 1:
            if randint(1, 10) == 1:
                is_speed = True
                speed_fall()

    if game_state == 1:
        #generuje ziemie i niebo
        screen.blit(sky_surf,sky_rect)
        screen.blit(ground_surf,ground_rect)

        #generuje gracza
        screen.blit(player_surf,player_rect)

        apple_timer_interval = 2000 - round((current_time - start_time) / 50)
        if apple_timer_interval < 800:
            apple_timer_interval = 800
        
        apple_rect_list = apples_movement(apple_rect_list)
        golden_apple_rect_list = golden_apples_movement(golden_apple_rect_list)

        #spadanie speed boosta
        if is_speed and speed_rect.bottom < 360:
            screen.blit(speed_surf, speed_rect)
            speed_rect.y += 3
            if speed_rect.colliderect(player_rect):
                speed_time_start = current_time
                is_speed = False
        if current_time - speed_time_start < 5000:
            speed = 15
        else:
            speed = 8
        
        #poruszanie gracza
        if move_right and player_rect.right <= 800:
            player_rect.x += speed
        if move_left and player_rect.left >= 0:
            player_rect.x -= speed
        
        display_score()
    elif game_state == 2:
        screen.fill((34, 122, 65))
        screen.blit(player_menu_surf, player_menu_rect)
        screen.blit(instruction_surf, instruction_rect)
        menu_score()
        display_best('koniec')
    else:
        screen.fill((32, 122, 65))
        screen.blit(player_menu_surf, player_menu_rect)
        screen.blit(apple_menu_surf, apple_menu_rect)
        screen.blit(gapple_menu_surf, gapple_menu_rect)
        screen.blit(instruction_surf, instruction_rect)
        screen.blit(title_surf, title_rect)
        display_best('menu')

    current_time = pygame.time.get_ticks()

    if score > best_score:
        best_score = score

    pygame.display.update()
    clock.tick(60)
