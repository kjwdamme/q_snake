import logging
import util
import state

log = logging.getLogger("client.snake")


class DQNSnake(object):
    def __init__(self, agent):
        self.name = "dqn snake"
        self.agent = agent

    def calc_new_pos(self, cur_pos, delta):
        return cur_pos[0] + delta[0], cur_pos[1] + delta[1]

    def get_next_move(self, game_map):
        # initialize gym environment and the agent
        width = game_map.game_map['width']

        player = next(filter(lambda x: x['name'] == self.name, game_map.game_map['snakeInfos']), None)
        player_coords = util.translate_positions(player['positions'], width)

        # reset state in the beginning of each game
        # state = self.create_state(game_map, player_coords)
        curr_state = state.create_state(game_map, player_coords)

        direction_num = self.agent.act(curr_state.get_array())

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

        new_pos = self.calc_new_pos(player_coords[0], direction.value[1])
        # next_state = self.create_state(game_map, [new_pos])
        next_state = state.create_state(game_map, [new_pos])

        reward = self.calc_reward(game_map, player_coords[0], new_pos)

        # Remember the previous state, action, reward, and done
        self.agent.remember(curr_state.get_array(), direction_num, reward, next_state.get_array())

        # train the agent with the experience of the episode

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

    def on_game_ended(self):
        self.agent.replay(5)

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


def get_snake(agent):
    return DQNSnake(agent)
