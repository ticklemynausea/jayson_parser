# this demo takes the jayson string below

from lib.parser import Parser

data = r"""
{
    "players": [
        { "name": "Ace Aventura", "score": 10000, "level": 10, "bonuses": ["funny_actor", "lame_movie"] },
        { "name": "Paladino Pino", "score": 9990, "level": 10 },
        { "name": "Name Inventor ", "score": 8990, "level": 8 },
        { "name": "Pete \"The Feet\" Sandoval", "score": 5990, "level": 7, "bonuses": ["played_drums"] },
        { "name": "Trey Azagthoth", "score": 5990, "level": 4, "bonuses": ["played_guitar"] },
        { "name": "Okay One More", "score": -5990, "level": 0, "bonuses": ["sucked_at_game"] }
    ],
    "bonuses": {
        "played_guitar": 10000,
        "played_drums": 9000,
        "sucked_at_game": -1,
        "lame_movie": -10000,
        "funny_actor": 1000
    }
}
"""
parser = Parser(data)
result = parser.parse()

# ~~~~

bonuses = result['bonuses']
players = []
for player in result['players']:
    if 'bonuses' in player:
        for bonus in player['bonuses']:
            player['score'] += bonuses[bonus]
    players.append(player)


sorted_players = sorted(players, key=lambda player: player['score'] * -1)

print "Name\tLevel\tScore"
for player in sorted_players:
    print "{0}\t{1}\t{2}".format(player['name'], player['level'], player['score'])
