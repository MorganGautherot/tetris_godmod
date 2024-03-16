class Score:
    def __init__(self) -> None:
        """
        Initilization of the class score
        """

        self.level = 1
        self.score = 0
        self.lines = 0
        self.combo = 1

    def mark_score(self, lines_cleared: int) -> None:
        """Mark score for every line cleared"""

        self.lines += lines_cleared

        if lines_cleared == 1:
            self.score += 40 * self.level
        if lines_cleared == 2:
            self.score += 100 * self.level
        if lines_cleared == 3:
            self.score += 300 * self.level
        if lines_cleared == 4:
            self.score += 1200 * self.level

        if self.lines >= self.level * 10:
            self.level += 1

        self.combo = self.combo + 1 if lines_cleared else 1

    def reset_combo(self) -> None:
        self.combo = 1
