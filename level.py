import random
from plateforme import spawnPlateform, activePlates
from ennemies import Enemy
from constants import *


def create_enemy_on_platform(plateform, enemy_img):
    x_min = plateform.x
    x_max = plateform.x + plateform.image.get_width()
    platform_params = [x_min, x_max, plateform.y]
    enemy = Enemy(enemy_img, platform_params)
    enemy.rect.bottom = plateform.y
    enemy.platform_sprite = plateform
    plateform.enemy = enemy
    return enemy


def init_platforms_and_enemies(enemy_img, score_obj):
    activePlates.clear()
    enemies = []
    y = HEIGHT - 80

    while y > -HEIGHT:
        for k in range(plateforme_par_ligne):
            p = spawnPlateform()
            p.y = y
            try:
                w = p.image.get_width()
            except:
                w = 100
            p.x = random.randint(0, WIDTH - w)

            spawn_prob = score_obj.enemy_spawn_prob()
            if spawn_prob > 0 and random.random() < spawn_prob:
                e = create_enemy_on_platform(p, enemy_img)
                enemies.append(e)
            else:
                p.enemy = None

        y -= GAP_Y
    return enemies


def recycle_platforms_and_enemies(enemies, enemy_img, score_obj):
    if not activePlates:
        return enemies

    min_y = min(p.y for p in activePlates)
    for p in activePlates:
        if p.y > HEIGHT + 50:
            p.y = min_y - GAP_Y
            try:
                w = p.image.get_width()
            except:
                w = 100
            p.x = random.randint(0, WIDTH - w)
            min_y = p.y

            if p.enemy is not None:
                e = p.enemy
                e.platform_sprite = p
                x_min = p.x
                x_max = p.x + p.image.get_width()
                e.platform = [x_min, x_max, p.y]
                e.rect.bottom = p.y
                e.rect.x = random.randint(x_min, x_max - e.width)
            else:
                spawn_prob = score_obj.enemy_spawn_prob()
                if spawn_prob > 0 and random.random() < spawn_prob:
                    e = create_enemy_on_platform(p, enemy_img)
                    enemies.append(e)
    return enemies