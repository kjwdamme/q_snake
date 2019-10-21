import logging
import util
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add
from DQAgent import DQAgent
from keras.utils import to_categorical
import numpy as np

log = logging.getLogger("client.snake")


class DQNSnake(object):
    def __init__(self):
        self.actions = 3
        self.agent = DQAgent(actions)

    def get_next_move(self, game_map):
        width = game_map.game_map['width']
        players = game_map.game_map['snakeInfos']
        player = next(filter(lambda x: x['name'] == self.name, players), None)
        player_pos = util.translate_positions(player['positions'], width)

        action = random.randint(0, actions)


    def on_game_ended(self):
        log.debug('The game has ended!')

    def on_snake_dead(self, reason):
        log.debug('Our snake died because %s', reason)

    def on_game_starting(self):
        log.debug('Game is starting!')

    def on_player_registered(self, snake_id):
        log.debug('Player registered successfully')
        self.snake_id = snake_id

    def on_invalid_player_name(self):
        log.fatal('Player name is invalid, try another!')

    def on_game_result(self, player_ranks):
        log.info('Game result:')
        for player in player_ranks:
            is_alive = 'alive' if player['alive'] else 'dead'
            log.info('%d. %d pts\t%s\t(%s)' %
                     (player['rank'], player['points'], player['playerName'],
                      is_alive))


def get_snake():
    return DQNSnake()
