class Joueur:
    
    def __init__(self, summoner_name, kill, death, assist, win, lose, champion):
        self.summoner_name = summoner_name
        self.kill = kill
        self.death = death
        self.assist = assist
        self.kda = round((self.kill + self.assist) / self.death, 2)
        self.champions = []
        self.champions.append(champion)
        self.win = win
        self.lose = lose

    def calculer_kda(self):
        self.kda = round((self.kill + self.assist) / self.death, 2)

    def ajouter_stats(self, kill, death, assist, win):
        self.kill += kill
        self.death += death
        self.assist += assist
        self.calculer_kda()

        if win:
            self.win += 1
        else:
            self.lose += 1

    def ajouter_champion(self, champion):
        self.champions.append(champion)

    def __repr__(self):
        return f'{self.summoner_name} : {self.kill} / {self.death} / {self.assist} / {self.kda} / {self.champions}'
