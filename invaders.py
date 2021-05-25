from invader import Invader
from laser import Laser
import math
from random import choice


class Invaders:

	def __init__(self, screen):
		# constructs and initializes 2d array of invaders
		self.screen = screen
		# row and column coordinates
		self.Y_list = [100, 140, 180, 220, 260]
		self.X_list = [40, 100, 160, 220, 280, 340, 400, 460, 520]
		# values for invaders according to row
		self.value_list = [30, 20, 20, 10, 10]
		# type of alien for each row selected by color string
		self.color_list = ["green", "pink", "pink", "yellow", "yellow"]
		# list for storing rows of invaders
		self.invaders_list = []
		# list for storing created and fired lasers
		self.laser_list = []
		# list for storing which invaders are able to shoot
		# i.e. those who are on the bottom or their respective column
		self.shooter_list = []
		# method for constructing 2d array
		self.build_attack()
		self.remove_counter = 0
		# self.shooter_list = []

	def clear_invaders(self):
		# clears 2d array
		self.invaders_list = []

	def initialize_shooter_list(self):
		# clears shooter list
		self.shooter_list = []

	def build_attack(self):
		self.clear_invaders()
		self.initialize_shooter_list()
		# iterate through row coordinates
		for y in range(len(self.Y_list)):
			# create empty row
			new_row = []
			# iterate through column coordinates
			for x in self.X_list:
				# create new invader, passing in from lists above, color type,
				# score value, start coordinates, and the index of the X_list as column number
				new_invader = Invader(self.screen, self.color_list[y], self.value_list[y], x, self.Y_list[y], self.X_list.index(x))
				# append new invader to row
				new_row.append(new_invader)
			# append completed row to invaders list
			self.invaders_list.append(new_row)
		# create initial shooter list from bottom row of invaders
		self.create_shooter_list()

	def check_if_all_killed(self):
		# check if all invaders have been shot
		# set state of invaders to be all gone,
		# to be negated if invader is found
		all_empty = True
		# iterate through each row, check length and
		# negate all_empty if length is greater than 0
		for row in self.invaders_list:
			if len(row) > 0:
				all_empty = False
		# otherwise return that all rows are empty
		return all_empty

	def blit(self):
		# display invaders on screen
		# iterate through each row in array
		for invader_row in self.invaders_list:
			# iterate through each invader in each row
			for invader in invader_row:
				#blits invader and checks if invader is
				#on second explosion image - i.e. has been hit (returns True)
				if invader.blit():
					# if hit, establish row, index and column number of hit invader
					row_index = self.invaders_list.index(invader_row)
					invader_index = invader_row.index(invader)
					column = invader.column
					# delete hit invader from array
					self.remove(row_index, invader_index)
					# replace invader in shooter list with the
					# next up remaining invader in its column
					self.update_shooter_list(column)
		# check and handle edge invaders reaching edges of screen
		self.detect_edges()
		# add and prime new lasers
		self.laser_list.append(self.prime_laser())
		# fire lasers
		for laser in self.laser_list:
			self.fire_laser(laser)

	def detect_edges(self):
		# toggle change direction or not
		change = None
		# check if invaders at the edges have reached the edges of the screen
		for invader_row in self.invaders_list:
			if len(invader_row) > 0:
				if invader_row[0].X <= 0:
					# if reached left edge, change direction to positive 1
					change = 1
				if invader_row[len(invader_row) - 1].X >= 560:
					# if reached right edge, change direction to minus 1
					change = -1
		# if change is not None, set new direction, drop down and increase speed
		if change:
			for invader_row in self.invaders_list:
				for invader in invader_row:
					invader.move = change
					invader.Y += invader.drop
					invader.speed += 0.015

	def check_if_hit(self, bullet_x, bullet_y):
		# takes in coordinates of player's bullet
		# iterates through each row of invaders
		for invader_row in self.invaders_list:
			# iterates through each invader in the row
			for invader in invader_row:
				# measure distance of bullet from each invader
				collision = math.sqrt(math.pow((invader.X + 17) - bullet_x, 2) + math.pow(invader.Y - bullet_y, 2))
				# if close enough...
				if collision < 30:
					# pass in invader to change its images to explosions
					self.change_to_explosion(invader)
					# return the invader's score value to add to the player's score
					return invader.value

	def check_and_remove_rows(self):
		# list comprehension to delete empty rows
		self.invaders_list = [row for row in self.invaders_list if row != []]

	def check_if_reached_bunkers(self, defences):
		# clear empty rows before check
		self.check_and_remove_rows()
		# gets lowest Y coordinate of a block in the defences
		marker = min([sublist[1][1] for sublist in defences.bunker_list])
		# check if last invader hasn't just been deleted
		if self.invaders_list != []:
			# iterate through bottom row of invaders check collision with defences
			for invader in self.invaders_list[len(self.invaders_list) - 1]:
				if invader.Y >= marker - 25:
					return True

	def check_if_player_hit(self, player):
		# iterate through laser list
		for laser in self.laser_list:
			# if there are presently any lasers
			if laser:
				collision = math.sqrt(math.pow((player.X + 17) - laser.X, 2) + math.pow(player.Y - laser.Y, 2))
				# if there is a collision and player hasn't already just been hit
				# to avoid losing two lives from two lasers close to each other
				if collision < 30 and not player.hit:
					# remove laser from list
					del self.laser_list[self.laser_list.index(laser)]
					player.hit = True
					player.lives -= 1
					return

	def change_to_explosion(self, invader_to_change):
		# change invader's images to explosions
		# thus altering their state to hit
		invader_to_change.image1 = invader_to_change.explosion1
		invader_to_change.image2 = invader_to_change.explosion2

	def remove(self, row_index, invader_index):
		# remove an invader from its row
		del self.invaders_list[row_index][invader_index]

	def create_shooter_list(self):
		# creates initial list of invaders who can shoot
		# i.e. bottom row of invaders
		for invader in self.invaders_list[len(self.invaders_list) - 1]:
			self.shooter_list.append(invader)

	def update_shooter_list(self, column):
		# replaces a shooter in higher position in same column
		# when an invader has been hit and removed
		# list comprehension to remove invader at specified column
		self.shooter_list = [i for i in self.shooter_list if i.column != column]
		# iterate backwards through rows of invaders until
		# invader in specified column is found
		for invader_row in reversed(self.invaders_list):
			for invader in invader_row:
				if invader.column == column:
					self.shooter_list.append(invader)
					return

	def prime_laser(self):
		# random number regulation of laser frequency
		prime_or_not = choice(range(75))
		if prime_or_not == 50:
			# create new instance of Laser object
			new_laser = Laser(self.screen)
			# randomply select which invader should fire
			chosen_shooter = choice(self.shooter_list)
			# set laser's start coordinates to chosen invader's position
			new_laser.X = chosen_shooter.X + 17
			new_laser.Y = chosen_shooter.Y + 17
			# regulates if laser should be moving or not
			new_laser.state = "firing"
			# returns for storing in laser list
			return new_laser

	def fire_laser(self, laser):
		# if laser is available
		if laser:
			# while firing and on screen, move and display laser
			if laser.state == "firing" and laser.Y <= 600:
				laser.Y += 1
				laser.blit()
			# otherwise remove laser from list
			else:
				del self.laser_list[self.laser_list.index(laser)]