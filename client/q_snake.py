import logging
import util
import random

log = logging.getLogger("client.snake")


class State(object):
    def __init__(self):
        self.food_left = False
        self.food_above = False
        self.on_food = False
        self.obstacle_left = False
        self.obstacle_above = False
        self.on_obstacle = False

    def calc_reward(self):
        total_reward = 0

        if self.food_left:
            total_reward += -1
        elif self.food_above:
            total_reward += -1
        elif self.on_food:
            total_reward += 100
        elif self.obstacle_left:
            total_reward += -1
        elif self.obstacle_above:
            total_reward += -1
        elif self.on_obstacle:
            total_reward += -100

        return total_reward


class QSnake(object):
    def __init__(self):
        self.name = "q learing slang"
        self.snake_id = None
        self.qtable = {}
        self.prev_state = State()

    def create_state(self, game_map, player_coords):
        new_state = State()

        width = game_map.game_map['width']

        food_coords = util.translate_positions(game_map.game_map['foodPositions'], width)
        obstacle_coords = util.translate_positions(game_map.game_map['obstaclePositions'], width)

        if len(food_coords) > 0:
            distances = []
            for food in food_coords:
                distances.append((util.get_manhattan_distance(player_coords[0], food), food))

            food_to_catch = min(distances, key=lambda t: t[0])[1]

            new_state.food_left = True if food_to_catch[0] < player_coords[0][0] else False

            new_state.food_above = True if food_to_catch[1] < player_coords[0][1] else False

            new_state.on_food = True if food_to_catch == player_coords[0] else False

            if len(obstacle_coords) > 0:
                for obstacle in obstacle_coords:
                    new_state.obstacle_left = True if player_coords[0][0] > obstacle[0] > food_to_catch[0] else False
                    new_state.obstacle_above = True if player_coords[0][1] > obstacle[0] > food_to_catch[1] else False
                    new_state.on_obstacle = True if obstacle == player_coords[0] else False

        return new_state

    def get_next_move(self, game_map):
        width = game_map.game_map['width']

        player = next(filter(lambda x: x['name'] == self.name, game_map.game_map['snakeInfos']), None)
        player_coords = util.translate_positions(player['positions'], width)

        cur_state = self.create_state(game_map, player_coords)
        self.qtable[cur_state] = [0, 0, 0, 0]

        learning_rate = .7
        discount_rate = .9
        exploration_chance = 1
        step = .1

        if exploration_chance < random.random():
            direction_num = random.randrange(4)
            if exploration_chance > 0:
                exploration_chance -= step
        else:
            direction_num = self.qtable[cur_state].index(max(self.qtable[cur_state]))

        if direction_num == 0:
            direction = util.Direction.DOWN
        elif direction_num == 1:
            direction = util.Direction.UP
        elif direction_num == 2:
            direction = util.Direction.LEFT
        else:
            direction = util.Direction.RIGHT

        new_state = self.create_state(game_map, player_coords + direction[1])

        self.qtable[cur_state][direction_num] = (1 - learning_rate) * self.qtable[cur_state][direction_num] + learning_rate * (cur_state.calc_reward() + discount_rate * max(self.qtable[new_state]))

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
    return QSnake()
