import pyglet
import config

window = pyglet.window.Window(width=1024, height=768)

# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           color=(0,0,0,255),
#                           x=window.width//2, y=window.height//2,
#                           anchor_x='left', anchor_y='center')

background = pyglet.resource.image('assets/background.png')
ratio = window.width/background.width, window.height/background.height
# TODO: also change ratio to font size (e.g. config.names_font.font_size)

def mul_ratio(vec):
    return vec[0]*ratio[0], vec[1]*ratio[1]


def reloc(pos):
    return pos[0], background.height-pos[1]


# Multiply for any screen resoltion and transalte (0,0)@top-left to (0,0)@bottom-left coordinates
def ratio_blit(image, pos, size):
    rpos = mul_ratio(reloc(pos))
    image.blit(rpos[0], rpos[1]-image.height*ratio[1], 0, *mul_ratio(size))


def on_joyaxis_motion(joystick, axis, value):
    if abs(value) > config.joy_analog_treshold:
        print('motion' + str(joystick) + '  ' + str(axis) + '  ' + str(value))


joysticks = pyglet.input.get_joysticks()
print(joysticks)
if not joysticks:
    print('No se detectaron joysticks!')
else:
    for idx, joy in joysticks:
        print('Joystick detectado #'+str(idx)+': ' + str(joy.device))

        joy.on_joyaxis_motion = on_joyaxis_motion
        joy.open()


example = pyglet.resource.image('assets/example_preview.png')


# create labels
ratio_names_pos = mul_ratio(reloc(config.names_pos))
labels = []
for i in range(0, config.names_lines):
    norm_pivot = 2 * (i / (config.names_lines-1) - 0.5)     # fractional value form -1 to 1 according to the index (center should be == 0 for odd config.names_lines)
    pivot = norm_pivot * (config.names_lines-1) / 2         # pivot relative to the amount of actual lines (used for separation)
    labels.append(pyglet.text.Label('Linea '+str(i)
                                    , **config.names_font
                                    , x=ratio_names_pos[0]
                                    , y=ratio_names_pos[1] - pivot * config.names_separation_y*ratio[1]
                                    , anchor_x='left', anchor_y='center'
                                    ))
    labels[i].font_size += (1-abs(norm_pivot)) * config.names_central_growth





#test
sprite = None
try:
    animation = pyglet.image.load_animation('assets/roboarcade2.gif')
    bin = pyglet.image.atlas.TextureBin()
    animation.add_to_texture_bin(bin)
    sprite = pyglet.sprite.Sprite(animation)
    sprite.scale = 3
except:
    pass

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0, 0, window.width, window.height)
    ratio_blit(example, config.preview_pos, config.preview_size)
    for label in labels: label.draw()
    if sprite: sprite.draw()


pyglet.app.run()
