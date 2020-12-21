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
	#Lista pól, które mogą być atakowene przez figury danego koloru
	check_white=[]
	check_black=[]	
	#Tworzenie szachownicy i figur
	chess_board=Group()
	board_pieces=Group()
	create_board_and_pieces(settings,screen,chess_board,board_pieces,
	check_white,check_black)
	#Lista, w której będą się zjadnowały pola mozliwo do zasłonięcia,
	#jeżeli król będzie szachowany prze figure poszuszajacą się rzędem
	king_attack_path=[]
	#Sprawdzenie możliwych ruchów poszczególnych figur
	fct.check_moves(board_pieces,chess_board,check_white,check_black,
	king_attack_path)
	#Lista w której będzie znajdował się znacznik pokazujący wybrane
	#pole
	highlight=[]
	#Lista w której będzie znajdował się komunikat końca gry
	game_end=[]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#Aktywowanie funkcji, tylko raz podczas kliknięcia
				if settings.clicked==False:
					fct.button_click(settings,screen,chess_board,
					highlight,check_white,check_black,board_pieces,
					game_end,king_attack_path)							
			elif event.type == pygame.MOUSEBUTTONUP:
				#Umożliwienie ponownych aktywacji funkcji przy kolejnych
				#kliknięciach
				settings.clicked=False
		#Wyświetlenie obiektów szacownicy	
		fct.update_screen(screen,chess_board,board_pieces,highlight,
		game_end)
play_chess()
