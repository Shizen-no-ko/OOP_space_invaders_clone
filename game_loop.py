import pygame
import sys
import time
from player import Player
from invaders import Invaders
from mothership import MotherShip
from bullet import Bullet
from scoreboard import Scoreboard
from defences import Defences
from sounds import Sounds
from pygame import mixer

pygame.mixer.init()
mixer.music.set_volume(0.01)


class GameLoop:

	def __init__(self):
		self.game_started = True
		pygame.init()
		# set up screen
		self.icon = pygame.image.load("images/icon.png")
		pygame.display.set_icon(self.icon)
		self.screen = pygame.display.set_mode((600, 700))
		pygame.display.set_caption("Michael's Amazing Space Invaders")
		# initialize all object instances required for game
		self.bring_in_components()
		# start loop
		self.loop()
		# import soundtrack for invaders
		mixer.music.load('sounds/haa.wav')
		# variable for tracking invader speed through each wave of new invaders
		self.current_invader_speed = self.invaders.invaders_list[0][0].speed

	def bring_in_components(self):
		# initializes all object instances required
		self.scoreboard = Scoreboard(self.screen)
		self.sounds = Sounds()
		self.bullet = Bullet(self.screen)
		self.set_protagonists()

	def set_protagonists(self):
		# initializes object instances that need to be refreshed during game loop
		self.player = Player(self.screen)
		self.defences = Defences(self.screen)
		self.invaders = Invaders(self.screen)
		self.mother_ship = MotherShip(self.screen)

	def score_for_a_hit(self, collision_type):
		# updates score if invader or mother ship hit
		if collision_type:
			self.sounds.play_explosion_sound()
			# reset bullet
			self.bullet.Y = 600
			self.bullet.X = -50
			self.bullet.state = "loaded"
			# determine which player should have score incremented
			if self.scoreboard.score_to_add == 1:
				self.scoreboard.score1 += collision_type
			elif self.scoreboard.score_to_add == 2:
				self.scoreboard.score2 += collision_type

	def loop(self):
		# main program loop
		while self.game_started:
			# if scoreboard.in_play is false, show title page
			self.title_page()
			# otherwise, run game
			self.inner_game_loop()

	def title_page(self):
		# get high score from file
		self.scoreboard.retrieve_high_score()
		# update high score display
		self.scoreboard.set_new_high_score_display()
		# play title sound
		self.sounds.play_title_sound()
		while not self.scoreboard.in_play:
			self.screen.fill('black')
			self.scoreboard.title_page()
			pygame.display.update()
			# check for events
			for event in pygame.event.get():
				# close screen event
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				# key events
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1 or event.key == pygame.K_KP1:
						# set to one player
						self.scoreboard.one_or_two = 1
						# toggle game to on
						self.scoreboard.in_play = True
					elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
						# set to two player
						self.scoreboard.one_or_two = 2
						# toggle game to on
						self.scoreboard.in_play = True
		# load invader soundtrack
		mixer.music.load("sounds/haa.wav")

	def inner_game_loop(self):
		while self.scoreboard.in_play:
			# game methods
			self.handle_keys()
			self.draw_screen()
			self.update_invader_speed()
			self.handle_collisions()
			self.play_soundtrack()
			self.blit_all()
			self.handle_game_over()
			self.handle_invaders_gone()
			# update screen after each loop
			pygame.display.update()

	def update_invader_speed(self):
		# maintain correct current speed of invaders,
		# so that new arrays of invaders don't go back to speed of first wave
		for row in self.invaders.invaders_list:
			if len(row) > 0:
				self.current_invader_speed = row[0].speed
				return

	def handle_keys(self):
		# handle key presses and close window events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.go_left()
				elif event.key == pygame.K_RIGHT:
					self.player.go_right()
				# if space pressed and bullet is not already moving on screen
				elif event.key == pygame.K_SPACE and self.bullet.state == "loaded":
					self.sounds.play_bullet_sound()
					self.bullet.state = "shooting"
					# position bullet to center of player sprite
					self.bullet.X = self.player.X + 19
			# if no keypress, set player movement to 0
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					self.player.stop()

	def draw_screen(self):
		# fill black background and line at bottom of screen
		self.screen.fill('black')
		pygame.draw.line(self.screen, "purple", (0, 650), (600, 650), 3)

	def handle_bullet(self):
		# if bullet is firing, handle collisions with defences and
		# invaders, updating scores accordingly
		if self.bullet.state == "shooting":
			self.bullet.Y += self.bullet.move
			collision = self.invaders.check_if_hit(self.bullet.X, self.bullet.Y)
			collision_mother = self.mother_ship.check_if_hit(self.bullet.X, self.bullet.Y)
			self.score_for_a_hit(collision)
			self.score_for_a_hit(collision_mother)
			self.defences.check_if_bunker_hit_by_player(self.bullet)

	def handle_lasers(self):
		# check if defences have been hit by invader laser
		# check if player has been hit by invader laser, and play sound
		self.invaders.check_if_player_hit(self.player)
		if self.player.hit:
			self.sounds.play_hit_sound()
		self.defences.check_if_bunker_hit_by_invader(self.invaders.laser_list)

	def handle_collisions(self):
		# run methods for checking and handling bullet and laser collisions
		self.handle_bullet()
		self.handle_lasers()

	def play_soundtrack(self):
		# play soundtrack if game is playing
		self.load_sounds()
		mixer.music.play(-1)
		if not self.scoreboard.in_play:
			mixer.music.stop()

	def load_sounds(self):
		# load sounds according to whether mother ship is on screen or not
		if self.mother_ship.moving and not self.mother_ship.sound_loaded:
			mixer.music.load("sounds/mothership.wav")
			# state of sound loaded
			self.mother_ship.sound_loaded = True
		elif not self.mother_ship.moving and self.mother_ship.sound_loaded:
			mixer.music.load("sounds/haa.wav")
			# state of sound loaded
			self.mother_ship.sound_loaded = False

	def blit_all(self):
		# blit all sprites, text, and play soundtrack
		self.bullet.blit()
		self.invaders.blit()
		self.player.blit()
		self.mother_ship.blit()
		self.load_sounds()
		self.play_soundtrack()
		self.defences.blit_bunker()
		self.scoreboard.blit()

	def handle_game_over(self):
		# if all lives gone, or invaders reach bunkers
		if self.player.lives <= 0 or self.invaders.check_if_reached_bunkers(self.defences):
			# if player 1 or 2 has beaten the high score, update high score
			if self.scoreboard.score1 > self.scoreboard.high_score or self.scoreboard.score2 > self.scoreboard.high_score:
				self.scoreboard.high_score = max(self.scoreboard.score1, self.scoreboard.score2)
				self.store_high_score()
			# clear screen
			self.screen.fill("black")
			# set game over, or player 2 text
			self.scoreboard.game_over()
			# play game over sound
			self.sounds.play_game_over_sound()
			mixer.music.stop()
			# display game over, or player 2 text
			self.scoreboard.blit()
			pygame.display.update()
			# pause before new start
			time.sleep(2)
			# reduce how many players left to play
			self.scoreboard.one_or_two -= 1
			# set which player will receive next points
			self.scoreboard.score_to_add += 1
			# if on player 2, reset game for player 2
			if self.scoreboard.one_or_two == 1:
				self.set_protagonists()
				return
			# if no players left, restart/reset whole game
			elif self.scoreboard.one_or_two < 1:
				self.scoreboard.in_play = False
				self.scoreboard.score_to_add = 1
				self.scoreboard.one_or_two = 1
				self.set_protagonists()
				self.scoreboard = Scoreboard(self.screen)
				return

	def handle_invaders_gone(self):
		# if all invaders have been shot, load new array of invaders
		if self.invaders.check_if_all_killed():
			self.invaders.build_attack()
			# set new array of invaders to current speed reached
			for row in self.invaders.invaders_list:
				for invader in row:
					invader.speed = self.current_invader_speed

	def store_high_score(self):
		# store high score in file
		with open('high_score.txt', 'w') as high:
			high.write(str(self.scoreboard.high_score))


