from pygame import mixer
mixer.init()


class Sounds:

	def __init__(self):
		self.bullet_sound = mixer.Sound('sounds/choo.wav')
		self.bullet_sound.set_volume(0.2)
		self.hit_sound = mixer.Sound('sounds/poo.wav')
		self.hit_sound.set_volume(0.1)
		self.explosion_sound = mixer.Sound('sounds/explosion.wav')
		self.explosion_sound.set_volume(0.1)
		self.mother_sound = mixer.music.load('sounds/mothership.wav')
		self.haa_sound = mixer.music.load('sounds/haa.wav')
		self.game_over_sound = mixer.Sound('sounds/ohno.wav')
		self.game_over_sound.set_volume(0.75)
		self.title_page_sound = mixer.Sound('sounds/yay.wav')
		self.title_page_sound.set_volume(0.2)
		# channels for sounds
		self.channel1 = None
		self.channel2 = None
		self.channel3 = None
		self.channel4 = None
		self.channel5 = None

	def play_bullet_sound(self):
		self.channel1 = mixer.find_channel(True)
		self.channel1.play(self.bullet_sound)

	def play_explosion_sound(self):
		self.channel2 = mixer.find_channel(True)
		self.channel2.play(self.explosion_sound)

	def play_game_over_sound(self):
		self.channel3 = mixer.find_channel(True)
		self.channel3.play(self.game_over_sound)

	def play_hit_sound(self):
		self.channel4 = mixer.find_channel(True)
		self.channel4.play(self.hit_sound)

	def play_title_sound(self):
		self.channel5 = mixer.find_channel(True)
		self.channel5.play(self.title_page_sound)