class Multiplier:
    def __init__(self):
        self.combo_streak = 0
        self.combo_multiplier = 1
        self.combo_levels = [1, 2, 4, 8]

    def update(self, hit):
        if hit:
            self.combo_streak += 1
            if self.combo_streak >= 8:
                self.combo_multiplier = 8
            elif self.combo_streak >= 4:
                self.combo_multiplier = 4
            elif self.combo_streak >= 2:
                self.combo_multiplier = 2
        else:
            self.combo_streak = max(0, self.combo_streak - 1)
            if self.combo_multiplier > 1:
                idx = self.combo_levels.index(self.combo_multiplier)
                self.combo_multiplier = self.combo_levels[max(0, idx - 1)]
