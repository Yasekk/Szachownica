import pygame
from pygame.sprite import Sprite
class SelectedPart(Sprite):
	"""Tworzenie znacznika, które będzie wskazywał aktualnie zaznaczone
	pole"""
	def __init__(self,screen,settings,board_part):
		super().__init__()
		self.screen=screen
		self.screen_rect=screen.get_rect()
		self.rect=pygame.Rect(0,0,settings.chess_field_size,
		settings.chess_field_size)
		self.color=(155,10,155)
		#Umiejscowienie znacznika w miejscu odposiadającemu polu
		#zaznaczonej figury
		self.rect.center=board_part.rect.center
	def draw_part(self):
		"""Wyświetlenie pola szachownicy"""
		pygame.draw.rect(self.screen,self.color,self.rect)
