import pygame


class Laser:

	def __init__(self, screen):
		self.screen = screen
		# import and scale image
		self.image = pygame.image.load("images/alien_laser.png")
		self.image = pygame.transform.scale(self.image, (4, 25))
		# place initially off screen
		self.Y = -50
		self.X = -50
		# variable for state of primed or firing
		self.state = "primed"


	def blit(self):
		# blit on screen
		self.screen.blit(self.image, (self.X, self.Y))