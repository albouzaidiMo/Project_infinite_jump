from ennemies import *
import pytest
import pygame

global platform_sol, platform_haute, platform_courte, screen1, enemy_1, enemy_2, enemy_3, enemy_4

platform_sol = [ 0 , 800 , 600 ]
platform_haute = [ 250 , 680 , 70 ]
platform_courte = [ 100 , 114 , 200 ]

screen1 = pygame.image.load("assets/enemy.png")
screen1 = pygame.transform.scale(screen1, (52, 33))

enemy_1 = Enemy(screen1, platform_sol)
enemy_1.rect.x = 600

enemy_2 = Enemy(screen1, platform_sol)
enemy_2.rect.x = 4
enemy_2.is_mvt_left = True

enemy_3 = Enemy(screen1, platform_haute)
enemy_3.rect.x = 668

enemy_4 = Enemy(screen1, platform_courte)

def test_random_position_in_platform_with_width():
    
    assert random_position_in_platform_with_width( platform_sol , 40 , 10) [1] == 600
    assert random_position_in_platform_with_width( platform_sol , 40 , 10) [0] in list(range(791))
    assert random_position_in_platform_with_width( platform_sol , 20 , 100) [0] in list(range(701))
    assert random_position_in_platform_with_width( platform_haute , 30 , 10 ) [1] == 70
    assert random_position_in_platform_with_width( platform_haute , 20 , 10) [0] in list(range(250,671))
    assert random_position_in_platform_with_width( platform_haute , 20 , 250) [0] in list(range(250,461))

def test_is_possible_left_right():
    
    assert enemy_1.is_possible_left_right() == [ True , True ]
    assert enemy_2.is_possible_left_right() == [ False , True ]
    assert enemy_3.is_possible_left_right() == [ True , False ]
    assert enemy_4.is_possible_left_right() == [ False , False ]

def test_mouvement_uniforme_in_platform():
    
    enemy_1.mouvement_uniforme_in_platform()
    assert enemy_1.rect.x == 605
    assert enemy_1.is_mvt_left == False
    
    enemy_2.mouvement_uniforme_in_platform()
    assert enemy_2.rect.x == 4
    assert enemy_2.is_mvt_left == False
    
    enemy_3.mouvement_uniforme_in_platform()
    assert enemy_3.rect.x == 668 
    assert enemy_3.is_mvt_left == True
    
    x4 = enemy_4.rect.x
    
    enemy_4.mouvement_uniforme_in_platform()
    assert enemy_4.rect.x == x4
    assert enemy_4.is_mvt_left == True
    
    enemy_4.mouvement_uniforme_in_platform()
    assert enemy_4.rect.x == x4
    assert enemy_4.is_mvt_left == False