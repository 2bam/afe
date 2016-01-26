
# App specific (Don't change unless you really need to


import pyglet
pyglet.font.add_directory('assets/test')

thumb = {
         'filename'         : 'thumb'
        ,'supported_ext'    : ['.png', '.jpg']
        ,'default_path'     : 'assets/test/example_preview.png'
        }

allowed_html_tags = ['b', 'i', 'sub', 'sup', 'br']

info_filename = 'info.xml'

info_defaults = {
     'description'  : ''
    ,'developer'    : ''
    ,'website'      : ''
    ,'year'         : '20XX'
    ,'controls'     : 'No especificado'
    ,'execute'      : ''
}

app_version = '0.1'

inverval_data_sync = 20

preview_pos = 106, 406
preview_size = 508, 293

names_pos = 764, 538        # left-x, center-y
names_font = {
              #'font_name': 'Times New Roman'
              'font_name': 'Nokia Cellphone FC'
              ,'font_size': 22
              ,'color'    : (255, 255, 64, 255)
}

names_lines = 5                 # keep odd
assert names_lines % 2 == 1

names_separation_y = 72
names_central_growth = 7        # font size growth in center of list

joy_analog_treshold = 0.4


def _(x):        # temp for gettext
    return x
