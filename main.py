import pygame, sys
from utils import *
from pathfinding import *
from sort import *
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720),pygame.FULLSCREEN)
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def play():
	while True:
		SCREEN.blit(BG, (0, 0))
		PLAY_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("VISIOALGO", True, "#b68f40")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

		ASTAR_BUTTON = get_button((320, 250), "A*")
		DJIKSTRA_BUTTON = get_button((320, 400), "Djikstra")
		INSERT_BUTTON = get_button((960, 250), "Insertion Sort", 40)
		BUBBLE_BUTTON = get_button((960, 400), "Bubble Sort")

		PLAY_BACK = Button(image=None, pos=(640, 625), 
							text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

		
		SCREEN.blit(MENU_TEXT, MENU_RECT)
		for button in [ASTAR_BUTTON, DJIKSTRA_BUTTON, INSERT_BUTTON, BUBBLE_BUTTON, PLAY_BACK]:
			button.change_color(PLAY_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if ASTAR_BUTTON.check_for_input(PLAY_MOUSE_POS):
					path_finding(SCREEN, 1920, 1080, astar)
				if DJIKSTRA_BUTTON.check_for_input(PLAY_MOUSE_POS):
					path_finding(SCREEN, 1920, 1080, djikstra)
				if INSERT_BUTTON.check_for_input(PLAY_MOUSE_POS):
					sort(insertion_sort, "Insertion Sort")
				if BUBBLE_BUTTON.check_for_input(PLAY_MOUSE_POS):
					sort(bubble_sort, "Bubble Sort")
				if PLAY_BACK.check_for_input(PLAY_MOUSE_POS):
					main_menu()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					main_menu()

		pygame.display.update()
	
def about():
	while True:
		OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

		SCREEN.blit(BG, (0, 0))

		OPTIONS_TEXT = get_font(75).render("A project by:", True, "#b68f40")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))

		#NAMES OF CREATORS
		PRANIL_BUTTON = get_button((320, 300), "Prabin Dhakal", 40, "#b68f40")
		SHARAD_BUTTON = get_button((960, 300), "Sharad Kr. Dahal", 36, "#b68f40")
		SIDDHANT_BUTTON = get_button((320, 450), "Siddhant Thakur", 38, "#b68f40")
		SIJAN_BUTTON = get_button((960, 450), "Sijan Dev", 40, "#b68f40")

		OPTIONS_BACK = Button(image=None, pos=(640, 625), 
							text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

		SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

		for button in [PRANIL_BUTTON, SHARAD_BUTTON, SIDDHANT_BUTTON, SIJAN_BUTTON, OPTIONS_BACK]:
			button.change_color(OPTIONS_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					main_menu()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if OPTIONS_BACK.check_for_input(OPTIONS_MOUSE_POS):
					main_menu()
			

		pygame.display.update()

#pathfinding algorithms
def path_finding(win, width, height, algorithm):
	ROWS = 52
	grid = make_grid(ROWS, width, height)
	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width, height)
		for event in pygame.event.get():

			if pygame.mouse.get_pressed()[0]: #for left mouse click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width, height)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #for right mouse click or double finger click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width, height)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width, height), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width, height)

				if event.key == pygame.K_r:
					start = None
					end = None
					grid = make_grid(ROWS, width, height)

				if event.key == pygame.K_ESCAPE:
					play()

#sorting algorithms
def sort(algo_name, algo_string):
	run = True
	clock = pygame.time.Clock()

	n = 60
	min_val = 2
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1280, 720, lst)
	sorting = False
	ascending = True

	sorting_algorithm = algo_name
	sorting_algo_name = algo_string
	sorting_algorithm_generator = None

	while run:
		clock.tick(60)

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw_sort(draw_info, sorting_algo_name, ascending)

		#event handlers
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_ESCAPE:
					play()
			elif event.key == pygame.K_q:
				pygame.quit()
				sys.exit()

def main_menu():
	while True:
		SCREEN.blit(BG, (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("VISIOALGO", True, "#b68f40")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

		PLAY_BUTTON = get_button((640, 250), "PLAY", 75, "Green", "assets/Play Rect.png")
		ABOUT_BUTTON = get_button((640, 400), "ABOUT", 75)
		QUIT_BUTTON = get_button((640, 550), "QUIT", 75, "Green", "assets/Quit Rect.png")

		SCREEN.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
			button.change_color(MENU_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
					play()
				if ABOUT_BUTTON.check_for_input(MENU_MOUSE_POS):
					about()
				if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

		pygame.display.update()

main_menu()