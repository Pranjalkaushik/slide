from pymunk import Space

from game_elements.base import *

def get_ground(draw:Draw, space:Space, window:pyglet.window.BaseWindow)->GameObject:
    ground_shape = draw.draw_ground()
    ground_collider = draw.add_collider(
        space.static_body,
        'segment',
        (GROUND_THICKNESS/2,),
        (0, GROUND_LEVEL),
        (window.width, GROUND_LEVEL)
    )
    ground = GameObject(
        window=window,
        shape=ground_shape,
        collider=ground_collider
    )
    return ground
