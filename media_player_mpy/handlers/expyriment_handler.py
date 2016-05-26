from handlers.pygame_handler import PygameHandler
from handlers.opengl_renderer import OpenGLRenderer

class ExpyrimentHandler(OpenGLRenderer, PygameHandler):
	"""
	Handles video frames and input supplied by media_player_gst for the expyriment backend,
	which is based on pygame (with OpenGL in fullscreen mode)
	"""
	def __init__(self, main_player, screen, custom_event_code = None):
		import OpenGL.GL as GL

		# Initialize super c lass
		PygameHandler.__init__(self, main_player, screen, custom_event_code )

		# GL context to use by the OpenGL_renderer class
		self.GL = GL
		self.texid = GL.glGenTextures(1)


	

