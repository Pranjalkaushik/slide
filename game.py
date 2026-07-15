import pyglet, pymunk
import conf
import random
from pymunk.pyglet_util import DrawOptions
from controller import jump
from utils import are_in_contact, get_coordinate, on_ground
from game_elements.base import Draw 
from game_elements.ground import get_ground
from game_elements.wall import get_wall, next_height
from game_elements.slider import get_slider
from game_elements.label import get_label

window = pyglet.window.Window(fullscreen=True)
space = pymunk.Space()
space.gravity = conf.GRAVITY
draw_options = DrawOptions()
batch = pyglet.graphics.Batch()

d = Draw(window, space, batch)
label = get_label('0', d, space, window)
ground = get_ground(d, space, window)
wall = get_wall(d, window)
slider = get_slider(d, window)


DT = 1 / 120
_accum = 0
points = 0

def update(frame_dt):
    global _accum
    global wall_direction
    global points
    
    if (slider.body.position[0] <  get_coordinate(window, -1, None)[0]) or are_in_contact(slider, wall):
        label.label.text = "Game Over !"
        return

    _accum += min(frame_dt, 0.25)
    while _accum >= DT:
        space.step(DT)
        _accum -= DT
    slider.sync_shape()
    if on_ground(slider):
        conf.JUMP_COUNT = 2
    wall.move_left()
    if wall.body and wall.body.position.x < get_coordinate(window, -5, None)[0]:
        # move wall to start
        wall.shape.height = next_height(wall)
        wall.shape.anchor_position = (wall.shape.width/2, wall.shape.height/2)
        wall.rebuild_collider()
        wall.body.position = (get_coordinate(window, 99, None)[0], conf.GROUND_LEVEL+wall.shape.height/2)
        
        # move slider a bit further
        slider.move_right(1.5)

        points += 1
        label.label.text = str(points)
        conf.GROUND_VELOCITY = min(conf.MAX_GROUND_VELOCITY, random.randrange(conf.GROUND_VELOCITY, conf.GROUND_VELOCITY+50)) 
    wall.sync_shape()


@window.event
def on_draw():
    window.clear()
    batch.draw()
    #space.debug_draw(draw_options)


@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.SPACE:
        jump(slider)


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
    
