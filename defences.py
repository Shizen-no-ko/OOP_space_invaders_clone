import pygame
import math


class Defences:

	def __init__(self, screen):
		self.screen = screen
		# load and scale building block images for defences
		self.building_block = pygame.transform.scale(pygame.image.load("images/defence_block.png"), (25, 15))
		self.inner_left = pygame.transform.scale(pygame.image.load("images/defence_inner_left.png"), (25, 15))
		self.inner_right = pygame.transform.scale(pygame.image.load("images/defence_inner_right.png"), (25, 15))
		self.top_left = pygame.transform.scale(pygame.image.load("images/defence_top_left.png"), (25, 15))
		self.top_left_damage1 = pygame.transform.scale(pygame.image.load("images/defence_top_left_damage1.png"), (25, 15))
		self.top_left_damage2 = pygame.transform.scale(pygame.image.load("images/defence_top_left_damage2.png"), (25, 15))
		self.top_right_damage1 = pygame.transform.scale(pygame.image.load("images/defence_top_right_damage1.png"), (25, 15))
		self.top_right_damage2 = pygame.transform.scale(pygame.image.load("images/defence_top_right_damage2.png"), (25, 15))
		self.top_right = pygame.transform.scale(pygame.image.load("images/defence_top_right.png"), (25, 15))
		self.damage1 = pygame.transform.scale(pygame.image.load("images/defence_damage_1.png"), (25, 15))
		self.damage2 = pygame.transform.scale(pygame.image.load("images/defence_damage_2.png"), (25, 15))
		# list for selecting blocks during construction process
		self.blocks = [self.building_block, self.top_left, self.top_right, self.inner_left, self.inner_right, self.damage1, self.damage2]
		# indexes for selecting correct block
		self.bunker_indexes = [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0]
		# start positions for each bunker
		self.bunker_positions = [[250, 500], [275, 500], [300, 500], [325, 500], [250, 515], [275, 515], [300, 515], [325, 515], [250, 530], [275, 530], [300, 530], [325, 530], [250, 545], [275, 545], [300, 545], [325, 545]]
		# list for storing all bunker blocks
		self.bunker_list = []
		# construct bunkers
		self.build_bunker()

	def clear_bunkers(self):
		# reset bunker block list
		self.bunker_list = []

	def build_bunker(self):
		self.clear_bunkers()
		# iterate through bunker_indexes, construct and store all three rows of blocks
		for i in range(len(self.bunker_indexes)):
			self.bunker_list.append([self.blocks[self.bunker_indexes[i]], self.bunker_positions[i]])
			self.bunker_list.append([self.blocks[self.bunker_indexes[i]], [self.bunker_positions[i][0] - 175, self.bunker_positions[i][1]]])
			self.bunker_list.append([self.blocks[self.bunker_indexes[i]], [self.bunker_positions[i][0] + 175, self.bunker_positions[i][1]]])

	def blit_bunker(self):
		# blit each block at its coordinates
		for b in range(len(self.bunker_list)):
			self.screen.blit(self.bunker_list[b][0], (self.bunker_list[b][1][0], self.bunker_list[b][1][1]))

	def block_damage_handler(self, block):
		# if block suffers collision, iterate through stages of decay until deleted
		# initial conditions (only for top_left and top_right)
		damage0 = [None, self.top_left, self.top_right]
		damage1 = [self.damage1, self.top_left_damage1, self.top_right_damage1]
		damage2 = [self.damage2, self.top_left_damage2, self.top_right_damage2]
		# if block is in second stage of damage, then delete
		if block[0] in damage2:
			del self.bunker_list[self.bunker_list.index(block)]
		# if block is in first stage of damage then
		# change to second damage state
		elif block[0] in damage1:
			block[0] = damage2[damage1.index(block[0])]
		# if block condition is normal top_left or top_right then
		# set to damaged top_left or top_right
		elif block[0] in damage0:
			block[0] = damage1[damage0.index(block[0])]
		# otherwise set to standard first damage block
		else:
			block[0] = self.damage1

	def check_if_bunker_hit_by_invader(self, laser_list):
		# iterate through each laser in the laser list and
		# check if collision with any blocks in bunker list
		for laser in laser_list:
			for block in self.bunker_list:
				# control if any laser exists
				if laser:
					# calculate collision
					collision = math.sqrt(math.pow((block[1][0] + 9) - laser.X, 2) + math.pow(block[1][1] - laser.Y, 2))
					# if collision, delete laser, update block's damage state
					if collision < 15:
						del laser_list[laser_list.index(laser)]
						self.block_damage_handler(block)
						return

	def check_if_bunker_hit_by_player(self, bullet):
		# if a bullet has been fired then
		# iterate through block list and check for collision
		if bullet:
			for block in self.bunker_list:
				# calculate collision
				collision = math.sqrt(math.pow((block[1][0] + 9) - bullet.X, 2) + math.pow(block[1][1] - bullet.Y, 2))
				if collision < 15:
					# set bullets state to 'hit'
					bullet.hit = True
					# update block's damage state
					self.block_damage_handler(block)
					return
