import logging
import util

log = logging.getLogger("client.snake")


class ExpertSnake(object):
    def __init__(self):
        self.name = "expert slang"
        self.snake_id = None

    def right_available(self, curr_pos, game_map):
        return game_map.is_tile_available_for_movement((curr_pos[0] + 1, curr_pos[1]))

    def left_available(self, curr_pos, game_map):
        return game_map.is_tile_available_for_movement((curr_pos[0] - 1, curr_pos[1]))

    def down_available(self, curr_pos, game_map):
        return game_map.is_tile_available_for_movement((curr_pos[0], curr_pos[1] + 1))

    def up_available(self, curr_pos, game_map):
        return game_map.is_tile_available_for_movement((curr_pos[0], curr_pos[1] - 1))

    def next_in_snake(self, direction, positions):
        if direction == util.Direction.RIGHT:
            return (positions[0][0] + 1, positions[0][1]) in positions
        elif direction == util.Direction.LEFT:
            return (positions[0][0] - 1, positions[0][1]) in positions
        elif direction == util.Direction.DOWN:
            return (positions[0][0], positions[0][1] + 1) in positions
        else:
            return (positions[0][0], positions[0][1] - 1) in positions

    def get_next_move(self, game_map):
        width = game_map.game_map['width']

        players = game_map.game_map['snakeInfos']
        player = next(filter(lambda x: x['name'] == self.name, players), None)
        player_pos = util.translate_positions(player['positions'], width)

        food_positions = game_map.game_map['foodPositions']

        # food_coords = food_positions[0] if len(food_positions) > 0 else None

        food_coords = util.translate_positions(food_positions, width)

        if len(food_coords) > 0:
            distances = []
            for food in food_coords:
                distances.append((util.get_manhattan_distance(player_pos[0], food), food))

            food_to_catch = min(distances, key=lambda t: t[0])[1]

            if food_to_catch[0] > player_pos[0][0]:
                if self.right_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.RIGHT, player_pos):
                    return util.Direction.RIGHT
                elif self.down_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.DOWN, player_pos):
                    return util.Direction.DOWN
                else:
                    return util.Direction.UP
            elif food_to_catch[0] < player_pos[0][0]:
                if self.left_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.LEFT, player_pos):
                    return util.Direction.LEFT
                elif self.down_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.DOWN, player_pos):
                    return util.Direction.DOWN
                else:
                    return util.Direction.UP



            elif food_to_catch[1] > player_pos[0][1]:
                if self.down_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.DOWN, player_pos):
                    return util.Direction.DOWN
                elif self.right_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.RIGHT, player_pos):
                    return util.Direction.RIGHT
                else:
                    return util.Direction.LEFT
            elif food_to_catch[1] < player_pos[0][1]:
                if self.up_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.UP, player_pos):
                    return util.Direction.UP
                elif self.right_available(player_pos[0], game_map) and not self.next_in_snake(util.Direction.RIGHT, player_pos):
                    return util.Direction.RIGHT
                else:
                    return util.Direction.LEFT
            else:
                return util.Direction.DOWN
        else:
            return util.Direction.DOWN

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
    return ExpertSnake()
