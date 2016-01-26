# Location specific

import os
import ctypes

# NOTE: We use a false fullscreen because real fullscreen stays always-on-top, covering games
faux_fullscreen = True

if faux_fullscreen:
	window_size = dict(width=ctypes.windll.user32.GetSystemMetrics(0), height=ctypes.windll.user32.GetSystemMetrics(1))		#windows-only
else:
	window_size = dict(width=1280, height=720)

machine = { 'name': 'ArgentronW'
		  , 'code': 'AGT'
		  , 'location': 'Niceto'
		  }

update_folder = os.path.abspath('update_folder')  # Source folder for compressed packages. Must be absolute path.
games_folder = os.path.abspath('games_folder')  # Destination folder for uncompressed games. Must be absolute path.

timeout_kill_proc = 90				# Seconds of inactivity until the program kills the game process for no input. 'None' to disable timeout. Suggested 90 for party venues
timeout_attract_mode = 90			# Seconds of inactivity until the attract mode video is started (if configured)
timeout_accountability = 10			# Seconds after no input time to stop counting time for the game's stats
