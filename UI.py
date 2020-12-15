import pygame
from pygame.sprite import Sprite
import pygame.font
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
class WinningScreen():
	"""Tworzenie grafiki z komunikatem, że nastąpił szach mat"""
	def __init__(self,screen,settings,message):
		self.screen=screen
		self.screen_rect=screen.get_rect()
		#Zdefiniowanie wymiarów i właściwości napisu
		self.width=settings.screen_width/2
		self.height=settings.screen_height/2
		self.field_color=(0,100,0)
		self.text_color=(255,255,255)
		self.font=pygame.font.SysFont(None,90)
		#Ustawienie prostokąta komunikatu i wyśrodkowanie go
		self.rect=pygame.Rect(0,0,self.width,self.height)
		self.rect.center=self.screen_rect.center
		self.prepare_message(message)
	def prepare_message(self,message):
		"""Umieszczenie komunikatu na wygenerowanym tle"""
		self.message_image=self.font.render(message,True,
		self.text_color,self.field_color)
		self.message_image_rect=self.message_image.get_rect()
		self.message_image_rect.center=self.rect.center
	def draw_message(self):
		#Wyświetlanie pustego tła a następnie komunikatu an nim
		self.screen.fill(self.field_color,self.rect)
		self.screen.blit(self.message_image,self.message_image_rect)
