import settings
import discord
from discord.ext import commands
import aiosqlite
from request import get_game, calculer_kda
from Joueur import Joueur

player_list = ['luv u too', 'PufferFishZ', 'BetterCallPlante', 'Dragon Sournois', 'airwick511111']


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command()
    async def add_game(ctx, game_id):
        connexion = await aiosqlite.connect('Players.db')
        cursor = await connexion.cursor()

        game_dict = get_game(game_id)
                
        for participants in game_dict['info']['participants']:
            if participants['summonerName'] in player_list:
                summoner_name = participants['summonerName']
                kill = participants['kills']
                death = participants['deaths']
                assist = participants['assists']
                champion = participants['championName']

                if await exists_in_database(summoner_name):
                    await cursor.execute("""SELECT * FROM players WHERE summoner_name = ?""", (summoner_name,))
                    player = await cursor.fetchone()
                    joueur = Joueur(player[0], player[1], player[2], player[3], player[5])
                    joueur.ajouter_stats(kill, death, assist)
                    joueur.ajouter_champion(champion)

                    await cursor.execute("""UPDATE players SET kill = ?, death = ?, assist = ?, kda = ?, champions = ? WHERE summoner_name = ?""",
                                          (joueur.kill, joueur.death, joueur.assist, joueur.kda, ' ,'. join(champ for champ in joueur.champions), joueur.summoner_name))
                    await connexion.commit()
                    print(joueur)
                else:
                    joueur = Joueur(summoner_name, kill, death, assist, champion)
                    await cursor.execute("""INSERT INTO players VALUES (?, ?, ?, ?, ?, ?)""", (joueur.summoner_name, joueur.kill, joueur.death, joueur.assist, joueur.kda, ' ,'. join(champ for champ in joueur.champions)))
                    await connexion.commit()
                    print(f'Added {summoner_name} to the database, kill: {kill}, death: {death}, assist: {assist}, kda: {joueur.kda}, champions: {joueur.champions}')
        
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

        bot.db = await aiosqlite.connect('Players.db')
        cursor = await bot.db.cursor()

        await cursor.execute("""CREATE TABLE IF NOT EXISTS players (summoner_name text, kill int, death int, assist int, kda float, champions text)""")
        await bot.db.commit()

        
    bot.run(settings.DISCORD_TOKEN)

async def exists_in_database(player_name):
    connexion = await aiosqlite.connect('Players.db')
    cursor = await connexion.cursor()

    await cursor.execute("""SELECT summoner_name FROM players WHERE summoner_name = ?""", (player_name,))
    player = await cursor.fetchone()

    if player is None:
        return False
    return True
    

if __name__ == '__main__':
    run()