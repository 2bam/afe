import pyglet
import config
import subprocess
from pyglet.window import key
import os
import machine_config as mconf
import sys
import shlex		# for Popen args
import shelve
from config import _

# Open shelf data to compare local versions and save stats
data = shelve.open('argentron_shelf', writeback=True)

# patch missing data
data_defaults = {'total_time': 0}
for __, game in data.items():
	for k, v in data_defaults.items():
		if k not in game:
			game[k] = v


game_infos = None

window = pyglet.window.Window(**mconf.window_size, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS if mconf.faux_fullscreen else pyglet.window.Window.WINDOW_STYLE_DEFAULT)

selected = 0			# Index of selected game list item (game_infos)
process = None		  	# Game process running or None
game_running = None		# 'name' id of game running
last_input = 0			# Seconds since last input from any joystick.

background = pyglet.resource.image('assets/bb/frontend_bg.png')
ratio = window.width/background.width, window.height/background.height
# TODO: also change ratio to font size (e.g. config.names_font.font_size)


def mul_ratio(vec):
	return vec[0]*ratio[0], vec[1]*ratio[1]


def reloc(pos):
	return pos[0], background.height-pos[1]

label_description = pyglet.text.HTMLLabel('Descripcion <b>soporta <i>HTML</i></b><br />'
										  , multiline = True
										  , x = mul_ratio(reloc((46,46)))[0]
										  , y = mul_ratio(reloc((46,46)))[1]
										  , width=580*ratio[0]
										  , height=340*ratio[1]
										  , anchor_y='top')

#label_description.color = (255, 255, 64, 255)
label_description.text += '''
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vitae tortor eget nulla lacinia dictum eu vehicula enim. Etiam id nisi sapien. Curabitur dui tellus, interdum ut mi eget, molestie egestas neque. Morbi sit amet leo vel odio molestie dictum. Nam gravida bibendum nisi, id iaculis mauris cursus et. Fusce tempus, purus sed bibendum efficitur, justo ligula porta metus, et tempus enim leo at ante. Duis rhoncus elit et lacus auctor, ut dignissim nunc rutrum. Phasellus sit amet arcu at arcu dignissim elementum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed finibus lorem sed tristique rutrum. Proin varius euismod augue sit amet elementum. Curabitur semper, metus vel interdum eleifend, lacus magna faucibus purus, quis bibendum massa diam eget massa.
Curabitur placerat suscipit congue. Duis vestibulum urna sed libero sagittis, at ultricies nisi laoreet. Phasellus in velit libero. Praesent ac eros vitae quam dignissim ullamcorper. Ut facilisis nunc et facilisis faucibus. Aliquam rhoncus vestibulum nulla eu rutrum. Duis quis luctus libero. Integer fermentum id quam et pharetra. Integer nec arcu in turpis ultricies tincidunt. Nullam a ante ut magna pellentesque viverra eu sed lectus. Morbi et tortor purus. Praesent scelerisque, eros vel interdum ultricies, diam libero vulputate justo, vel eleifend augue risus id augue.
'''
label_description.text = '<font color="red">' + label_description.text + '</font>'

# Multiply for any screen resoltion and transalte (0,0)@top-left to (0,0)@bottom-left coordinates
def ratio_blit(image, pos, size):
	rpos = mul_ratio(reloc(pos))
	image.blit(rpos[0], rpos[1] - size[1]*ratio[1], 0, *mul_ratio(size))


#TODO: global hook for keyboard/mouse too, to be able to accomodate games/systems that don't use joysticks (C module/dll?)
def on_input(id_text):
	global last_input
	print('Joy input! ' + str(id_text))
	print('Last input ' + str(last_input) + ' seconds ago')
	last_input = 0
	pass

##########################
# Initialize input stuff #
##########################

# Joysticks are needed for activity when lost focus due to game running, and to start the watchdog on exit button press...
joysticks = pyglet.input.get_joysticks()
print(joysticks)
if not joysticks:
	print('uscore')
	print(str(_))
	print('aa')
	print(_('No se detectaron joysticks!'))
else:
	for idx, joy in enumerate(joysticks):
		print(_('Joystick detectado #')+str(idx)+': ' + str(joy.device))

		#joy.on_joyaxis_motion = on_joyaxis_motion

		#Send everything to the same handler (except motion that has a threshold)
		def on_motion(joystick, axis, value):
			if abs(value) > config.joy_analog_treshold:
				on_input(joystick)
		joy.on_joyaxis_motion = on_motion
		joy.on_joyutton_press = lambda joystick, button: on_input(joystick)
		joy.on_joybutton_release = lambda joystick, button: on_input(joystick)
		joy.on_joyhat_motion = lambda joystick, hat_x, hat_y: on_input(joystick)
		joy.open()

####################
# Create gui items #
####################
preview_image = pyglet.resource.image('assets/test/example_preview.png')

