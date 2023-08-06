

class Joueur:
    
    def __init__(self, summoner_name, kill, death, assist, champion):
        self.summoner_name = summoner_name
        self.kill = kill
        self.death = death
        self.assist = assist
        self.kda = round((self.kill + self.assist) / self.death, 2)
        self.champions = []
        self.champions.append(champion)

    def calculer_kda(self):
        self.kda = round((self.kill + self.assist) / self.death, 2)

    def ajouter_stats(self, kill, death, assist):
        self.kill += kill
        self.death += death
        self.assist += assist
        self.calculer_kda()

    def ajouter_champion(self, champion):
        self.champions.append(champion)

    def __repr__(self):
        return f'{self.summoner_name} : {self.kill} / {self.death} / {self.assist} / {self.kda} / {self.champions}'
