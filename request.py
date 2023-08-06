import requests
import settings

url = "https://americas.api.riotgames.com/lol/match/v5/matches/"

def get_game(game_id):
    response = requests.get(url + 'NA1_' + game_id + "?api_key=" + settings.RIOT_TOKEN)

    if response.status_code == 401:
        print("Unauthorized")
        return None
    elif response.status_code == 404:
        print("Data not Found")
        return None
    elif response.status_code == 500:
        print("Internal Server Error")
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        return None


if __name__ == "__main__":
    print(get_game('4737645222'))


    