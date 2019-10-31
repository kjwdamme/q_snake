import logging
import util
import random
import csv

log = logging.getLogger("client.snake")


class State(object):
    def __init__(self):
        self.obstacle_left = False
        self.obstacle_right = False
        self.obstacle_above = False
        self.obstacle_below = False
        self.food_left = False
        self.food_right = False
        self.food_above = False
        self.food_below = False

    def get_tuple(self):
        return self.obstacle_left,\
               self.obstacle_right,\
               self.obstacle_above,\
               self.obstacle_below,\
               self.food_left,\
               self.food_right,\
               self.food_above,\
               self.food_below


class QSnake(object):
    def __init__(self):
        self.name = "pik"
        self.snake_id = None
        self.qtable = self.read_qtable()
        self.last_move = util.Direction.UP

    def create_state(self, game_map, player_coords):
        width = game_map.game_map['width']
        state = State()

        food_coords = util.translate_positions(game_map.game_map['foodPositions'], width)
        head_coords = player_coords[0]

        if len(food_coords) > 0:
            distances = []
            for food in food_coords:
                distances.append((util.get_manhattan_distance(head_coords, food), food))

            food_to_catch = min(distances, key=lambda t: t[0])[1]

            if food_to_catch[0] < head_coords[0]:
                state.food_left = True
            if food_to_catch[0] > head_coords[0]:
                state.food_right = True
            if food_to_catch[1] < head_coords[1]:
                state.food_above = True
            if food_to_catch[1] > head_coords[1]:
                state.food_below = True
            if food_to_catch[0] == head_coords[0] and food_to_catch[1] == head_coords[1]:
                state.on_food = True

        if not game_map.is_tile_available_for_movement(self.calc_new_pos(head_coords, (1, 0))) or game_map.is_coordinate_out_of_bounds(self.calc_new_pos(head_coords, (1, 0))):
            state.obstacle_right = True
        if not game_map.is_tile_available_for_movement(self.calc_new_pos(head_coords, (-1, 0))) or game_map.is_coordinate_out_of_bounds(self.calc_new_pos(head_coords, (-1, 0))):
            state.obstacle_left = True
        if not game_map.is_tile_available_for_movement(self.calc_new_pos(head_coords, (0, -1))) or game_map.is_coordinate_out_of_bounds(self.calc_new_pos(head_coords, (0, -1))):
            state.obstacle_above = True
        if not game_map.is_tile_available_for_movement(self.calc_new_pos(head_coords, (0, 1))) or game_map.is_coordinate_out_of_bounds(self.calc_new_pos(head_coords, (0, 1))):
            state.obstacle_below = True

        return state

    def calc_new_pos(self, cur_pos, delta):
        return cur_pos[0] + delta[0], cur_pos[1] + delta[1]

    def get_next_move(self, game_map):
        width = game_map.game_map['width']

        player = next(filter(lambda x: x['name'] == self.name, game_map.game_map['snakeInfos']), None)
        player_coords = util.translate_positions(player['positions'], width)
        cur_state = self.create_state(game_map, player_coords)

        if cur_state.get_tuple() not in self.qtable:
            self.qtable[cur_state.get_tuple()] = [0, 0, 0, 0]

        learning_rate = .7
        discount_rate = .9
        exploration_chance = 0

        if exploration_chance > random.random():
            direction_num = random.randrange(4)
        else:
            direction_num = self.qtable[cur_state.get_tuple()].index(max(self.qtable[cur_state.get_tuple()]))

        if direction_num == 0:
            direction = util.Direction.DOWN
        elif direction_num == 1:
            direction = util.Direction.UP
        elif direction_num == 2:
            direction = util.Direction.LEFT
        elif direction_num == 3:
            direction = util.Direction.RIGHT
        else:
            print("That should not be possible")

        new_pos = (player_coords[0][0] + direction.value[1][0], player_coords[0][1] + direction.value[1][1])
        new_state = self.create_state(game_map, [new_pos])

        if new_state.get_tuple() not in self.qtable:
            self.qtable[new_state.get_tuple()] = [0, 0, 0, 0]

        curr_qvalue = self.qtable[cur_state.get_tuple()][direction_num]
        memory = (1 - learning_rate) * curr_qvalue
        reward = self.calc_reward(game_map, player_coords, new_pos)
        max_quality_step = max(self.qtable[new_state.get_tuple()])

        q_value = memory + learning_rate * (reward + discount_rate * max_quality_step)

        self.qtable[cur_state.get_tuple()][direction_num] = q_value

        return direction

    def calc_reward(self, game_map, cur_pos, new_head_pos):
        width = game_map.game_map['width']
        reward = 0

        food_coords = util.translate_positions(game_map.game_map['foodPositions'], width)
        obstacle_coords = util.translate_positions(game_map.game_map['obstaclePositions'], width)

        if new_head_pos in food_coords:
            reward += 100

        if new_head_pos in obstacle_coords or new_head_pos in cur_pos:
            reward -= 100

        enemies = filter(lambda x: x['name'] != self.name, game_map.game_map['snakeInfos'])
        enemy_positions = []
        for enemy in enemies:
            enemy_positions.append(util.translate_positions(enemy['positions'], width))

        if new_head_pos in enemy_positions:
            reward -= 100

        if reward == 0:
            reward += 20

        return reward

    def save_qtable(self):
        with open('qtable.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.qtable.items():
                writer.writerow([key, value])

    def read_qtable(self):
        with open('qtable.csv') as csv_file:
            reader = csv.reader(csv_file)
            dictio = dict(reader)
            new_dict = {}
            for key in dictio:
                l = []
                tup_arr = key.replace('(', '').replace(')', '').split(", ")
                for tup in tup_arr:
                    l.append(tup == 'True')
                tup = tuple(l)
                array = dictio[key].replace('[', '').replace(']', '').split(', ')

                i = []
                for item in array:
                    i.append(float(item))
                new_dict[tup] = i

            return new_dict

    def on_game_ended(self):
        self.save_qtable()
        log.debug('The game has ended!')

    def on_snake_dead(self, reason):
        self.save_qtable()
        log.debug('Our snake died because %s', reason)

    def on_game_starting(self):
        # self.read_qtable()
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
