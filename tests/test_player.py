# test_player.py
import pytest
import pygame

from player import Player


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def dummy_image():
    return pygame.Surface((21, 36))


@pytest.fixture
def patch_image_load(monkeypatch, dummy_image):
    def fake_load(path):
        return dummy_image.copy()

    monkeypatch.setattr(pygame.image, "load", fake_load)


@pytest.fixture
def player(patch_image_load, dummy_image):
    """Retourne un joueur initialisé avec les patches en place."""
    return Player(dummy_image)


def test_initial_state(player):
    assert player.rect.x == 400
    assert player.rect.y == 540
    assert player.vx == 0
    assert player.vy == 0
    assert player.is_jumping == [False, False]
    assert player.direction == "right"
    assert player.img_act is player.image


def test_jump_and_double_jump(player):
    # premier saut
    player.jump()
    assert player.vy == -20
    assert player.is_jumping == [True, False]

    # deuxième saut (double saut)
    player.jump()
    assert player.vy == -15
    assert player.is_jumping == [True, True]

    # troisième appel : rien ne doit changer
    player.jump()
    assert player.vy == -15
    assert player.is_jumping == [True, True]


def test_update_resets_on_ground(player):
    screen_height = 600
    # on simule un joueur qui tombe déjà
    player.rect.y = 590
    player.vy = 5
    player.is_jumping = [True, True]

    player.update(screen_height)

    # replacé sur le sol
    assert player.rect.y == screen_height - player.height
    assert player.vy == 0
    assert player.is_jumping == [False, False]


def test_left_and_right_change_position_and_direction(player):
    x0 = player.rect.x
    player.left()
    assert player.rect.x == x0 - player.player_x_change
    assert player.direction == "left"

    x1 = player.rect.x
    player.right()
    assert player.rect.x == x1 + player.player_x_change
    assert player.direction == "right"


def test_frontiere_wraps_horizontally(player):
    # sortie par la droite
    player.rect.left = 801
    player.frontiere()
    assert player.rect.right == 0

    # sortie par la gauche
    player.rect.right = -1
    player.frontiere()
    assert player.rect.left == 800


def test_animate_idle_keeps_base_image(player):
    # on met une image courante différente pour vérifier le reset
    player.img_act = pygame.Surface((10, 10))
    player.animate(moving1=False)
    assert player.img_act is player.image


def test_animate_moves_through_frames(player):
    # direction droite
    player.direction = "right"
    old_frame = player.frame
    player.animate(moving1=True)
    assert player.frame > old_frame
    assert player.img_act in player.images_right
    player.direction = "left"
    old_frame = player.frame
    player.animate(moving1=True)
    assert player.frame > old_frame
    assert player.img_act in player.images_left