# Location specific

import os
import ctypes
user32 = ctypes.windll.user32

#NOTE: We use a false fullscreen because fixme: for some reason if startin in fullscreen = False and then toggling the fonts and positions are badly placed
faux_fullscreen = True


if faux_fullscreen:
    window_size = dict(width=user32.GetSystemMetrics(0), height=user32.GetSystemMetrics(1))
else:
    window_size = dict(width=1280, height=720)

machine = { 'name'     : 'ArgentronW'
           ,'code'    : 'AGT'
           ,'location': 'Niceto'
           }

update_folder = os.path.abspath('update_folder')            # Source folder for compressed packages. Must be absolute
games_folder = os.path.abspath('games_folder')              # Destination folder for uncompressed games. Must be absolute


