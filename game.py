from pyglet.customtypes import AnchorX
import pyglet, pymunk

window = pyglet.window.Window()

TITLE = 'GO SLIDE !'
TITLE_FONT_SIZE = 36
SLIDER_SIZE = 10

# utils
def get_coordinate(horizontal_percentage:float|None, verticle_percentage:float|None) -> tuple:
    x, y = None, None
    if horizontal_percentage:
        x = horizontal_percentage * window.width / 100
    if verticle_percentage:
        y = verticle_percentage * window.height / 100
    return x,y

# label
label = pyglet.text.Label(
    TITLE,
    font_name='Times New Roman',
    font_size=TITLE_FONT_SIZE,
    x=get_coordinate(50, None)[0],
    y=get_coordinate(None, 100)[1] - TITLE_FONT_SIZE,
    anchor_x='center',
    anchor_y='center'
    )

# space and objects
space = pymunk.Space()
space.gravity = (0, -1800)

batch = pyglet.graphics.Batch()



slider_shape = pyglet.shapes.Rectangle(
    get_coordinate(50, None)[0],
    get_coordinate(None, 50)[1],
    width=SLIDER_SIZE,
    height=SLIDER_SIZE,
    color=(80,200,120),
    batch=batch
)

slider_body = pymunk.Body(
    mass=1,
    moment=float('inf'),
)
slider_body.position = get_coordinate(50, 50)

slider_collider = pymunk.Poly.create_box(slider_body, (SLIDER_SIZE, SLIDER_SIZE))
slider_collider.friction = 1

space.add(slider_body, slider_collider)


slider_2_shape = pyglet.shapes.Rectangle(
    get_coordinate(50, None)[0] - ((SLIDER_SIZE + 30)/2),
    get_coordinate(None, 20)[1],
    width=SLIDER_SIZE+30,
    height=SLIDER_SIZE,
    color=(80,200,120),
    batch=batch
)
slider_2_body = pymunk.Body(
    body_type=pymunk.Body.STATIC
)
slider_2_body.position = get_coordinate(50, 20)

slider_2_collider = pymunk.Poly.create_box(slider_2_body, (SLIDER_SIZE, SLIDER_SIZE))
slider_2_collider.friction = 1

space.add(slider_2_body, slider_2_collider)


# draw and update

DT = 1 / 120
_accum = 0

def update(frame_dt):
    global _accum
    _accum += min(frame_dt, 0.25)
    while _accum >= DT:
        space.step(DT)
        _accum -= DT
    slider_shape.position = slider_body.position


@window.event
def on_draw():
    window.clear()
    label.draw()
    batch.draw()

pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
    
