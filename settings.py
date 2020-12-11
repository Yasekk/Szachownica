class Settings():
	def __init__(self):
		"""Podstawowe ustanienia programu; rozmiar komórek składających
		sie na tło ekranu jest skalowany na podstawie preferowanego
		rozmiaru ekranu i liczby komórek"""
		#Parametry ekranu
		self.screen_height=650
		self.screen_width=1300
		#Parametry niewidzialnego tła; obliczanie szerokości i wysokości
		#komórek, z kórych będzie składało się niewidzialne tło
		self.width_grid_number=200
		self.height_grid_number=100
		#Rozmiary komórek składających się na tło
		self.width_grid=self.screen_width/self.width_grid_number
		self.height_grid=self.screen_height/self.height_grid_number
		#Szerokość i wysokośc pól na szachownicy
		self.chess_field_size=self.width_grid*11
		#Możliwe ruchy dla obecnie zaznaczonej figury
		self.avialable_moves=None
		#Obecnie zaznaczona figura
		self.moving_piece=None
		#Sprawdzanie czy mysz została odkliknięta (zapobieganie
		#powtarzania działania do czasu odkliknięcia i kliknięcia na 
		#nowo)
		self.clicked=False
		
