import pyglet, pymunk
import conf
from pymunk.pyglet_util import DrawOptions
from controller import jump
from utils import get_coordinate
from game_elements.base import Draw 
from game_elements.ground import get_ground
from game_elements.wall import get_wall
from game_elements.slider import get_slider

window = pyglet.window.Window(resizable=True)
space = pymunk.Space()
space.gravity = (0, -1800)
draw_options = DrawOptions()
batch = pyglet.graphics.Batch()

d = Draw(window, space, batch)
ground = get_ground(d, space, window)
wall = get_wall(d, window)
slider = get_slider(d, window)


DT = 1 / 120
_accum = 0


def update(frame_dt):
    global _accum
    global wall_direction
    import controller
    _accum += min(frame_dt, 0.25)
    while _accum >= DT:
        space.step(DT)
        _accum -= DT
    slider.sync_shape()
    wall.move_left()
    if wall.body and wall.body.position.x < get_coordinate(window, 1, None)[0]:
        wall.shape.height += 100
        wall.shape.anchor_position = (wall.shape.width/2, wall.shape.height/2)
        wall.rebuild_collider()
        wall.body.position = (get_coordinate(window, 99, None)[0], conf.GROUND_LEVEL+wall.shape.height/2)
        conf.GROUND_VELOCITY += 100
    wall.sync_shape()


@window.event
def on_draw():
    window.clear()
    batch.draw()
    #space.debug_draw(draw_options)


@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.SPACE:
        jump(slider.body)


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
    
