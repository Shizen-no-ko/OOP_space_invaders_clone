import pygame
pygame.font.init()


class Scoreboard:

	def __init__(self, screen):
		self.screen = screen
		# initialize player scores
		self.score1 = 0
		self.score2 = 0
		self.high_score = 0
		# bring in high score from file
		self.retrieve_high_score()
		# fonts
		self.font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 17)
		self.game_over_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 40)
		# titles and labels
		self.score_titles = self.font.render('Score < 1 >  Hi-Score  Score < 2 >', False, (255, 255, 255))
		self.scores = self.font.render(f'   {self.score1:04d}        {self.high_score:04d}        {self.score2:04d}', False, (255, 255, 255))
		self.game_over_text = self.game_over_font.render('GAME OVER', False, (255, 255, 255))
		self.player_2_text = self.game_over_font.render('Player 2', False, (255, 255, 255))
		self.title_image = pygame.image.load("images/title_image.png")
		self.title_image = pygame.transform.scale(self.title_image, (400, 400))
		self.high_score_display = self.font.render(f'Current High Score: {self.high_score:04d}', False, (255, 255, 255))
		self.select_text1 = self.font.render('One or Two Players?', False, (255, 255, 255))
		self.select_text2 = self.font.render('Press < 1 > or < 2 >', False, (255, 255, 255))
		# toggle for inner game loop
		self.in_play = False
		# indicator for one or two players selected
		self.one_or_two = 1
		# which score tally to add points to; player 1 or 2
		self.score_to_add = 1

	def retrieve_high_score(self):
		# bring in previously stored high-score
		with open('high_score.txt', 'r') as high:
			self.high_score = int(high.read())

	def blit(self):
		# update score display and blit it with titles above
		self.scores = self.font.render(f'   {self.score1:04d}        {self.high_score:04d}        {self.score2:04d}', False, (255, 255, 255))
		self.screen.blit(self.score_titles, (13, 13))
		self.screen.blit(self.scores, (13, 43))

	def game_over(self):
		# handle game over condition.
		# Either display game over text and end inner game loop
		if self.one_or_two == 1:
			self.screen.blit(self.game_over_text, (120, 300))
			self.in_play = False
		# or display player 2 text
		else:
			self.screen.blit(self.player_2_text, (140, 300))

	def set_new_high_score_display(self):
		# update the high score display for the title page
		self.high_score_display = self.font.render(f'Current High Score: {self.high_score:04d}', False, (255, 255, 255))

	def title_page(self):
		# display layout for title page
		self.high_score_display = self.font.render(f'Current High Score: {self.high_score:04d}', False, (255, 255, 255))
		self.screen.blit(self.title_image, (100, 55))
		self.screen.blit(self.high_score_display, (100, 500))
		self.screen.blit(self.select_text1, (135, 550))
		self.screen.blit(self.select_text2, (125, 600))
