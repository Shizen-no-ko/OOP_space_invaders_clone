import pygame
from random import choice
import math


class MotherShip:

	def __init__(self, screen):
		self.screen = screen
		self.value = 200
		# usual image state of mother ship
		self.main_image = pygame.image.load("images/mother_ship.png")
		self.main_image = pygame.transform.scale(self.main_image, (80, 25))
		self.image = self.main_image
		# images for explosion animation
		self.explosion1 = pygame.image.load("images/mother_explosion_1.png")
		self.explosion2 = pygame.image.load("images/mother_explosion_2.png")
		self.explosion1 = pygame.transform.scale(self.explosion1, (80, 25))
		self.explosion2 = pygame.transform.scale(self.explosion2, (80, 25))
		# initial coordinates
		self.X = 615
		self.Y = 70
		# iterator for delaying stages of explosion animation
		self.change_count = 0
		# self.first_image = True
		# toggle switch for movement of mother ship
		self.moving = False
		# move steps
		self.move = -2
		# movement speed
		self.speed = 0.3
		# state of being shot or not
		self.shot = False
		# tracker for switching soundtrack files in game loop
		self.sound_loaded = False

	def move_mother(self):
		# moves mother ship across screen and
		# checks if gone off left edge and resets accordingly
		if self.moving:
			self.X += self.move * self.speed
			if self.X <= -80:
				self.reset_mother()
				return

	def reset_mother(self):
		# reset mother ship to initial conditions
		self.image = self.main_image
		self.X = 615
		self.shot = False
		self.moving = False

	def start_moving(self):
		# start mother ship moving across the screen
		self.moving = True

	def blit(self):
		self.random_launch()
		self.move_mother()
		self.screen.blit(self.image, (self.X, self.Y))
		if self.shot:
			# changes image to first explosion image
			# and resets counter for next change
			if self.image == self.main_image:
				self.image = self.explosion1
				self.change_count = 0
			# changes image to second explosion image
			# and resets counter for next change
			if self.image == self.explosion1 and self.change_count >= 50:
				self.image = self.explosion2
				self.change_count = 0
			# after second explosion image, resets mother ship
			if self.image == self.explosion2 and self.change_count >= 50:
				self.reset_mother()
		self.change_count += self.speed * 5

	def check_if_hit(self, bullet_x, bullet_y):
		# calculate collision and set shot state accordingly
		collision = math.sqrt(math.pow((self.X + 17) - (bullet_x - 17), 2) + math.pow(self.Y - bullet_y, 2))
		if collision < 30:
			self.shot = True
			return self.value

	def random_launch(self):
		# using random numbers to decide when mother ship sets off
		decider = choice(range(2000))
		if decider == 1000 and not self.moving:
			self.moving = True

