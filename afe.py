#import window
import config
import machine_config as mconf
import os
import xml.etree.ElementTree as ElementTree
import pyglet

def load_game_info(game_name):
    info = {}

    #find screenshot
    dir = os.path.join(mconf.games_folder, game_name)
    for root, dirs, files in os.walk(dir):
        for f in files:
            split = os.path.splitext(f)
            if split[0] == config.thumb['filename'] and split[1] in config.thumb['supported_ext']:
                info['thumb'] = os.path.normpath(os.path.join(root, f))
    if not 'thumb' in info:
        info['thumb'] = config.thumb['default_path']

    #defaults por las dudas
    info['fullname'] = game_name
    for key, value in config.info_defaults.items():
        info[key] = value

    info_path = os.path.normpath(os.path.join(dir, config.info_filename))
    if os.path.exists(info_path) and os.path.isfile(info_path):
        #try:
            xroot = ElementTree.parse(info_path).getroot()

            for key in ('fullname', *config.info_defaults.keys()):
                tag = xroot.find(key)
                if tag is not None:
                    info[key] = tag.text
                    for sub in tag:
                        if sub.tag in config.allowed_html_tags:
                            info[key] += str(ElementTree.tostring(sub))
                        else:
                            info[key] += '' or sub.tail
        #except:
        #    print('Error cargando "' + info_path + '", usando valores estandar')

    return info

game_infos = []
for root, dirs, files in os.walk(mconf.games_folder):
    for game_name in sorted(list(dirs)):
        game_infos.append({'name':game_name, 'info':load_game_info(game_name)})

import gui

gui.game_infos = game_infos
gui.refresh_labels(game_infos)

#test
#os.popen(game_infos[0]['info']['execute'])


pyglet.app.run()
