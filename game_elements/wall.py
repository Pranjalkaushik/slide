
from game_elements.base import *

def get_wall(draw:Draw, window:pyglet.window.BaseWindow)->GameObject:
    wall_shape, wall_body = draw.draw_wall(
        (get_coordinate(window, 99, None)[0], GROUND_LEVEL+10),
        SLIDER_SIZE,
        SLIDER_SIZE*3
    )
    wall_collider = draw.add_collider(
        wall_body,
        'poly',
        (SLIDER_SIZE, SLIDER_SIZE*3)
    )
    wall = GameObject(
        window=window,
        shape=wall_shape,
        body=wall_body,
        collider=wall_collider
    )
    return wall
