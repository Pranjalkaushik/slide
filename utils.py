import pyglet
from game_elements.base import GameWorld, GameObject

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

def on_ground(body:GameObject) -> bool:
    ground = GameWorld.get_obj('ground')
    if body.collider and ground and ground.collider:
        overlaps = body.space.shape_query(body.collider)
        return any(o.shape is ground.collider for o in overlaps)
