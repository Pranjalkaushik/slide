
import pyglet
from pymunk import Space
from utils import get_coordinate
from game_elements.base import GameObject, Draw, GameWorld

def get_label(text:str, draw:Draw, space:Space, window:pyglet.window.BaseWindow)->GameObject:
    top_pos = get_coordinate(window, 50, 80)
    text_l = draw.draw_text(text, top_pos, 30)
    label = GameObject(
        window=window,
        label=text_l,
        space=space
    )
    GameWorld.add_obj('label', label)
    return label
