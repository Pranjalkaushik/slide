import pyglet
from game_elements.base import GameWorld, GameObject
import conf

def get_coordinate(
        window:pyglet.window.BaseWindow,
        horizontal_percentage:float|None,
        verticle_percentage:float|None
) -> tuple:
    x, y = None, None
    if horizontal_percentage:
        x = horizontal_percentage * window.width / 100
    if verticle_percentage:
        y = verticle_percentage * window.height / 100
    return x,y


def are_in_contact(body_1:GameObject, body_2:GameObject):
    if body_1.collider and body_2.collider:
        overlaps = body_1.space.shape_query(body_1.collider)
        return any([o.shape is body_2.collider for o in overlaps])


def on_ground(body:GameObject) -> bool:
    ground = GameWorld.get_obj('ground')
    if ground:
        return bool(are_in_contact(body, ground))
