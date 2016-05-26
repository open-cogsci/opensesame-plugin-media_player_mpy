import psychopy
import time
from handlers.opengl_renderer import OpenGLRenderer

import logging
logger = logging.getLogger(__name__)
# Catch this, because otherwise sphinx will crash when creating documentation.
try:
	from libopensesame.exceptions import osexception
except:
	logger.debug('Could not import osexception')

class PsychopyHandler(OpenGLRenderer):
	"""
	Handles video frames and input for the psychopy backend supplied by media_player_gst
	Based on OpenGL so inherits from the OpenGL_renderer superclass
	"""
	def __init__(self, main_player, screen, custom_event_code = None):
		"""
		Constructor. Set variables to be used in rest of class.

		Arguments:
		main_player -- reference to the main_player_gst object (which should instantiate this class)
		screen -- reference to the psychopy display surface

		Keyword arguments:
		custom_event_code -- (Compiled) code that is to be called after every frame
		"""
		import ctypes
		import pyglet.gl

		self.main_player = main_player
		self.win = screen
		self.mouse = psychopy.event.Mouse(visible=False, win=screen)
		self.frame = None
		self.custom_event_code = custom_event_code

		# GL context to be used by the OpenGL_renderer class
		# Create texture to render frames to later
		GL = self.GL = pyglet.gl
		self.texid = GL.GLuint()
		GL.glGenTextures(1, ctypes.byref(self.texid))

	def handle_videoframe(self, frame):
		"""
		Callback method for handling a video frame

		Arguments:
		frame - the video frame supplied as a str/bytes object
		"""
		self.frame = frame

	def process_frame(self):
		""" Pretty weird, but psychopy only has correct video playback after a
		frame has been processed, and doesn't allow intermediate buffer swaps.
		These result in a black screen, making the movie flicker. Just do everything
		at once here then. """

		super(PsychopyHandler, self).process_frame()
		super(PsychopyHandler, self).draw_frame()
		self.win.flip()

	def swap_buffers(self):
		"""Flip buffer to screen. Done in process_frame()"""
		pass

	def process_user_input(self):
		"""
		Process events from input devices

		Returns:
		True -- if no key/mouse button has been pressed or if custom event code returns True
		False -- if a keypress or mouse click was detected (an OS indicates playback should be stopped then
			or custom event code has returned False
		"""
		pressed_keys = psychopy.event.getKeys()

		for key in pressed_keys:
			# Catch escape presses
			if key == "escape":
				self.main_player.stop()
				raise osexception("The escape key was pressed")

			if self.custom_event_code != None:
				return self.process_user_input_customized(("key", key))
			elif self.main_player.duration == u"keypress":
				self.main_player.experiment.response = key
				self.main_player.experiment.end_response_interval = time.time()
				return False

		if self.main_player.duration == u"mouseclick":
			pressed_mouse_buttons = self.mouse.getPressed()
			if pressed_mouse_buttons != [0, 0, 0]:
				self.main_player.experiment.response = pressed_mouse_buttons
				self.main_player.experiment.end_response_interval = time.time()
				return False

		return True

	def process_user_input_customized(self, event=None):
		"""
		Allows the user to insert custom code. Code is stored in the event_handler variable.

		Arguments:
		event -- a tuple containing the type of event (key or mouse button press)
			   and the value of the key or mouse button pressed (which character or mouse button)
		"""

		if event is None:
			events = psychopy.event.getKeys()
			event = []  # List to contain collected info on key and mouse presses
			for key in events:
				if key == "escape":
					self.main_player.playing = False
					raise osexception(u"The escape key was pressed")
				else:
					event.append(("key", key))

			# If there is only one tuple in the list of collected events, take it out of the list
			if len(event) == 1:
				event = event[0]


		continue_playback = True

		# Variables for user to use in custom script
		exp = self.main_player.experiment
		frame = self.main_player.frame_no
		mov_width = self.main_player.destsize[0]
		mov_height = self.main_player.destsize[1]
		times_played = self.main_player.times_played

		# Easily callable pause function
		# Use can now simply call pause() to pause and unpause()
		paused = self.main_player.paused
		pause = self.main_player.pause

		# Add more convenience functions?

		# Execute custom code
		try:
			exec(self.custom_event_code)
		except Exception as e:
			self.main_player.playing = False
			raise osexception(u"Error while executing event handling code: %s" % e)

		# if continue_playback has been set to anything else than True or False, then stop playback
		if type(continue_playback) != bool:
			continue_playback = False

		return continue_playback

	def draw_frame(self):
		""" Draw the frame - Done in process_frame() """
		pass
