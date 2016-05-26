import pyglet

import logging
logger = logging.getLogger(__name__)
# Catch this, because otherwise sphinx will crash when creating documentation.
try:
	from libopensesame.exceptions import osexception
except:
	logger.debug('Could not import osexception')

import numpy as np

class OpenGLRenderer(object):
	"""
	Superclass for both the expyriment and psychopy handlers. Both these backends
	are OpenGL based and basically have the same drawing routines.
	By inheriting from this class, they only need to be defined once in here.
	"""

	def __init__(self):
		raise osexception("This class should only be subclassed on not be instantiated directly!")

	def prepare_for_playback(self):
		"""Prepares the OpenGL context for playback"""
		GL = self.GL

		# Prepare OpenGL for drawing
		GL.glPushMatrix()		# Save current OpenGL context
		GL.glLoadIdentity()

		# Set screen coordinates to useful values for movie playback (per pixel coordinates)
		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glPushMatrix()
		GL.glLoadIdentity()
		GL.glOrtho(0.0,  self.main_player.experiment.width,  
			self.main_player.experiment.height, 0.0, 0.0, 1.0)
		GL.glMatrixMode(GL.GL_MODELVIEW)

		# Create black empty texture to start with, to prevent artifacts
		img = np.zeros([self.main_player.vid_size[0], 
			self.main_player.vid_size[1],3], dtype=np.uint8)
		img.fill(0)

		GL.glEnable(GL.GL_TEXTURE_2D)
		GL.glBindTexture(GL.GL_TEXTURE_2D, self.texid)
		GL.glTexImage2D( GL.GL_TEXTURE_2D, 0, 
			GL.GL_RGB, self.main_player.vid_size[0], self.main_player.vid_size[1], 
			0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img.tostring())
		GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
		GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)

		GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
		self.frameQuadID = self.create_quad()

	def create_quad(self):
		""" Create a display list drawing a quad to display the texture on """
		GL = self.GL

		(x, y) = self.main_player.vid_pos
		(w, h) = self.main_player.dest_size

		x, y = int(x), int(y)
		w, h = int(w), int(h)

		frameQuadID = GL.glGenLists(1);
		GL.glNewList(frameQuadID, GL.GL_COMPILE)
		GL.glBegin(GL.GL_QUADS)
		GL.glTexCoord2f(0.0, 0.0)
		GL.glVertex3i(x, y, 0)
		GL.glTexCoord2f(1.0, 0.0)
		GL.glVertex3i(x+w, y, 0)
		GL.glTexCoord2f(1.0, 1.0)
		GL.glVertex3i(x+w, y+h, 0)
		GL.glTexCoord2f(0.0, 1.0)
		GL.glVertex3i(x, y+h, 0)
		GL.glEnd()
		GL.glEndList()
		return frameQuadID

	def playback_finished(self):
		""" Restore previous OpenGL context as before playback """
		GL = self.GL

		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glPopMatrix()
		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glPopMatrix()

	def process_frame(self):
		"""
		Does the actual rendering of the buffer to the screen
		"""
		GL = self.GL

		# Get desired format from main player
		(w,h) = self.main_player.dest_size
		(x,y) = self.main_player.vid_pos

		# Frame should blend with color white
		GL.glColor4f(1,1,1,1)

		# Only if a frame has been set, blit it to the texture
		if hasattr(self,"frame") and not self.frame is None:
			if GL is pyglet.gl:
				img_data = self.frame.ctypes
			else:
				img_data = self.frame

			GL.glLoadIdentity()
			GL.glTexSubImage2D( 
				GL.GL_TEXTURE_2D, 0, 0, 0, 
				#self.main_player.vid_size[0], self.main_player.vid_size[1], 
				self.frame.shape[1], self.frame.shape[0],
				GL.GL_RGB, GL.GL_UNSIGNED_BYTE, 
				img_data)

	def draw_frame(self):
		""" Draw the quad of which the frame is the texture """
		GL = self.GL
		# Clear The Screen And The Depth Buffer
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
		# Bind the texture
		GL.glBindTexture(GL.GL_TEXTURE_2D, self.texid)
		# Draw the quad containing the texture
		GL.glCallList(self.frameQuadID)
		# Make sure there are no pending drawing operations and flip front and backbuffer
		GL.glFlush()
