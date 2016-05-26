from handlers.pygame_handler import PygameHandler
import pygame

class LegacyHandler(PygameHandler):
	"""
	Handles video frames and input supplied by media_player_gst for the legacy backend, which is based on pygame
	"""

	def __init__(self, main_player, screen, custom_event_code = None):
		"""
		Constructor. Set variables to be used in rest of class.

		Arguments:
		main_player -- reference to the main_player_gst object (which should instantiate this class)
		screen -- reference to the pygame display surface

		Keyword arguments:
		custom_event_code -- (Compiled) code that is to be called after every frame
		"""
		# Call constructor of super class
		super(LegacyHandler, self).__init__(main_player, screen, custom_event_code )
		# Surface that is a 1:1 representation of the numpy array in which the frame is delivered		
		self.src_surface = pygame.Surface(self.main_player.vid_size, 0, 24, (255, 65280, 16711680, 0))
		self.src_surface.set_alpha(None)
		# Surface that is scaled to the destination size in which the frame is to be presented (if video has to be resized to full-screen)
		self.dest_surface = pygame.Surface(self.main_player.dest_size, 0, 24, (255, 65280, 16711680, 0))
		self.dest_surface.set_alpha(None)

	def prepare_for_playback(self):
		"""
		Setup screen for playback (Just fills the screen with the background color for this backend)
		"""
		# Fill surface with background color
		self.screen.fill(pygame.Color(str(self.main_player.experiment.background)))
		self.screen.set_alpha(None)
		self.last_drawn_frame_no = 0

	def process_frame(self):
		"""
		Does the actual rendering of the buffer to the screen
		"""
		if hasattr(self,"frame") and not self.frame is None:
			# Only draw each frame to screen once, to give the pygame (software-based) rendering engine
			# some breathing space

			if self.last_drawn_frame_no != self.main_player.frame_no:
				# t1 = time.time()
				pygame.surfarray.blit_array(self.src_surface, self.frame.swapaxes(0,1))
				# stage1 = (time.time()-t1)*1000
				# print("Blitting np array took {} ms".format(stage1))
				
				if self.main_player.var.resizeVideo == u"yes":
					# t1 = time.time()
					pygame.transform.scale(self.src_surface, self.main_player.dest_size, self.dest_surface)
					# stage2 = (time.time()-t1)*1000
					# print("Transforming took {} ms".format(stage2))
					# If resize option is selected, resize frame to screen/window dimensions and blit
					
					# t1 = time.time()
					self.screen.blit(self.dest_surface.convert(), self.main_player.vid_pos)
					# stage3 = (time.time()-t1)*1000
					# print("Blitting to screen took {} ms".format(stage3))
				else:
				# In case movie needs to be displayed 1-on-1 blit directly to screen
					self.screen.blit(self.src_surface, self.main_player.vid_pos)
				# print("------------------------------------")
				# print("Total {} ms".format(stage1 + stage2 + stage3))
				# print("====================================")
				self.last_drawn_frame_no = self.main_player.frame_no

