import logging
import util
import random
import itertools
import csv

log = logging.getLogger("client.snake")


class State(object):
    def __init__(self):
        self.food_left = False
        self.food_above = False
        self.on_food = False
        self.obstacle_left = False
        self.obstacle_above = False
        self.on_obstacle = False

    def get_tuple(self):
        return self.food_left, self.food_above, self.on_food, self.obstacle_left, self.obstacle_above, self.on_obstacle

    def calc_reward(self):
        total_reward = 0

        total_reward += -5

        if self.food_left:
            total_reward += 5
        if self.food_above:
            total_reward += 5
        if self.on_food:
            total_reward += 100
        if self.on_obstacle:
            total_reward += -100

        return total_reward


class QSnake(object):
    def __init__(self):
        self.name = "q learing slang"
        self.snake_id = None
        self.qtable = self.read_qtable()
        self.prev_state = State()

    def init_qtable(self):
        qtable = {}
        bool_combinations = list(itertools.product([True, False], repeat=6))

        for comb in bool_combinations:
            state = State()
            state.food_left = comb[0]
            state.food_above = comb[1]
            state.on_food = comb[2]
            state.obstacle_left = comb[3]
            state.obstacle_above = comb[4]
            state.on_obstacle = comb[5]

            qtable[state.get_tuple()] = [0, 0, 0, 0]

        return qtable

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

        learning_rate = .7
        discount_rate = .9
        exploration_chance = 1
        step = .1

        if exploration_chance > random.random():
            direction_num = random.randrange(4)
            if exploration_chance > 0:
                exploration_chance -= step
        else:
            direction_num = self.qtable[cur_state.get_tuple()].index(max(self.qtable[cur_state.get_tuple()]))

        if direction_num == 0:
            direction = util.Direction.DOWN
        elif direction_num == 1:
            direction = util.Direction.UP
        elif direction_num == 2:
            direction = util.Direction.LEFT
        else:
            direction = util.Direction.RIGHT

        new_pos = [(player_coords[0][0] + direction.value[1][0], player_coords[0][1] + direction.value[1][1])]
        new_state = self.create_state(game_map, new_pos)

        memory = (1 - learning_rate) * self.qtable[cur_state.get_tuple()][direction_num]
        reward = cur_state.calc_reward()
        max_quality_step = max(self.qtable[new_state.get_tuple()])

        self.qtable[cur_state.get_tuple()][direction_num] = memory + learning_rate * (reward + discount_rate * max_quality_step)

        return direction

    def save_qtable(self):
        with open('qtable.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.qtable.items():
                writer.writerow([key, value])

    def read_qtable(self):
        with open('../qtable.csv') as csv_file:
            reader = csv.reader(csv_file)
            dictio = dict(reader)
            return dictio

    def on_game_ended(self):
        self.save_qtable()
        log.debug('The game has ended!')

    def on_snake_dead(self, reason):
        self.save_qtable()
        log.debug('Our snake died because %s', reason)

    def on_game_starting(self):
        self.read_qtable()
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
