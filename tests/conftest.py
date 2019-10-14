import pytest


@pytest.fixture
def game_map():
    return {
        'width': 46,
        'height': 34,
        'worldTick': 12,
        'snakeInfos': [{
            'name': 'StayAliveBot',
            'points': 4,
            'positions': [411, 365, 319, 273, 227],
            'tailProtectedForGameTicks': 0,
            'id': 'a4924398-8e85-452d-854b-09635a100829'
        }, {
            'name': 'StraightBot',
            'points': 4,
            'positions': [92, 138, 184, 185, 186],
            'tailProtectedForGameTicks': 0,
            'id': '92a976fc-616b-4f5e-a3dc-fc5bad775092'
        }, {
            'name': 'StraightBot',
            'points': 4,
            'positions': [1483, 1484, 1485, 1486, 1487],
            'tailProtectedForGameTicks': 0,
            'id': 'a5215ec7-ced6-48c9-8209-7006052ee420'
        }, {
            'name': 'expert_snake.py',
            'points': 4,
            'positions': [1560, 1514, 1468, 1422, 1376],
            'tailProtectedForGameTicks': 0,
            'id': '6dbded46-684a-4227-841c-a017619d1f05'
        }, {
            'name': 'StraightBot',
            'points': 4,
            'positions': [552, 598, 644, 690, 736],
            'tailProtectedForGameTicks': 0,
            'id': '02941ffa-13cb-4d67-950c-b03e0fd2dfba'
        }],
        'foodPositions': [1406],
        'obstaclePositions': [
            59, 60, 61, 105, 106, 107, 151, 152, 153, 385, 386, 395, 431, 432,
            519, 520, 521, 565, 566, 567, 582, 611, 612, 613
        ]
    }
