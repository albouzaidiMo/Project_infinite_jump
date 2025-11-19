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
    start_x = player.rect.x
    player.left()
    assert player.rect.x == start_x - player.player_x_change
def test_move_right(player):
    start_x = player.rect.x
    player.right()
    assert player.rect.x == start_x + player.player_x_change

def test_first_jump(player):
    player.jump()
    assert player.vy == -20
    assert player.is_jumping[0] is True
    assert player.is_jumping[1] is False


def test_second_jump(player):
    player.jump()
    player.jump()
    assert player.vy == -15
    assert player.is_jumping[1] is True

def test_no_third_jump(player):
    player.jump()
    player.jump()
    vy_before = player.vy
    player.jump()
    assert player.vy == vy_before
def test_frontiere_right_wrap(player):
    player.rect.left = 801
    player.frontiere()
    assert player.rect.right == 0


def test_frontiere_left_wrap(player):
    player.rect.right = -1
    player.frontiere()
    assert player.rect.left == 800