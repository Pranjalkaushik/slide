import pyglet
import conf
from game_elements.base import Draw, GameObject


def get_slider(draw:Draw, window:pyglet.window.BaseWindow)->GameObject:
    slider_shape, slider_body = draw.draw_slider()
    slider_collider = draw.add_collider(
        slider_body,
        'poly',
        (conf.SLIDER_SIZE, conf.SLIDER_SIZE)
    )
    slider = GameObject(
        window=window,
        shape=slider_shape,
        body=slider_body,
        collider=slider_collider,
        space=draw.space
    )
    return slider
