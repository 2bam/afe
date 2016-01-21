
#TODO: Also update IDE (except for update.py)
#TODO: if "kill" file found in directory, remove the game from shelf and path

import machine_config as mconf
import shelve
import os
import re
import zipfile
import sys

# Open shelf data to compare local versions
data = shelve.open('argentron_shelf', writeback=True)

# http://stackoverflow.com/a/1714190
def normalize_ver_string(v):
    return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]


supported_ext = ['.zip']
for subdir, dirs, _ in os.walk(mconf.update_folder):
    for game_name in dirs:

        print(_('\nProcesando: {game})').format(game=game_name))
        dir = os.path.join(subdir, game_name)

        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and os.path.splitext(f)[1] in supported_ext]

        if not files:
            print(_('Directorio vacio para juego {game}: ').format(game=game_name))
        else:
            #extract version numbers and fill game_list with (version-list, fullpath) tuple
            game_list = []
            for f in files:
                noext = os.path.splitext(f)[0]
                veridx = noext.rfind('_')
                if veridx >= 0:
                    file_ver = noext[veridx+1:]
                else:
                    file_ver = '0'      #cant find version, make it 0
                # print('version  '+str(file_ver)+'  ')
                game_list.append({'version': normalize_ver_string(file_ver), 'path': os.path.normpath(os.path.join(dir, f))})

            #sort by version-list
            game_list.sort(key=lambda x: x['version'], reverse=True)

            print(_('Ultima version encontrada: {version!s}').format(game_list[0]['version']))

            try:
                target_dir = os.path.normpath(os.path.join(mconf.games_folder, game_name))
                try:
                    os.makedirs(target_dir)
                except:
                    pass    #usually from 'already exists'

                if game_name in data:
                    if game_list[0]['version'] == data[game_name]['version']:
                        print(game_name + ' está al día')
                    else:
                        #UPDATE
                        zip = zipfile.ZipFile(game_list[0]['path'])
                        #fixme: extractall vulnerability?
                        #TODO: just uncompress files over old one or nuke it first?
                        zip.extractall(target_dir)
                        print(game_name + ' ' + ('upgraded' if game_list[0]['version'] > data[game_name]['version'] else 'downgraded') + ' de version' + str(data[game_name]['version']) +' a '+ str(game_list[0]['version']))
                else:
                    #INSTALL
                    zip = zipfile.ZipFile(game_list[0]['path'])
                    #fixme: extractall vulnerability?
                    zip.extractall(target_dir)
                    data[game_name] = {}
                    print(game_name + ' instalado version ' + str(game_list[0]['version']))


                data[game_name]['version'] = game_list[0]['version']
            except:
                print(_('No se pudo descomprimir {path} correctamente').format(path=game_list[0]['path']))
                print(sys.exc_info()[0])


data.close()
#call('afe.py')