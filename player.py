import pygame


class Player:

	def __init__(self, screen):
		self.screen = screen
		# load and resize main image
		self.primary_image = pygame.image.load("images/shooter.png")
		self.primary_image = pygame.transform.scale(self.primary_image, (40, 25))
		self.image = self.primary_image
		self.explosion1 = pygame.image.load("images/shooter_explosion1.png")
		self.explosion2 = pygame.image.load("images/shooter_explosion2.png")
		self.explosion1 = pygame.transform.scale(self.explosion1, (40, 25))
		self.explosion2 = pygame.transform.scale(self.explosion2, (40, 25))
		# initial coordinates
		self.X = 280
		self.Y = 600
		# for changing move direction
		self.distance = 2
		# how much player is moving
		self.move = 0
		self.lives = 3
		# store state of hit or not hit
		self.hit = False
		# regulates explosion animation
		self.change_count = 0
		# speed player can move
		self.speed = 0.3

	def blit(self):
		# moves on each loop according to value of self.move
		self.X += self.move
		# stop player moving off screen
		if self.X >= 560:
			self.X = 560
		if self.X <= 0:
			self.X = 0
		# check and handle explosions
		self.explosion()
		# blit player
		self.screen.blit(self.image, (self.X, self.Y))
		self.display_lives()

	def explosion(self):
		if self.hit:
			# check if explosion animation has started and
			# if not change to first explosion image
			if self.image == self.primary_image:
				self.image = self.explosion1
				# start animation counter
				self.change_count = 0
			# if already on first explosion image, change to second
			if self.image != self.primary_image and self.change_count >= 50:
				self.image = self.explosion2
			# if on second explosion image, reset player
			if self.image == self.explosion2 and self.change_count >= 100:
				self.image = self.primary_image
				self.X = 300
				self.hit = False
				return True
			# regulates animation speed
			self.change_count += self.speed * 10


	def go_left(self):
		self.move = -self.distance

	def go_right(self):
		self.move = self.distance

	def stop(self):
		# stop movement by setting self.move to 0
		self.move = 0

	def display_lives(self):
		# blit main image, bottom left according to number of lives left
		if self.lives > 2:
			self.screen.blit(self.primary_image, (113, 660))
		if self.lives > 1:
			self.screen.blit(self.primary_image, (63, 660))
		if self.lives > 0:
			self.screen.blit(self.primary_image, (13, 660))
