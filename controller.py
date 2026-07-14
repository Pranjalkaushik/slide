import conf

def jump(body):
    body.apply_impulse_at_local_point((0, conf.JUMP_VELOCITY))
