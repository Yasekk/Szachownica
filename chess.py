import pygame
import sys
from settings import Settings
import functions as fct
from pygame.sprite import Group
from chess_board import create_board_and_pieces
def play_chess():
	#Inicjalizacja programu i wczytywanie początkowych wartości
	pygame.init()
	settings=Settings()
	screen=pygame.display.set_mode((settings.screen_width,
	settings.screen_height))
	pygame.display.set_caption("Chess")
	#Tworzenie szachownicy i figur
	chess_board=Group()
	board_pieces=Group()
	create_board_and_pieces(settings,screen,chess_board,board_pieces)	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#Aktywowanie funkcji, tylko raz podczas kliknięcia
				if settings.clicked==False:
					fct.button_click(settings,chess_board)							
			elif event.type == pygame.MOUSEBUTTONUP:
				#Umożliwienie ponownych aktywacji funkcji przy kolejnych
				#kliknięciach
				settings.clicked=False
		#Wyświetlenie obiektów szacownicy	
		fct.update_screen(screen,chess_board,board_pieces)
play_chess()
