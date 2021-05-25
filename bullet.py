import pygame


class Bullet:

	def __init__(self, screen):
		self.screen = screen
		self.image = pygame.image.load("images/shooter_bullet.png")
		self.image = pygame.transform.scale(self.image, (4, 25))
		# off screen coordinates
		self.Y = 600
		self.X = -50
		# state for removing bullet from screen
		self.hit = False
		# speed of bullet
		self.move = - 4
		# variable for storing state of firing or loaded
		self.state = "loaded"


	def blit(self):
		# blit bullet on screen and check if reset is needed
		self.check_for_reset()
		self.screen.blit(self.image, (self.X, self.Y))


	def check_for_reset(self):
		# if bullet goes off screen or has a collision, reset it
		if self.Y <= 0 or self.hit:
			self.Y = 600
			self.X = -50
			self.state = "loaded"
			self.hit = False
