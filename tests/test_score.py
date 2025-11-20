# test_score.py
import pytest
from score import Score


@pytest.fixture
def score():
    return Score()


def test_initial_value_is_zero(score):
    assert score.value == 0


def test_add_default_is_one(score):
    score.add()
    assert score.value == 1
    score.add()
    assert score.value == 2


def test_add_custom_amount(score):
    score.add(10)
    assert score.value == 10
    score.add(5)
    assert score.value == 15


def test_reset(score):
    score.add(50)
    assert score.value == 50
    score.reset()
    assert score.value == 0


def test_can_spawn_enemies_threshold(score):
    # en dessous ou égal à 500 → False
    score.value = 500
    assert score.can_spawn_enemies() is False

    # au-dessus de 500 → True
    score.value = 501
    assert score.can_spawn_enemies() is True


def test_enemy_spawn_prob_zero_below_threshold(score):
    score.value = 0
    assert score.enemy_spawn_prob() == 0

    score.value = 500
    assert score.enemy_spawn_prob() == 0




def test_enemy_spawn_prob_capped_at_0_9(score):
    # valeur très grande -> devrait être capée à 0.9
    score.value = 10000
    assert score.enemy_spawn_prob() == 0.9