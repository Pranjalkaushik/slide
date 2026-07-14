import pyglet
from pymunk import Space
import conf
from game_elements.base import GameObject, Draw

def get_ground(draw:Draw, space:Space, window:pyglet.window.BaseWindow)->GameObject:
    ground_shape = draw.draw_ground()
    ground_collider = draw.add_collider(
        space.static_body,
        'segment',
        (conf.GROUND_THICKNESS/2,),
        (0, conf.GROUND_LEVEL),
        (window.width, conf.GROUND_LEVEL)
    )
    ground = GameObject(
        window=window,
        shape=ground_shape,
        collider=ground_collider,
        space=draw.space
    )
    return ground
