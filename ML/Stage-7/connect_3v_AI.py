#TODO: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 3
COLUMN_COUNT = 5

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1#RED
AI_PIECE = 2#YELLOW

WINDOW_LENGTH = 4

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
    Win_1 = 0
    Win_2 = 0

    for c in range(COLUMN_COUNT):
        column = board[:, c]
        if (np.array_equal(column, [1, 1, 1]) or
            np.array_equal(column, [1, 2, 1]) or
            np.array_equal(column, [2, 1, 1])):
            Win_1 += 1

    for c in range(COLUMN_COUNT):
        column = board[:, c]
        if (np.array_equal(column, [2, 2, 2]) or
            np.array_equal(column, [2, 1, 2]) or
            np.array_equal(column, [1, 2, 2])):
            Win_2 += 1

    #print("RED WIN:", Win_1)
    #print("YELLOW WIN:", Win_2)

    if piece == 1 and Win_1 >= 3:
        return True
    elif piece == 2 and Win_2 >= 3:
        return True

    return False
	# # Check horizontal locations for win
	# for c in range(COLUMN_COUNT-3):
	# 	for r in range(ROW_COUNT):
	# 		if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
	# 			return True

	# # Check vertical locations for win
	# for c in range(COLUMN_COUNT):
	# 	for r in range(ROW_COUNT-3):
	# 		if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
	# 			return True

	# # Check positively sloped diaganols
	# for c in range(COLUMN_COUNT-3):
	# 	for r in range(ROW_COUNT-3):
	# 		if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
	# 			return True

	# # Check negatively sloped diaganols
	# for c in range(COLUMN_COUNT-3):
	# 	for r in range(3, ROW_COUNT):
	# 		if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
	# 			return True

def evaluate_window(temp_board,c,piece):
	score = 0

	opp_piece = PLAYER_PIECE

	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE


	col = temp_board[:,c]


	

	# if window.count(piece) == 4:
	# 	score += 100
	# elif window.count(piece) == 3 and window.count(EMPTY) == 1:
	# 	score += 5
	# elif window.count(piece) == 2 and window.count(EMPTY) == 2:
	# 	score += 2

	# if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
	# 	score -= 4


#TODO: change in scoring
		
	if piece == PLAYER_PIECE:#player
		pass
	

	#np.array_equal(col,[2,2,1])
	elif piece == AI_PIECE:#AI
		if np.array_equal(col,[2,2,1])  or np.array_equal(col,[2,1,2]):
			score += 100
		elif np.array_equal(col,[2,2,2]):
			score += 90
		elif np.array_equal(col,[2,1,1]):
			score += 50
		# elif c == [1,2,2]:
		# 	score += 40
		elif np.array_equal(col,[0,0,2]):
			score += 30
		elif np.array_equal(col,[0,2,2]):
			score += 15
		elif np.array_equal(col,[0,2,1]): #or c == [0,1,2]:#50% chance
			score += 10
		# elif np.array_equal(col,[0,0,0]):
		# 	score += 5
		else:
			score += 0

		# elif c == [0,0,2] or c == [0,0,1]:
		# 	score += 5
			
		# elif c == [1,1,2] or c == [1,2,1]:
		# 	score -= 100
		# elif c == [1,1,1]:
		# 	score -= 90
		# elif c == [1,2,2]:
		# 	score -= 50
		# elif c == [0,1,1]:
		# 	score -= 15
		# elif c == [0,0,1]:
		# 	score -= 30

	return score

