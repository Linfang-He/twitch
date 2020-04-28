import json
import pandas as pd

channels, users, games, games_play = [], [], [], []
comments, play2game = [], []

# lines = []
with open('train.json', 'r') as f:
	for line in f:
		record = json.loads(line) 
		messages = record['ms']
		channels.append(record['c'])
		users.append(record['u'])
		for ms in messages:
			comments.append({
				'channel': record['c'],
				'user': record['u'],
				'timestamp': ms['t'],
				'comment': ms['m'],
				'game_play': record['c'] + '_' + ms['g'],
				})
			play2game.append({
				'game_play': record['c'] + '_' + ms['g'],
				'game': ms['g'],
				})
			games_play.append(record['c'] + '_' + ms['g'])
			games.append(ms['g'])

channels = pd.DataFrame(list(set(channels)))
users = pd.DataFrame(list(set(users)))
games = pd.DataFrame(list(set(games)))
games_play = pd.DataFrame(list(set(games_play)))
play2game = pd.DataFrame(play2game).astype('category')
comments = pd.DataFrame(comments).astype({'channel': 'category', 'user': 'category', 'game_play': 'category'})

channels.to_csv('channels.csv')
users.to_csv('users.csv')
games.to_csv('games.csv')
games_play.to_csv('games_play.csv')
play2game.to_csv('play2game.csv')
comments.to_csv('comments.csv')

print("Number of channels:", channels.shape[0])  # 146537
print("Number of users:", users.shape[0])  # 7923774
print("Number of games:", games.shape[0])  # 7576
print("Number of games_play", games_play.shape[0])  # 301815
print("Number of play2game", play2game.shape[0])  # 410686442
print("Number of records:", comments.shape[0])  # 410686442
print("Finish processing train.json")


"""Simply judge whether a game exists in multiple channels"""
# users = []
# all_games = []
# with open('train.json', 'r') as f:
# 	for i in range(50):
# 		tmp_g = []
# 		line = f.readline()
# 		result = json.loads(line)
# 		for d in result['ms']:
# 			tmp_g.append(d['g'])
# 		all_games = all_games + list(set(tmp_g))

# set_games = list(set(all_games))

# print(len(set_games))
# print(len(all_games))