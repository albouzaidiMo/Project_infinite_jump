class Score:
    def __init__(self):
        self.value = 0

    def reset(self):
        self.value = 0

    def add(self, amount=1):
        self.value += amount

    def can_spawn_enemies(self):
        return self.value > 500
#probabilité dépend du score
    def enemy_spawn_prob(self):
        if not self.can_spawn_enemies():
            return 0
        return min(0.9, self.value / 400)