import pygame
import pytest

from player import *
@pytest.fixture
#Est un décorateur utilisé par pytest. Son rôle est très important : créer et fournir automatiquement des objets prêts à l’emploi pour les tests.

def player():
    pygame.init()
    fake_image = pygame.Surface((10, 10))
    return Player(fake_image)


def test_move_left(player):
    start_x = player.x
    player.left()
    assert player.x == start_x - player.player_x_change

def test_move_right(player):
    start_x = player.x
    player.right()
    assert player.x == start_x + player.player_x_change

def test_jump_vy_flag(player):
    player.jump()
    assert player.vy == -15
    assert player.is_jumping is True
def test_jump_cannot_double_jump(player):
    player.jump()
    first_vy = player.vy
    player.jump()
    assert player.vy == first_vy
    assert player.is_jumping is True