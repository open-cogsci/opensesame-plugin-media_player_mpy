"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.

This module interfaces with the GStreamer framework through the
Python bindings supplied with it. The module enables media playback functionality
in the OpenSesame Experiment buider. In this module's current version, the
GStreamer SDK (from http://www.gstreamer.com) is expected to be
installed at its default location (in windows this is c:\gstreamer-sdk).
If this is not the case in your situation, please change the GSTREAMER_PATH
variable so that it points to the location at which you installed the
GStreamer framework. This plugin should then automatically find all required
libraries and Python modules.
"""

__author__ = "Daniel Schreij"
__license__ = "GPLv3"

# Import Python 3 compatibility functions
from libopensesame.py3compat import *
# Import the required modules.
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception

import os
import time

import mediadecoder

class media_player_mpy(item):
	description = u'Media player based on moviepy'
	
	@property
	def frame_no(self):
		return self.player.current_frame_no

	@property
	def times_played(self):
		return self.player.loop_count
	
	def reset(self):
		"""
		desc:
			Initialize/ reset the plug-in.
		"""
		# Set default experimental variables and values
		self.var.video_src 			= u""
		self.var.duration 			= u"keypress"
		self.var.resizeVideo 		= u"yes"
		self.var.playaudio 			= u"yes"
		self.var.loop 				= u"no"
		self.var.event_handler_trigger = u"on keypress"
		self.var.event_handler 		= u""
		self.var.soundrenderer 		= "sounddevice"

		# Set default internal variables
		self.__frame_updated 		= False

		# Debugging output is only visible when OpenSesame is started with the
		# --debug argument.
		debug.msg(u'media_player_mpy has been initialized!')

	def prepare(self):
		"""
		desc:
			Opens the video file for playback and compiles the event handler
			code.

		returns:
			desc:	True on success, False on failure.
			type:	bool
		"""
		# Call parent functions.
		item.prepare(self)

		# Byte-compile the event handling code (if any)
		if self.var.event_handler.strip() != u"":
			# custom_event_handler = compile(self.var.event_handler, u"<string>", 
			# 	u"exec")
			custom_event_handler = self.python_workspace._compile(self.var.event_handler)
		else:
			custom_event_handler = None

		if self.var.playaudio == u"yes":
			playaudio = True
		else:
			playaudio = False

		# Initialize player object
		self.player = mediadecoder.Decoder(play_audio=playaudio)
		self.player.loop = (self.var.loop == "yes")

		# Load video file to play
		if self.var.video_src == u"":
			raise osexception(u"No video file was set")
		else:
			# Find the full path to the video file. This will point to some
			# temporary folder where the file pool has been placed
			path = self.experiment.get_file(self.var.video_src)

			if not os.path.exists(path):
				raise osexception(u"Invalid path to video file: {0} (file not "
					"found)".format(path))
			# Load the video file. Returns false if this failed
			elif not self.player.load_media(path):
				raise osexception(u"Video file could not be loaded")

		# Set audiorenderer
		if self.var.playaudio == u"yes" and self.player.audioformat:
			if self.var.soundrenderer == u"pygame":
				from mediadecoder.soundrenderers import SoundrendererPygame
				self.audio_handler = SoundrendererPygame(self.player.audioformat)
			elif self.var.soundrenderer == u"pyaudio":
				from mediadecoder.soundrenderers import SoundrendererPyAudio
				self.audio_handler = SoundrendererPyAudio(self.player.audioformat)
			elif self.var.soundrenderer == u"sounddevice":
				from mediadecoder.soundrenderers import SoundrendererSounddevice
				self.audio_handler = SoundrendererSounddevice(self.player.audioformat)

			self.player.set_audiorenderer(self.audio_handler)

		self.vid_size = self.player.clip.size
		self.windowsize = self.experiment.resolution()

		if self.var.resizeVideo == u"yes":
			self.dest_size = self.calculate_scaled_resolution(self.windowsize, 
				self.vid_size)
		else:
			self.dest_size = self.vid_size

		self.vid_pos = ((self.windowsize[0] - self.dest_size[0]) / 2, 
			(self.windowsize[1] - self.dest_size[1]) / 2)

		# Set handler of frames and user input
		if type(self.var.canvas_backend) in [unicode,str]:
			if self.var.canvas_backend == u"legacy" or self.var.canvas_backend \
				== u"droid":
				from handlers import LegacyHandler
				self.handler = LegacyHandler(self, self.experiment.surface, 
					custom_event_handler)
			if self.var.canvas_backend == u"psycho":
				from handlers import PsychopyHandler
				self.handler = PsychopyHandler(self, self.experiment.window, 
					custom_event_handler)
			if self.var.canvas_backend == u"xpyriment":
				# Expyriment uses OpenGL in fullscreen mode, but just pygame
				# (legacy) display mode otherwise
				if self.var.fullscreen:
					from handlers import ExpyrimentHandler
					self.handler = ExpyrimentHandler(self, self.experiment.window, 
						custom_event_handler)
				else:
					from handlers import LegacyHandler
					self.handler = LegacyHandler(self, self.experiment.window, 
						custom_event_handler)
		else:
			# Give a sensible error message if the proper back-end has not been
			# selected
			raise osexception(u"The media_player plug-in could not determine "
				"which backend was used!")

		self.player.set_videoframerender_callback(self.__update_videoframe)

		# Init texture lock to False
		self.texture_locked = False

		# Report success
		return True

	def run(self):
		# Record the timestamp of the plug-in execution.
		self.set_item_onset()
		# Run your plug-in here.

		# Initilialise playback state
		self.paused = False
		keep_playing = True

		self.experiment.cleanup_functions.extend([self.stop, self.close_audio])

		# Set some variables in workspace for easy access in custom script
		self.python_workspace['mov_width'] = self.dest_size[0]
		self.python_workspace['mov_height'] = self.dest_size[1]
		# User can simply call pause() to pause and unpause()
		self.python_workspace['pause'] = self.pause
		
		# Prepare frame renderer in handler for playback
		# (e.g. set up OpenGL context, thus only relevant for OpenGL based 
		# backends)
		self.handler.prepare_for_playback()

		# Start processing loop of audio frames
		self.start_audio()

		### Main player loop. While True, the movie is playing
		start_time = self.experiment.clock.time()
		self.player.play()

		# While video is playing, render frames
		while self.player.status in [mediadecoder.PLAYING, mediadecoder.PAUSED]:
			if self.__frame_updated:
				# Draw current frame to screen
				self.texture_locked = True
				self.handler.process_frame()
				self.texture_locked = False
				# Reset updated flag
				self.__frame_updated = False

			# Draw the frame to backbuffer and show it on the screen
			self.handler.draw_frame()
			self.handler.swap_buffers()

			# #Handle input events
			try:
				if self.event_handler_trigger == "after every frame":
					keep_playing = self.handler.process_user_input_customized()
				else:
					keep_playing = self.handler.process_user_input()
			except osexception as e:
				self.stop()
				self.close_audio()
				raise e

			if not keep_playing:
				self.stop()
				break

			# Determine if playback should continue when a time limit is set
			if type(self.var.duration) == int:
				if self.experiment.clock.time() - start_time > self.var.duration:
					self.stop()
					
			# Without this sleep, the video rendering threard goes haywire...
			time.sleep(0.005)

		# Restore OpenGL context to state before playback
		self.handler.playback_finished()
		self.close_audio()

	def start_audio(self):
		if self.player.audioformat and hasattr(self,'audio_handler'):
			self.audio_handler.start()

	def close_audio(self):
		if self.player.audioformat and hasattr(self,'audio_handler'):
			self.audio_handler.close_stream()
			self.player.audioformat = None

	def calculate_scaled_resolution(self, screen_res, image_res):
		"""Calculate image size so it fits the screen
		Arguments:
		screen_res  --  Tuple containing display window size/Resolution
		image_res   --  Tuple containing image width and height

		Returns:
		(width, height) tuple of image scaled to window/screen
		"""

		rs = screen_res[0]/float(screen_res[1])
		ri = image_res[0]/float(image_res[1])

		if rs > ri:
			return (int(image_res[0] * screen_res[1]/image_res[1]), screen_res[1])
		else:
			return (screen_res[0], int(image_res[1]*screen_res[0]/image_res[0]))

	def __render_audioframe(self, frame):
		self.audio_handler.write(frame)

	def __update_videoframe(self, frame):
		if not self.texture_locked:
			self.handler.handle_videoframe(frame)
			self.__frame_updated = True

	def stop(self):
		self.player.stop()

	def pause(self):
		if self.player.status == mediadecoder.PAUSED:
			self.player.pause()
			self.paused = False
		elif self.player.status == mediadecoder.PLAYING:
			self.player.pause()
			self.paused = True


class qtmedia_player_mpy(media_player_mpy, qtautoplugin):
	def __init__(self, name, experiment, script=None):
		# Call parent constructors.
		media_player_mpy.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

		# Connect playaudio value change to function that enables or disables
		# sound renderer selection.
		# Account for Qt4/5 inconsistency here
		
		try:
			self.play_audio.currentTextChanged.connect(self.set_soundrenderer_status)
		except:
			self.play_audio.editTextChanged.connect(self.set_soundrenderer_status)
		
		# Init the setting for when the experiment is loaded.
		if self.var.playaudio == "yes":
			self.sound_renderer.setDisabled(False)
		elif self.var.playaudio == "no":
			self.sound_renderer.setDisabled(True)

		# Issue a warning if user selects options that potentially cause an infinite
		# loop
		try:
			self.loop_video.currentTextChanged.connect(self.check_for_infinite_loops)
		except:
			self.loop_video.editTextChanged.connect(self.check_for_infinite_loops)

		self.line_edit_duration.editingFinished.connect(self.check_for_infinite_loops)
		self.check_available_soundrenderers()

	def set_soundrenderer_status(self, value):
		""" Enables or disables the soundrenderer combo box, depending on the
		selection of playaudio."""

		if value == "yes":
			self.sound_renderer.setDisabled(False)
		elif value == "no":
			self.sound_renderer.setDisabled(True)

	def check_available_soundrenderers(self):
		""" Removes sound renderes that are not available on the system."""
		try:
			import pygame
		except:
			i = self.sound_renderer.findText('pygame')
			if i != -1:
				self.sound_renderer.removeItem(i)

		try:
			import pyaudio
		except:
			i = self.sound_renderer.findText('pyaudio')
			if i != -1:
				self.sound_renderer.removeItem(i)

		try:
			import sounddevice
		except:
			i = self.sound_renderer.findText('sounddevice')
			if i != -1:
				self.sound_renderer.removeItem(i)

	def check_for_infinite_loops(self, value=None):
		loop_value = self.loop_video.currentText()
		duration_value = self.line_edit_duration.text()

		if loop_value == "yes" and duration_value == "sound":
			self.extension_manager.fire('notify', 
				message = '<strong>Warning</strong>: With the current combination'
				' of <em>loop</em> and <em>duration</em> settings the video will'
				' play forever',
				category = 'warning',
				timeout = 10000,
				always_show = True)




		


