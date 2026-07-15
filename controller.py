import conf
from game_elements.base import GameObject
from utils import on_ground

def jump(game_obj:GameObject):
    body = game_obj.body
    if conf.JUMP_COUNT:
        body.apply_impulse_at_local_point((0, conf.JUMP_VELOCITY*(2/conf.JUMP_COUNT)))
        conf.JUMP_COUNT -= 1
