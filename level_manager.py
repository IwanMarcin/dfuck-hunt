class LevelManager:
    def __init__(self):
        self.level = 1
        self.score_for_next = 10

    def update(self, hits):
        if hits >= self.level * self.score_for_next and self.level < 50:
            self.level += 1

    def get_spawn_chance(self):
        base = 0.7
        if 10 <= self.level < 20:
            return base + 0.05
        elif 30 <= self.level < 40:
            return base + 0.10
        elif 40 <= self.level <= 50:
            return base + 0.20
        return base

    def get_speed_multiplier(self):
        if 20 <= self.level < 30:
            return 1.10
        elif 30 <= self.level < 40:
            return 1.05
        elif 40 <= self.level <= 50:
            return 1.10
        return 1.0

    def get_poop_damage(self):
        base = 5
        if 10 <= self.level < 20:
            return base + 5
        elif 20 <= self.level < 30:
            return base + 10
        elif 40 <= self.level <= 50:
            return base + 20
        return base

    def get_armed_chance(self):
        return min(0.3 + self.level * 0.01, 0.6)
