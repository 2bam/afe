# Location specific


import ctypes
user32 = ctypes.windll.user32

fullscreen = False           #fixme: for some reason if startin in fullscreen = False and then toggling the fonts and positions are badly placed


#window_size = dict(width=1280, height=720)
window_size = dict(width=user32.GetSystemMetrics(0), height=user32.GetSystemMetrics(1))

machine = { 'name'     : 'ArgentronW'
           ,'code'    : 'AGT'
           ,'location': 'Niceto'
           }

update_folder = './update_folder'
#games_folder = './games_folder'
games_folder = 'C:\developing\PROJECTS\projects16\AFE\games_folder'

