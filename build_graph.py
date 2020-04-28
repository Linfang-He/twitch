import dgl
import pandas as pd
import pickle
import torch
from builder import PandasGraphBuilder

channels = pd.read_csv('channels.csv')
users = pd.read_csv('users.csv')
games = pd.read_csv('games.csv')
games_play = pd.read_csv('games_play.csv')

play2game = pd.read_csv('play2game.csv')
comments = pd.read_csv('comments.csv')
subscribes = pd.read_csv('train_truth.csv')


# Remove meaningless columns
channels.columns = ['_', 'channel']
channels = channels.drop(columns = '_', axis=1)
users.columns = ['_', 'user']
users = users.drop(columns = '_', axis=1)
games.columns = ['_', 'game']
games = games.drop(columns = '_', axis=1)
games_play.columns = ['_', 'game_play']
games_play = games_play.drop(columns = '_', axis=1)

play2game.columns = ['_', 'game_play', 'game']
play2game = play2game.drop(columns = '_', axis=1)
comments.columns = ['_', 'channel', 'user', 'timestamp', 'message', 'game_play']
comments = comments.drop(columns = ['_', 'message'], axis=1)

print("Finish reading csv files")


# Build trirelation graph
builder = PandasGraphBuilder()
builder.add_entities(users, 'user', 'user')
builder.add_entities(games, 'game', 'game')
builder.add_entities(channels, 'channel', 'channel')
builder.add_entities(games_play, 'game_play', 'game_play')

builder.add_binary_relations(play2game, 'game_play', 'game', 'corresponds')
# builder.add_binary_relations(play2game, 'game_play', 'game', 'corresponded')
builder.add_binary_relations(comments, 'user', 'game_play', 'comments')
# builder.add_binary_relations(comments, 'game', 'user', 'commented-by')
builder.add_binary_relations(comments, 'user', 'channel', 'watches')
# builder.add_binary_relations(comments, 'user', 'channel', 'watched-by')
builder.add_binary_relations(comments, 'channel', 'game_play', 'contains')
# builder.add_binary_relations(comments, 'game', 'channel', 'contained-by')
builder.add_binary_relations(subscribes, 'user', 'channel', 'subscribes')
# builder.add_binary_relations(subscribes, 'channel', 'user', 'subscribed-by')
g = builder.build()

# Assign features
g.edges['comments'].data['timestamp'] = torch.LongTensor(comments['timestamp'].values)
# g.edges['commented-by'].data['timestamp'] = torch.LongTensor(comments['timestamp'].values)

with open('g_comm_subs.pkl', 'wb') as f:
	pickle.dump(g, f)
print("Finish building the graph")


'''Three subgraphs'''
# Build user-comment-game graph
# builder_comment = PandasGraphBuilder()
# builder_comment.add_entities(users, 'user', 'user')
# builder_comment.add_entities(games, 'game', 'game')
# builder_comment.add_binary_relations(comments, 'user', 'game', 'comments')
# builder_comment.add_binary_relations(comments, 'game', 'user', 'commented-by')
# g_comment = builder_comment.build()

# Assign features
# g_comment.edges['comments'].data['timestamp'] = torch.LongTensor(comments['timestamp'].values)
# g_comment.edges['commented-by'].data['timestamp'] = torch.LongTensor(comments['timestamp'].values)

# with open('g_comment.pkl', 'wb') as f:
# 	pickle.dump(g_comment, f)
# print("Finish building user-comment-game graph")


# Build channel-contain-game graph
# builder_contain = PandasGraphBuilder()
# builder_contain.add_entities(channels, 'channel', 'channel')
# builder_contain.add_entities(games, 'game', 'game')
# builder_contain.add_binary_relations(comments, 'channel', 'game', 'contains')
# builder_contain.add_binary_relations(comments, 'game', 'channel', 'contained-by')
# g_contain = builder_contain.build()

# with open('g_contain.pkl', 'wb') as f:
# 	pickle.dump(g_contain, f)
# print("Finish building channel-contain-game graph")


# Build user-subscribe-channel graph
# builder_subscribe = PandasGraphBuilder()
# builder_subscribe.add_entities(channels, 'channel', 'channel')
# builder_subscribe.add_entities(users, 'user', 'user')
# builder_subscribe.add_binary_relations(subscribes, 'user', 'channel', 'subscribes')
# builder_subscribe.add_binary_relations(subscribes, 'channel', 'user', 'subscribed-by')
# g_subscribe = builder_subscribe.build()

# with open('g_subscribe.pkl', 'wb') as f:
# 	pickle.dump(g_subscribe, f)
# print("Finish building channel-contain-game graph")


# Dump the graph
# dataset = {
# 	'g_comment': g_comment,
# 	'g_contain': g_contain,
# 	'g_subscribe': g_subscribe
# }

# with open('graphs.pkl', 'wb') as f:
# 	pickle.dump(dataset, f)
