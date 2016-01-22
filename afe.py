#import window
import config
import machine_config as mconf
import os
import xml.etree.ElementTree as ElementTree
import pyglet

print('''
    *************************************************
    Arrancando Argentron Front End v{app_version}
    Creado por Martin Sebastian Wain

    Maquina     {machine[name]}
    Codigo      {machine[code]}
    Ubicacion   {machine[location]}
    *************************************************
    '''.format(app_version=config.app_version, machine=mconf.machine))

try:
    os.makedirs(mconf.games_folder)
except:
    pass

def load_game_info(game_name):
    info = {}

    #find screenshot
    dir = os.path.join(mconf.games_folder, game_name)
    for f in os.listdir(dir):
        abs_path = os.path.join(dir, f)
        if os.path.isfile(abs_path):
            splat = os.path.splitext(f)
            if splat[0] == config.thumb['filename'] and splat[1] in config.thumb['supported_ext']:
                info['thumb'] = os.path.normpath(abs_path)
    if not 'thumb' in info:
        info['thumb'] = config.thumb['default_path']

    # 'name' is the codename/directory name
    info['name'] = game_name

    # defaults just in case...
    info['fullname'] = game_name
    for key, value in config.info_defaults.items():
        info[key] = value

    info_path = os.path.normpath(os.path.join(dir, config.info_filename))
    if os.path.exists(info_path) and os.path.isfile(info_path):
        try:
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
        except:
            print('Error cargando "' + info_path + '", usando valores estandar')

    return info

game_infos = []
dirs = [item for item in os.listdir(mconf.games_folder) if os.path.isdir(os.path.join(mconf.games_folder, item))]
for game_name in sorted(dirs):
    print("Game found:"+game_name)
    game_infos.append(load_game_info(game_name))

import gui

gui.game_infos = game_infos
gui.refresh()

#test
#os.popen(game_infos[0]['execute'])


pyglet.app.run()
