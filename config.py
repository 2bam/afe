
# App specific (Don't change unless you really need to


thumb = {
         'filename'         : 'thumb'
        ,'supported_ext'    : ['.png', '.jpg']
        ,'default_path'     : 'assets/example_preview.png'
        }

allowed_html_tags = ['b','i']

info_filename = 'info.xml'

info_defaults = {
     'description'  : ''
    ,'controls'     : 'No especificado'
    ,'execute'      : ''
}

app_version = '0.1'

preview_pos = 84, 184
preview_size = 206, 89

names_pos = 336, 228        # left-x, center-y
names_font = {'font_name': 'Times New Roman',
              'font_size': 24,
              'color'    : (0, 0, 64, 255) }

names_lines = 5                 # keep odd
assert names_lines % 2 == 1

names_separation_y = 25
names_central_growth = 7        # font size growth in center of list

joy_analog_treshold = 0.4

