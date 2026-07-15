import pyglet
import random
import conf
from utils import get_coordinate
from game_elements.base import GameObject, Draw, GameWorld

def get_wall(draw:Draw, window:pyglet.window.BaseWindow)->GameObject:
    wall_shape, wall_body = draw.draw_wall(
        (get_coordinate(window, 99, None)[0], conf.GROUND_LEVEL+10),
        conf.SLIDER_SIZE,
        conf.SLIDER_SIZE*3
    )
    wall_collider = draw.add_collider(
        wall_body,
        'poly',
        (conf.SLIDER_SIZE, conf.SLIDER_SIZE*3)
    )
    wall = GameObject(
        window=window,
        shape=wall_shape,
        body=wall_body,
        collider=wall_collider,
        space=draw.space
    )
    GameWorld.add_obj('wall', wall)
    return wall


def next_height(wall:GameObject):
    return max(conf.SLIDER_SIZE*3, random.randrange(wall.shape.height-50, wall.shape.height+100))
