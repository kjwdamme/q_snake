import numpy as np
import util


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

    def get_array(self):
        return np.array([[self.obstacle_left, self.obstacle_right, self.obstacle_above, self.obstacle_below, self.food_left, self.food_right, self.food_above, self.food_below]])

    def get_tuple(self):
        return self.obstacle_left,\
               self.obstacle_right,\
               self.obstacle_above,\
               self.obstacle_below,\
               self.food_left,\
               self.food_right,\
               self.food_above,\
               self.food_below


def create_state(game_map, player_coords):
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

    if not game_map.is_tile_available_for_movement(calc_new_pos(head_coords, (1, 0))) or game_map.is_coordinate_out_of_bounds(calc_new_pos(head_coords, (1, 0))):
        state.obstacle_right = True
    if not game_map.is_tile_available_for_movement(calc_new_pos(head_coords, (-1, 0))) or game_map.is_coordinate_out_of_bounds(calc_new_pos(head_coords, (-1, 0))):
        state.obstacle_left = True
    if not game_map.is_tile_available_for_movement(calc_new_pos(head_coords, (0, -1))) or game_map.is_coordinate_out_of_bounds(calc_new_pos(head_coords, (0, -1))):
        state.obstacle_above = True
    if not game_map.is_tile_available_for_movement(calc_new_pos(head_coords, (0, 1))) or game_map.is_coordinate_out_of_bounds(calc_new_pos(head_coords, (0, 1))):
        state.obstacle_below = True

    return state


def calc_new_pos(cur_pos, delta):
    return cur_pos[0] + delta[0], cur_pos[1] + delta[1]
