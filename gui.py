import pyglet
import config
import subprocess
from pyglet.window import key

game_infos = None

window = pyglet.window.Window(width=1024, height=768)

# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           color=(0,0,0,255),
#                           x=window.width//2, y=window.height//2,
#                           anchor_x='left', anchor_y='center')

selected = 0
process = None
background = pyglet.resource.image('assets/background.png')
ratio = window.width/background.width, window.height/background.height
# TODO: also change ratio to font size (e.g. config.names_font.font_size)


def mul_ratio(vec):
    return vec[0]*ratio[0], vec[1]*ratio[1]


def reloc(pos):
    return pos[0], background.height-pos[1]

label_description = pyglet.text.HTMLLabel('Descripcion <b>soporta <i>HTML</i></b><br />', multiline = True, y = mul_ratio(reloc((10,30)))[1], width = 300*ratio[0])
label_description.text += '''
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae tortor eget nulla lacinia dictum eu vehicula enim. Etiam id nisi sapien. Curabitur dui tellus, interdum ut mi eget, molestie egestas neque. Morbi sit amet leo vel odio molestie dictum. Nam gravida bibendum nisi, id iaculis mauris cursus et. Fusce tempus, purus sed bibendum efficitur, justo ligula porta metus, et tempus enim leo at ante. Duis rhoncus elit et lacus auctor, ut dignissim nunc rutrum. Phasellus sit amet arcu at arcu dignissim elementum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed finibus lorem sed tristique rutrum. Proin varius euismod augue sit amet elementum. Curabitur semper, metus vel interdum eleifend, lacus magna faucibus purus, quis bibendum massa diam eget massa.
Curabitur placerat suscipit congue. Duis vestibulum urna sed libero sagittis, at ultricies nisi laoreet. Phasellus in velit libero. Praesent ac eros vitae quam dignissim ullamcorper. Ut facilisis nunc et facilisis faucibus. Aliquam rhoncus vestibulum nulla eu rutrum. Duis quis luctus libero. Integer fermentum id quam et pharetra. Integer nec arcu in turpis ultricies tincidunt. Nullam a ante ut magna pellentesque viverra eu sed lectus. Morbi et tortor purus. Praesent scelerisque, eros vel interdum ultricies, diam libero vulputate justo, vel eleifend augue risus id augue.
'''


# Multiply for any screen resoltion and transalte (0,0)@top-left to (0,0)@bottom-left coordinates
def ratio_blit(image, pos, size):
    rpos = mul_ratio(reloc(pos))
    image.blit(rpos[0], rpos[1]-image.height*ratio[1], 0, *mul_ratio(size))


def on_joyaxis_motion(joystick, axis, value):
    if abs(value) > config.joy_analog_treshold:
        print('motion' + str(joystick) + '  ' + str(axis) + '  ' + str(value))


#TODO: joysticks will be needed for activity when lost focus due to game running...
# joysticks = pyglet.input.get_joysticks()
# print(joysticks)
# if not joysticks:
#     print('No se detectaron joysticks!')
# else:
#     for idx, joy in joysticks:
#         print('Joystick detectado #'+str(idx)+': ' + str(joy.device))
#
#         joy.on_joyaxis_motion = on_joyaxis_motion
#         joy.open()


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



def refresh_labels(game_infos):
    for i in range(0, config.names_lines):
        labels[i].text = '¡NO HAY JUEGOS' if not game_infos else game_infos[(selected - config.names_lines // 2 + i) % len(game_infos)]['info']['fullname']



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

def kill_proc():
    if not process:
        return
    print('Terminating previous process')
    print(gui.process)
    gui.process.terminate()
    window.activate()

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0, 0, window.width, window.height)
    ratio_blit(example, config.preview_pos, config.preview_size)
    for label in labels: label.draw()
    if sprite: sprite.draw()
    label_description.draw()

import gui

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        gui.selected = (gui.selected - 1) % len(game_infos)
        refresh_labels(game_infos)
    elif symbol == key.DOWN:
        gui.selected = (gui.selected + 1) % len(game_infos)
        refresh_labels(game_infos)
    elif symbol == key.RETURN:
        kill_proc()
        exec = game_infos[selected]['info']['execute']
        if exec:
            print('Executing ' + game_infos[selected]['info']['execute'])
            try:
                gui.process = subprocess.Popen(game_infos[selected]['info']['execute'])

            except:
                gui.process = None


    print('A key was pressed sym=' + key.symbol_string(symbol) + ' mod=' + key.modifiers_string(modifiers))