# create labels
ratio_names_pos = mul_ratio(reloc(config.names_pos))
labels = []
for i in range(0, config.names_lines):
	norm_pivot = 2 * (i / (config.names_lines-1) - 0.5)	 # fractional value form -1 to 1 according to the index (center should be == 0 for odd config.names_lines)
	pivot = norm_pivot * (config.names_lines-1) / 2		 # pivot relative to the amount of actual lines (used for separation)
	labels.append(pyglet.text.Label('Linea '+str(i)
									, **config.names_font
									, x=ratio_names_pos[0]
									, y=ratio_names_pos[1] - pivot * config.names_separation_y*ratio[1]
									, anchor_x='left', anchor_y='center'
									))
	labels[i].font_size += (1-abs(norm_pivot)) * config.names_central_growth

def refresh_labels(game_infos):
	for i in range(0, config.names_lines):
		labels[i].text = _('¡NO HAY JUEGOS!') if not game_infos else game_infos[(selected - config.names_lines // 2 + i) % len(game_infos)]['fullname']


# GIF test
sprite = None
try:
	animation = pyglet.image.load_animation('assets/test/roboarcade2.gif')
	bin = pyglet.image.atlas.TextureBin()
	animation.add_to_texture_bin(bin)
	sprite = pyglet.sprite.Sprite(animation)
	sprite.scale = 2
except:
	pass




def kill_proc():
	if not process:
		return
	print('Terminating previous process for ' + str(game_running))
	print(gui.process)
	gui.process.terminate()
	on_process_end()


def draw_with_precarious_shadow(label, offset):
	# too slow!

	# col = label.color
	# label.color = (0,0,0,255)
	# label.x -= offset
	# label.y -= offset
	# label.draw()
	# label.color = col
	# label.x += offset
	# label.y += offset
	label.draw()

@window.event
def on_draw():
	window.clear()
	background.blit(0, 0, 0, window.width, window.height)
	ratio_blit(preview_image, config.preview_pos, config.preview_size)
	for label in labels:
		draw_with_precarious_shadow(label, 4)
	if sprite:
		sprite.draw()
	draw_with_precarious_shadow(label_description, 1)


import gui	  #FIXME: this is weird, having to import our own module to access in a function... I'm not that Python savvy. Investigate.

def refresh():
	refresh_labels(game_infos)
	if len(game_infos) > 0:
		sel_game = game_infos[selected]
		gui.preview_image = pyglet.image.load(sel_game['thumb'])
		gui.label_description.text = '''
									 <h1>{info[fullname]} ({info[developer]}, {info[year]})</h1>
									 {info[description]}<br />
									 <h3>Controles</h3>
									 {info[controls]}<br />
									 <br />
									 <u>{info[website]}</u>'''.format(info=sel_game)		#fixme: <u> is shown in black!
		gui.label_description.color = (255,255,255,255)

def on_process_end():
	global game_running
	global process
	print('Game ' + game_running + ' closed. Total accounted runtime: ' + str(data[game_running]['total_time']))
	game_running = None
	process = None
	window.activate()

def do_data_sync(dt):
	data.sync()

def do_checks(dt):
	global last_input
	global process
	global game_running

	if process:
		last_input += dt

		if mconf.timeout_kill_proc and last_input > mconf.timeout_kill_proc:
			kill_proc()

		if gui.process.poll() is not None:
			print(_("El proceso se termino a si mismo. Exit code: ") + str(process.poll()))
			on_process_end()
		else:
			# If game running, count time (within the threshold of no input)
			if last_input <= mconf.timeout_accountability:
				data[game_running]['total_time'] += dt



@window.event
def on_key_press(symbol, modifiers):
	global selected
	global process
	global game_running

	if symbol == key.UP:
		selected = (selected - 1) % len(game_infos)
		refresh()
	elif symbol == key.DOWN:
		selected = (selected + 1) % len(game_infos)
		refresh()
	elif symbol == key.F and (modifiers&key.MOD_ALT) != 0:
		#window.set_fullscreen(not window.fullscreen, **mconf.window_size)
		pass
	elif symbol == key.ESCAPE:
		kill_proc()
		raise SystemExit()
	elif symbol == key.RETURN:
		kill_proc()
		exec = game_infos[selected]['execute']
		if exec:
			exec_dir = os.path.join(mconf.games_folder, game_infos[selected]['name'])
			print(_('Ejecutando [{exe}] con CWD=[{cwd}]').format(exe=exec, cwd=exec_dir))
			exec_list = shlex.split(exec, posix=True)
			exec_list[0] = os.path.join(exec_dir, exec_list[0])
			print(exec_list)
			try:
				#Windows hack: Give focus to window TODO: is this still needed?
				#windows-only
				si = subprocess.STARTUPINFO()
				si.dwFlags = subprocess.STARTF_USESHOWWINDOW
				SW_SHOW = 5
				si.wShowWindow = SW_SHOW

				process = subprocess.Popen(exec_list, cwd=exec_dir, startupinfo=si)
				last_input = 0
				game_running = game_infos[selected]['name']
				# gui.process = subprocess.Popen(exec_path, cwd=exec_dir)
				print(_('OK'))
			except:
				print(_('ERROR AL EJECUTAR: ') + str(sys.exc_info()[0]))
				process = None
				game_running = None

	print('A key was pressed sym=' + key.symbol_string(symbol) + ' mod=' + key.modifiers_string(modifiers))


pyglet.clock.schedule_interval(do_checks, 1.0)
pyglet.clock.schedule_interval(do_data_sync, config.inverval_data_sync)
