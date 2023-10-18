import os


class score():

    def __init__(self):
        self.scorefile = os.path.join(os.path.dirname(__file__), ".highscores")
        self.level = 1
        self.score = 0
        self.lines = 0

        self.combo = 1  # Combo will increase when you clear lines with several tetrominos in a row


    def load_score(self):
        """ Returns the highest score, or 0 if no one has scored yet """
        try:
            with open(self.scorefile) as file:
                scores = sorted([int(score.strip())
                                for score in file.readlines()
                                if score.strip().isdigit()], reverse=True)
        except IOError:
            scores = []

        return scores[0] if scores else 0

    def write_score(self, score):
        """
        Writes score to file.
        """
        assert str(score).isdigit()
        with open(self.scorefile, 'a') as file:
            file.write("{}\n".format(score))

    def mark_score(self, lines_cleared):
        '''Mark score for every line cleared'''
        
        self.lines += lines_cleared

        self.score += 100 * (lines_cleared**2) * self.combo

        if self.lines >= self.level * 10:
            self.level += 1

        self.combo = self.combo + 1 if lines_cleared else 1

    def reset_combo(self):
        self.combo = 1

