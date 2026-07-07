
GROUND_VELOCITY = 500
JUMP_VELOCITY = 700

def jump(body):
    body.apply_impulse_at_local_point((0, JUMP_VELOCITY))
