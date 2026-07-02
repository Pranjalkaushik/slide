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

GROUND_LEVEL = get_coordinate(None, 20)[1]
GROUND_THICKNESS = 10

class Draw:
    
    def __init__(self, space, batch):
        self.space = space
        self.batch = batch

    def draw_text(self, text, pos, size):
        t = pyglet.text.Label(
            text,
            font_name='Times New Roman',
            font_size=size,
            x=pos[0],
            y=pos[1],
            anchor_x='center',
            anchor_y='center'
            )
        return t

    def draw_ground(self):
        ground_shape = pyglet.shapes.Line(
            0, GROUND_LEVEL,
            window.width, GROUND_LEVEL,
            thickness = GROUND_THICKNESS,
            color=(80,200,120),
            batch=batch
        )
        return ground_shape

    def draw_slider(self):
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
        return slider_shape, slider_body


    def draw_wall(self, pos, size):
        ...

    def draw_box(self, pos, size):
        ...

    def add_collider(self, body, collider_type, size, pos_1 = None, pos_2 = None, friction = 1):
        if collider_type == 'poly': 
            collider = pymunk.Poly.create_box(
                body,
                (size - 10, size - 10)
            )
            collider.friction = friction
            space.add(body, collider)

        elif collider_type == 'segment':
            collider = pymunk.Segment(
                body,
                pos_1,
                pos_2,
                size
            )
            collider.friction = friction
            space.add(collider)


space = pymunk.Space()
space.gravity = (0, -1800)
batch = pyglet.graphics.Batch()

d = Draw(space, batch)

label = d.draw_text(
    TITLE,
    get_coordinate(50, 95),
    TITLE_FONT_SIZE
)

slider_shape, slider_body = d.draw_slider()
d.add_collider(
    slider_body,
    'poly',
    SLIDER_SIZE
)

ground_shape = d.draw_ground()
d.add_collider(
    space.static_body,
    'segment',
    GROUND_THICKNESS/2,
    (0, GROUND_LEVEL),
    (window.width, GROUND_LEVEL)
)

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
    
