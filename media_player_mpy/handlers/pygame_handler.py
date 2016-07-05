import pygame

import logging
logger = logging.getLogger(__name__)
# Catch this, because otherwise sphinx will crash when creating documentation.
try:
	from libopensesame.exceptions import osexception
except:
	logger.debug('Could not import osexception')


class PygameHandler(object):
	"""
	Superclass for both the legacy and expyriment hanlders. Both these backends are based on pygame, so have
	the same event handling methods, which they can both inherit from this class.
	"""

	def __init__(self, main_player, screen, custom_event_code = None):
		"""
		Constructor. Set variables to be used in rest of class.

		Arguments:
		main_player -- reference to the main_player_gst object (which instantiates this class or its sublass)
		screen -- reference to the pygame display surface

		Keyword arguments:
		custom_event_code -- (Compiled) code that is to be called after every frame
		"""
		self.main_player = main_player
		self.screen = screen
		self.custom_event_code = custom_event_code

	def handle_videoframe(self, frame):
		"""
		Callback method for handling a video frame

		Arguments:
		frame - the video frame supplied as a str/bytes object
		"""
		self.frame = frame

	def draw_frame(self):
		"""Dummy function - the drawing of the frame happens elsewhere for pygame"""
		pass

	def swap_buffers(self):
		"""
		Flips back and front buffers
		"""
		pygame.display.flip()

	def prepare_for_playback(self):
		"""
		Dummy function (to be implemented in OpenGL based subclasses like expyriment)
		This function should prepare the context of OpenGL based backends for playback
		"""
		pass

	def playback_finished(self):
		"""
		Dummy function (to be implemented in OpenGL based subclasses like expyriment)
		This function should restore OpenGL context to as it was before playback
		"""
		pass

	def process_user_input(self):
		"""
		Process events from input devices

		Returns:
		True -- if no key/mouse button has been pressed or if custom event code returns True
		False -- if a keypress or mouse click was detected (an OS indicates playback should be stopped then
			or custom event code has returned False
		"""
		# By default, continue playback
		keep_playing = True
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				# Catch escape presses
				if event.key == pygame.K_ESCAPE:
					self.main_player.pause()
					self.main_player.experiment.pause()
					self.main_player.pause()
				else:
					# Check if user has entered custom event code. If duration is set
					# to keypress or mouseclick, exit anyway.
					if self.custom_event_code != None:
						keep_playing = self.process_user_input_customized(("key", 
							pygame.key.name(event.key)))
						
					# Stop experiment on keypress (if indicated as stopping method)
					if self.main_player.duration == u"keypress":
						self.main_player.experiment.response = pygame.key.name(event.key)
						self.main_player.experiment.end_response_interval = pygame.time.get_ticks()
						return False

			if event.type == pygame.MOUSEBUTTONDOWN:
				# Stop experiment on mouse click (if indicated as stopping method)
				if self.custom_event_code != None:
					keep_playing = self.process_user_input_customized(("mouse", event.button))

				if self.main_player.duration == u"mouseclick":
					self.main_player.experiment.response = event.button
					self.main_player.experiment.end_response_interval = pygame.time.get_ticks()
					return False

		pygame.event.pump()
		return keep_playing

	def process_user_input_customized(self, event=None):
		"""
		Allows the user to insert custom code. Code is stored in the event_handler variable.

		Arguments:
		event -- a tuple containing the type of event (key or mouse button press)
			   and the value of the key or mouse button pressed (which character or mouse button)
		"""

		# Listen for escape presses and collect keyboard and mouse presses if no event has been passed to the function
		# If only one button press or mouse press is in the event que, the resulting event variable will just be a tuple
		# Otherwise the collected event tuples will be put in a list, which the user can iterate through with his custom code
		# This way the user will have either
		#  1. a single tuple with the data of the event (either collected here from the event que or passed from process_user_input)
		#  2. a list of tuples containing all key and mouse presses that have been pulled from the event queue

		if event is None:
			events = pygame.event.get()
			event = []  # List to contain collected info on key and mouse presses
			for ev in events:
				if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
					self.main_player.playing = False
					raise osexception(u"The escape key was pressed")
				elif ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
					# Exit on ESC press
					if ev.type == pygame.KEYDOWN:
						event.append(("key", pygame.key.name(ev.key)))
					elif ev.type == pygame.MOUSEBUTTONDOWN:
						event.append(("mouse", ev.button))
			# If there is only one tuple in the list of collected events, take it out of the list
			if len(event) == 1:
				event = event[0]

		continue_playback = True

		# Variables for user to use in custom script
		try:
			self.main_player.python_workspace['continue_playback'] = True
			self.main_player.python_workspace['frame'] = self.main_player.frame_no
			self.main_player.python_workspace['times_played'] = self.main_player.times_played
			self.main_player.python_workspace['paused'] = self.main_player.paused
			self.main_player.python_workspace['event'] = event
		except Exception as e:
			raise osexception("Error assigning variables in media_player: {}".format(e))

		# Add more convenience functions?

		try:
			self.main_player.python_workspace._exec(self.custom_event_code)
		except Exception as e:
			self.main_player.playing = False
			raise osexception(u"Error while executing event handling code: %s" % e)

		# Get potentially altered value of continue_playback from the workspace
		continue_playback = self.main_player.python_workspace['continue_playback']
		if type(continue_playback) != bool:
			continue_playback = False

		pygame.event.pump()
		return continue_playback
