import settings
import discord
from discord.ext import commands
import aiosqlite
from request import get_game
from Joueur import Joueur
from Team import Team

HISTORIQUE_GAMES = []

def calculer_winrate(win, lose):
    return round(win / (win + lose) * 100, 2)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    team = Team()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command()
    async def add_game(ctx, game_id):
        connexion = await aiosqlite.connect('Players.db')
        cursor = await connexion.cursor()

        if ctx.channel.id != settings.CHANNEL_ID:
            print('Ce n\'est pas le bon channel')
            await ctx.channel.purge(limit=1)
            return

        if game_id in HISTORIQUE_GAMES:
            await ctx.send('Cette game a déjà été ajoutée')
            return
        
        HISTORIQUE_GAMES.append(game_id)

        game_dict = get_game(game_id)

        if game_dict is None:
            await ctx.send('Cette game n\'existe pas')
            return
        
        for participants in game_dict['info']['participants']:
            if participants['summonerName'] in team.members:
                summoner_name = participants['summonerName']
                kill = participants['kills']
                death = participants['deaths']
                assist = participants['assists']
                champion = participants['championName']
                win = participants['win']
                print(f'{summoner_name} : {kill} / {death} / {assist} / {champion} / win = {win}')

                if await exists_in_database(summoner_name):
                    await cursor.execute("""SELECT * FROM players WHERE summoner_name = ?""", (summoner_name,))
                    player = await cursor.fetchone()
                    print(player)
                    joueur = Joueur(player[0], player[1], player[2], player[3], player[5], player[6], player[7], player[8])
                    joueur.ajouter_stats(kill, death, assist, win)
                    joueur.ajouter_champion(champion)
                    print(joueur)
                    await cursor.execute("""UPDATE players SET kill = ?, death = ?, assist = ?, kda = ?, win = ?, lose = ?, jouer = ?, champions = ? WHERE summoner_name = ?""",
                                          (joueur.kill, joueur.death, joueur.assist, joueur.kda, joueur.win, joueur.lose, joueur.jouer, ', '. join(champ for champ in joueur.champions), joueur.summoner_name))
                    await connexion.commit()
                    print(joueur)
                else:
                    print(win)
                    real_win = 0
                    real_lose = 0
                    if win:
                        real_win = 1
                    else:
                        real_lose += 1
                    joueur = Joueur(summoner_name, kill, death, assist, real_win, real_lose, champion)
                    await cursor.execute("""INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (joueur.summoner_name, joueur.kill, joueur.death, joueur.assist, joueur.kda, joueur.win, joueur.lose, ', '. join(champ for champ in joueur.champions), joueur.jouer))
                    await connexion.commit()
                    print(f'Added {summoner_name} to the database, kill: {kill}, death: {death}, assist: {assist}, kda: {joueur.kda}, win: {joueur.win}, lose: {joueur.lose} champions: {joueur.champions}, jouer: {joueur.jouer}')

        if win is not None:
            team.update_score(win)
        
        await cursor.execute("""SELECT * FROM games""")
        game = await cursor.fetchone()
        if game is not None:
            await cursor.execute("""UPDATE games SET win = ?, lose = ?, winrate = ?""", (team.win, team.lose, team.winrate))
        else:
            await cursor.execute("""INSERT INTO games VALUES (?, ?, ?)""", (team.win, team.lose, team.winrate))
        await connexion.commit()

    @bot.command()
    async def show_stats(ctx):
        if ctx.channel.id != settings.BOT_COMMAND_CHANNEL_ID:
            return
        channel = bot.get_channel(settings.STATS_CHANNEL_ID)
        message = "Voici les stats des anges !! \n"
        connexion = await aiosqlite.connect('Players.db')
        cursor = await connexion.cursor()

        await channel.purge(limit=1)

        await cursor.execute("""SELECT * FROM games""")
        game = await cursor.fetchone()
        message += f'Win: {game[0]}, Lose: {game[1]}, Winrate: {game[2]}' + '%\n'

        await cursor.execute("""SELECT * FROM players""")
        players = await cursor.fetchall()
        for player in players:
            message += '------------------------' + '\n'
            message += f'{player[0]} / kills : {player[1]} / deaths = {player[2]} / assists = {player[3]} / \nkda = {player[4]} / parties jouées = {player[8]}\n champions jouées = {player[7]}\n'

        await channel.send(message)


    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

        bot.db = await aiosqlite.connect('Players.db')
        cursor = await bot.db.cursor()

        await cursor.execute("""CREATE TABLE IF NOT EXISTS players (summoner_name text, kill int, death int, assist int, kda float, win int, lose int, jouer int, champions text)""")
        await bot.db.commit()

        await cursor.execute(""" CREATE TABLE IF NOT EXISTS games (win int, lose int, winrate float)""")
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