def score_position(temp_board, piece):
	
	score = 0

	# print(board)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		print(c)
		#col_array = [int(i) for i in list(board[:,c])]
		#for r in range(ROW_COUNT-3):
			#window = col_array[r:r+WINDOW_LENGTH]
		score += evaluate_window(temp_board,c,piece)
		# print("---------")
		# print(temp_board[:,c])
		# print("---------")
		

	
		

	#for vertical

	# ## Score center column
	# center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	# center_count = center_array.count(piece)
	# score += center_count * 3

	# ## Score Horizontal
	# for r in range(ROW_COUNT):
	# 	row_array = [int(i) for i in list(board[r,:])]
	# 	for c in range(COLUMN_COUNT-3):
	# 		window = row_array[c:c+WINDOW_LENGTH]
	# 		score += evaluate_window(window, piece)

	# ## Score Vertical
	# for c in range(COLUMN_COUNT):
	# 	col_array = [int(i) for i in list(board[:,c])]
	# 	for r in range(ROW_COUNT-3):
	# 		window = col_array[r:r+WINDOW_LENGTH]
	# 		score += evaluate_window(window, piece)

	# ## Score posiive sloped diagonal
	# for r in range(ROW_COUNT-3):
	# 	for c in range(COLUMN_COUNT-3):
	# 		window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
	# 		score += evaluate_window(window, piece)

	# for r in range(ROW_COUNT-3):
	# 	for c in range(COLUMN_COUNT-3):
	# 		window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
	# 		score += evaluate_window(window, piece)

	return score

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	if not valid_locations:  # Check if valid_locations is empty
		return None  # No valid moves available, return None
	best_score = -10000

	best_col = random.choice(valid_locations)

	#for prefrences
	all_column_score_dict = {}

	for col in valid_locations:

		row = get_next_open_row(board, col)

		temp_board = board.copy()

		drop_piece(temp_board, row, col, piece)

		score = score_position(temp_board, piece)

		#print("---",temp_board[:,col],"--->",score)


		#print(score)

		all_column_score_dict[col]=score

	#print(all_column_score_dict)
	#for checking from middle
	# values = list(all_column_score_dict.values())
	# keys = list(all_column_score_dict.keys())

#TODO: for center priority
		
	if len(valid_locations) >= 2:
		middle_index = len(valid_locations) // 2  # Calculate middle index dynamically

		best_score = all_column_score_dict[valid_locations[middle_index]]
		best_key = valid_locations[middle_index]

		# Iterate through elements around the middle index to find the best score
		for i in range(max(0, middle_index - 1), min(len(valid_locations), middle_index + 2)):
			if all_column_score_dict[valid_locations[i]] > best_score:
				best_score = all_column_score_dict[valid_locations[i]]
				best_key = valid_locations[i]

		best_col = best_key

	return best_col

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):

	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves,TIE
				return (None, 0)
		else: # Depth is zerox
			return (None, score_position(board, AI_PIECE))
		
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def switch_turns():
	"""
	Function to switch turns between two teams, allowing each team to have a random number of consecutive turns (1, 2, or 3).

	Parameters:
		team1 (str): Name of the first team.
		team2 (str): Name of the second team.
		
	Returns:
		str: Name of the team whose turn is next.
	"""
	team1 = PLAYER
	team2 = AI
	switch_turns.counter = getattr(switch_turns, 'counter', 0)
	switch_turns.last_team = getattr(switch_turns, 'last_team', None)
	switch_turns.consecutive_count = getattr(switch_turns, 'consecutive_count', 0)
	switch_turns.max_consecutive = getattr(switch_turns, 'max_consecutive', random.randint(1, 2))

	if switch_turns.last_team != team1 and switch_turns.last_team != team2:
		# If it's the first turn, choose a random team to start
		switch_turns.last_team = random.choice([team1, team2])

	if switch_turns.consecutive_count < switch_turns.max_consecutive:
		# If the consecutive count is less than the maximum allowed, continue with the same team
		switch_turns.consecutive_count += 1
	else:
		# If the consecutive count is equal to the maximum allowed, switch to the other team
		if switch_turns.last_team == team1:
			switch_turns.last_team = team2
		else:
			switch_turns.last_team = team1
		# Reset consecutive count and determine new max consecutive turns
		switch_turns.consecutive_count = 1
		switch_turns.max_consecutive = random.randint(1, 2)

	return_team = switch_turns.last_team

	return return_team

board = create_board()

print_board(board)
game_over = False

#helper
pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
#helper

# turn = random.randint(PLAYER, AI)
# turn = next(generate_turns())
turn = switch_turns()

Cnt = 0

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):

					row = get_next_open_row(board, col)

					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						
						game_over = True

					print_board(board)
					draw_board(board)
					# turn += 1
					# turn = turn % 2
						
					# turn = random.randint(0,1)
						
					# turn = next(generate_turns())
						
					turn = switch_turns()

					Cnt += 1

					if Cnt >= 15 and not game_over:
						print("Tie")               
						game_over = True



	# # Ask for Player 2 Input
	if turn == AI and not game_over:				

		#col = random.randint(0, COLUMN_COUNT-1)
		col = pick_best_move(board, AI_PIECE)
		#col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			# turn += 1
			# turn = turn % 2

			# turn = random.randint(0,1)

			# turn = next(generate_turns())

			turn = switch_turns()

			Cnt += 1

			if Cnt >= 15:
				print("Tie")               
				game_over = True

	if game_over:
		pygame.time.wait(3000)


