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
        self.apple_reward = 100
        self.death_reward = -100
        self.life_reward = 1
        self.score = 0
        self.episode_length = 0
        self.episode_reward = 0
        self.experience_buffer = []
        self.agent = DQAgent(actions)
        self.action = random.randint(0, actions)
        self.last_move = util.Direction.DOWN

    def get_next_move(self, game_map):
        reward = self.life_reward
        width = game_map.game_map['width']
        player = next(filter(lambda x: x['name'] == self.name, game_map.game_map['snakeInfos']), None)
        player_coords = util.translate_positions(player['positions'], width)
        food_coords = util.translate_positions(game_map.game_map['foodPositions'], width)
        obstacle_coords = util.translate_positions(game_map.game_map['obstaclePositions'], width)

        if self.action == 0 and self.last_move != util.Direction.UP:
            direction = util.Direction.DOWN
        elif self.action == 1 and self.last_move != util.Direction.DOWN:
            direction = util.Direction.UP
        elif self.action == 2 and self.last_move != util.Direction.RIGHT:
            direction = util.Direction.LEFT
        elif self.action == 3 and self.last_move != util.Direction.LEFT:
            direction = util.Direction.RIGHT
        else:
            direction = self.last_move

        new_pos = [(player_coords[0][0] + direction.value[1][0], player_coords[0][1] + direction.value[1][1])]

        if len(food_coords) > 0:
            for food in food_coords:
                if food == new_pos[0]:
                    self.score += 1
                    reward = self.apple_reward

        if len(obstacle_coords) > 0:
            for obstacle in obstacle_coords:
                if obstacle == new_pos[0]:
                    reward = self.death_reward

        if util.Map.is_coordinate_out_of_bounds(game_map, new_pos):
            reward = self.death_reward

            # Add SARS tuple to experience_buffer
        # experience_buffer.append((np.asarray([game_map]), self.action, reward, np.asarray([next_state])))
        episode_reward += reward

        # Change current state
        # state = list(next_state)

        # Poll the DQAgent to get the next action
        action = self.DQA.get_action(np.asarray([game_map]))

        return direction

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
