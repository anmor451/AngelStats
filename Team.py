class Team:
    def __init__(self):
        self.win = 0
        self.lose = 0
        self.winrate = 0
        self.members = ['Bouillon' ,'TR0PHEE', 'MTC Paradox', 'Mister Wubz', 'Jean Francois', 'Sac De Papier', 'Bengadon']

    def calculer_winrate(self):
        self.winrate = round(self.win / (self.win + self.lose), 2)

    def update_score(self, win):
        if win:
            self.win += 1
        else:
            self.lose += 1
        self.calculer_winrate()