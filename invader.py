import pygame


class Invader:

	def __init__(self, screen, inv_type, value,  x, y, column):
		# initiate each invader from passed-in values of type,
		# score value, coordinates and which column they will occupy
		self.screen = screen
		self.value = value
		if inv_type == "green":
			self.image1 = pygame.image.load("images/invader_green_1.png")
			self.image2 = pygame.image.load("images/invader_green_2.png")
		elif inv_type == "yellow":
			self.image1 = pygame.image.load("images/invader_yellow_1.png")
			self.image2 = pygame.image.load("images/invader_yellow_2.png")
		elif inv_type == "pink":
			self.image1 = pygame.image.load("images/invader_pink_1.png")
			self.image2 = pygame.image.load("images/invader_pink_2.png")
		self.explosion1 = pygame.image.load("images/explosion_1.png")
		self.explosion2 = pygame.image.load("images/explosion_2.png")
		self.image1 = pygame.transform.scale(self.image1, (40, 25))
		self.image2 = pygame.transform.scale(self.image2, (40, 25))
		self.explosion1 = pygame.transform.scale(self.explosion1, (40, 25))
		self.explosion2 = pygame.transform.scale(self.explosion2, (40, 25))
		# for monitoring which image of animation is currently showing
		self.first_image = True
		# iterator for regulating animation speed
		self.change_count = 0
		# coordinates
		self.X = x
		self.Y = y
		# move distance
		self.move = 1
		# speed of movement
		self.speed = 0.3
		# how much to drop at the edges of screen
		self.drop = 3
		# variable for determining which invader
		# to replace deleted invader in shooter list
		self.column = column

	def move_invader(self):
		# moves invader
		self.X += self.move * self.speed

	def blit(self):
		self.move_invader()
		# change from first image to second image by evaluating self.first_image
		if self.first_image:
			self.screen.blit(self.image2, (self.X, self.Y))
			# after change count reaches 100, switch and reset conditions
			if self.change_count >= 100:
				self.first_image = False
				self.change_count = 0
		# change from second image back to first by evaluating self.first_image
		elif not self.first_image:
			self.screen.blit(self.image1, (self.X, self.Y))
			# after change count reaches 100, switch and reset conditions
			if self.change_count >= 100:
				self.first_image = True
				self.change_count = 0
				# returns true if invader has been hit and is
				# on second explosion image
				if self.image2 == self.explosion2:
					return True
		# regulation of animation speed
		self.change_count += self.speed * 5
