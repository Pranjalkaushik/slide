import conf
from game_elements.base import GameObject
from utils import on_ground

def jump(game_obj:GameObject):
    body = game_obj.body
    if on_ground(game_obj):
        body.apply_impulse_at_local_point((0, conf.JUMP_VELOCITY))
