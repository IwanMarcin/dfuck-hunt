from sounds import next_level

class LevelManager:
    def __init__(self):
        self.level = 0
        self.score_for_next = 10

    def update(self, hits):
        if hits >= self.score_for_next:
            self.level += 1
            next_level()
            self.score_for_next += 10

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
        return 1.0 + self.level * 0.01

    def get_poop_damage(self):
        base = 5
        if 10 <= self.level < 20:
            return base + 5
        elif 20 <= self.level < 30:
            return base + 10
        elif 40 <= self.level:
            return base + 20
        return base

    def get_armed_chance(self):
        return min(0.3 + self.level * 0.01, 0.6)
