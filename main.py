## CS440 Spring 2021
## Project 2 : Minesweeper
## Mustafa Sadiq (ms3035)

## Uncomment block of code to run from 'uncomment from here' to 'uncomment till here'

######################## IMPORTS ########################################
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import time
import math

######################## INTRODUCTION ########################################
## Environment
## 'X' = mine
## 'C' = no mine where C is 0-8

######################## MAKE BOARD ########################################
def make_board(dim, n):
    board = np.empty([dim, dim], dtype=str)
    while n != 0:
        x = rand.randrange(0, dim)
        y = rand.randrange(0, dim)
        if board[x][y] != 'X':
            board[x][y] = 'X' 
            n -= 1   
    
    for x in range(dim):
        for y in range(dim):
            if board[x][y] != 'X':
                board[x][y] = count_neighbouring_mines_board(board, (x, y))

    return board

######################## MAKE BOARD COUNT MINES ########################################
def count_neighbouring_mines_board(board, point):
    count = 0
    for neighbour in get_neighbours(len(board), point):
        if board[neighbour[0]][neighbour[1]] == 'X':
            count += 1
    return count


######################## PRINT BOARD ########################################
def print_board(board):
    print('-'*(len(board)*4), end="")
    print()
    for x in board:
        for y in x:
            print(f'| {y} ', end="")
        print("|", end="")
        print()
        print('-'*(len(board)*4), end="")
        print()

######################## GET NEIGHBOURS GIVEN A DIM AND POINT ########################################
def get_neighbours(dim, point):
    x = point[0]
    y = point[1]
    neighbours = []

    # non diagonal neighbours
    if x-1 >= 0: 
        neighbours.append((x-1, y))
    if y-1 >= 0: 
        neighbours.append((x, y-1))        
    if x+1 <= dim - 1: 
        neighbours.append((x+1, y))  
    if y+1 <= dim - 1: 
        neighbours.append((x, y+1))

    # diagonal neighbours
    if x-1 >= 0 and y-1 >= 0: 
        neighbours.append((x-1, y-1))
    if x-1 >= 0 and y+1 <= dim - 1: 
        neighbours.append((x-1, y+1))
    if x+1 <= dim - 1 and y-1 >= 0: 
        neighbours.append((x+1, y-1)) 
    if x+1 <= dim - 1 and y+1 <= dim - 1: 
        neighbours.append((x+1, y+1))        
     
    
    return neighbours

######################## GET NEIGHBOURS COUNT THAT ARE MINES ########################################
def count_neighbouring_mines(dim, point, mine_cells):
    count = 0
    for neighbour in get_neighbours(dim, point):
        if neighbour in mine_cells:
            count += 1
    return count

######################## GET NEIGHBOURS COUNT THAT ARE NOT MINES ########################################
def count_neighbouring_safe(dim, point, safe_cells):
    count = 0
    for neighbour in get_neighbours(dim, point):
        if neighbour in safe_cells:
            count += 1
    return count

######################## GET NEIGHBOURS COUNT THAT ARE HIDDEN ########################################
def count_neighbouring_hidden(dim, point, hidden_cells):
    count = 0
    for neighbour in get_neighbours(dim, point):
        if neighbour in hidden_cells:
            count += 1
    return count

######################## QUERY GAME BOARD ########################################
def query(game_board, point):
    return game_board[point[0]][point[1]]

######################## PRINT BOTH BOARDS ########################################
def print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells):
    print('\nGame board:')
    print_board(game_board)
    print('\nPlayer board:')
    print_player_baord(game_board, dim, safe_cells, mine_cells, hidden_cells)    
    print('--------------------------------------\n')

######################## INITIALZE HIDDEN SET ########################################
def initialize_hidden_cells(dim):
    hidden_cells = set()
    for x in range(dim):
        for y in range(dim):
            hidden_cells.add((x, y))

    return hidden_cells

######################## PRINT PLAYER BOARD ########################################
def print_player_baord(game_board, dim, safe_cells, mine_cells, hidden_cells):
    board = np.empty([dim, dim], dtype=str)
    for safe_cell in safe_cells:
        board[safe_cell[0]][safe_cell[1]] = query(game_board, safe_cell)
    for mine_cell in mine_cells:
        board[mine_cell[0]][mine_cell[1]] = 'X'
    for hidden_cell in hidden_cells:
        board[hidden_cell[0]][hidden_cell[1]] = ' '

    print_board(board)

######################## PRINT KNOWLEDGE BASE ########################################
def print_knowlegde_base(knowledge_base):
    for knowledge in knowledge_base:
        print(str(knowledge[0]) + ' : ' + str(knowledge[1]), end='\n')
    

####################### BASIC AGENT ##########################
### uncomment from here
# def basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
#     inferred = False
#     for safe_cell in safe_cells:
#         mines = count_neighbouring_mines(dim, safe_cell, mine_cells)
#         safe = count_neighbouring_safe(dim, safe_cell, safe_cells)
#         hidden = count_neighbouring_hidden(dim, safe_cell, hidden_cells)
#         clue = int(query(game_board, safe_cell))       

#         if clue - mines == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     mine_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     print(neighbour, 'flagged as mine')
#                     inferred = True
#             if inferred:
#                 return True

#         if len(get_neighbours(dim, safe_cell)) - clue - safe == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     safe_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     print(neighbour, 'flagged as safe')
#                     inferred = True
#             if inferred:
#                 return True

#     return False


# dim = 3
# n = 2
            
# game_board = make_board(dim, n)

# safe_cells = set()
# mine_cells = set()
# hidden_cells = initialize_hidden_cells(dim)
# print("\nInitial boards")
# print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)

# while True:
#     if len(hidden_cells) == 0:
#         print("\nGame finished: no more hidden cells")
#         break

#     if basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
#         print("\nBasic agent made move")
#         print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)
#         time.sleep(0)
#     else:
#         random_cell = rand.choice(tuple(hidden_cells))
#         print("\nMaking random query at", random_cell)
#         type_of_celll = query(game_board, random_cell)
#         if type_of_celll.isdigit():
#             safe_cells.add(random_cell)
#         else:
#             mine_cells.add(random_cell)            
#         hidden_cells.remove(random_cell)
#         print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)
        
### uncomment to here
####################### BASIC AGENT GRAPH ##########################
# ### uncomment from here
# def basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
#     safely_identified_mines = 0
#     inferred = False
#     for safe_cell in safe_cells:
#         mines = count_neighbouring_mines(dim, safe_cell, mine_cells)
#         safe = count_neighbouring_safe(dim, safe_cell, safe_cells)
#         hidden = count_neighbouring_hidden(dim, safe_cell, hidden_cells)
#         clue = int(query(game_board, safe_cell))       

#         if clue - mines == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     mine_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     safely_identified_mines += 1
#                     inferred = True
#             if inferred:
#                 return True, safely_identified_mines

#         if len(get_neighbours(dim, safe_cell)) - clue - safe == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     safe_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     inferred = True
#             if inferred:
#                 return True, safely_identified_mines

#     return inferred, safely_identified_mines

# dim = 20
# runs = 10
# densities_interval = 5
# dataX = range(1, dim*dim+1, densities_interval)
# dataY = []

# for mine_density in dataX:
#     safely_identified_mines = 0
#     for run in range(runs):
#         game_board = make_board(dim, mine_density)

#         safe_cells = set()
#         mine_cells = set()
#         hidden_cells = initialize_hidden_cells(dim)

#         while True:
#             if len(hidden_cells) == 0:
#                 break
#             inferred, mines = basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells)
#             safely_identified_mines += mines
#             if inferred:
#                 ()
#             else:
#                 random_cell = rand.choice(tuple(hidden_cells))
#                 type_of_celll = query(game_board, random_cell)
#                 if type_of_celll.isdigit():
#                     safe_cells.add(random_cell)
#                 else:
#                     mine_cells.add(random_cell)            
#                 hidden_cells.remove(random_cell)
                
#     print(safely_identified_mines, mine_density*runs)
#     dataY.append(safely_identified_mines/(mine_density*runs))

# plt.plot(dataX, dataY)
# # plt.title("Basic agent: average final score vs mine density")
# # plt.ylabel("Safely identified mines/total mines")
# # plt.xlabel("Total mines")
# # plt.show()
# ### uncomment to here


####################### IMPROVED AGENT ##########################
## uncomment from here
def basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
    inferred = False
    for safe_cell in safe_cells:
        mines = count_neighbouring_mines(dim, safe_cell, mine_cells)
        safe = count_neighbouring_safe(dim, safe_cell, safe_cells)
        hidden = count_neighbouring_hidden(dim, safe_cell, hidden_cells)
        clue = int(query(game_board, safe_cell))       

        if clue - mines == hidden:
            for neighbour in get_neighbours(dim, safe_cell):
                if neighbour in hidden_cells:
                    mine_cells.add(neighbour)
                    hidden_cells.remove(neighbour)
                    print(neighbour, 'flagged as mine')
                    inferred = True
            if inferred:
                return True

        if len(get_neighbours(dim, safe_cell)) - clue - safe == hidden:
            for neighbour in get_neighbours(dim, safe_cell):
                if neighbour in hidden_cells:
                    safe_cells.add(neighbour)
                    hidden_cells.remove(neighbour)
                    print(neighbour, 'flagged as safe')
                    inferred = True
            if inferred:
                return True

    return False

def solve_knowledgebase_subset(knowledge_base):
    for knowledge in knowledge_base:
        knowledge_cells = knowledge[0]
        knowledge_clue = knowledge[1]
        for knowledge_nested in knowledge_base:
            if knowledge != knowledge_nested:
                knowledge_cells_nested = knowledge_nested[0]
                knowledge_clue_nested = knowledge_nested[1]

                if len(knowledge_cells_nested) < len(knowledge_cells):
                    if knowledge_cells_nested.issubset(knowledge_cells):
                        new_knowledge = [knowledge_cells-knowledge_cells_nested, knowledge_clue-knowledge_clue_nested]
                        if new_knowledge not in knowledge_base:
                            # print('new knowledge:', new_knowledge)
                            knowledge_base.append(new_knowledge)
                            knowledge_base = solve_knowledgebase_subset(knowledge_base)
                            return knowledge_base
    return knowledge_base

def solve_knowledgebase_subsequence(knowledge_base):
    for knowledge in knowledge_base:
        knowledge_cells = knowledge[0]
        knowledge_clue = knowledge[1]
        for knowledge_nested in knowledge_base:
            if knowledge != knowledge_nested:
                knowledge_cells_nested = knowledge_nested[0]
                knowledge_clue_nested = knowledge_nested[1]

                if len(knowledge_cells_nested) == len(knowledge_cells):
                    if len(knowledge_cells_nested.intersection(knowledge_cells)) == len(knowledge_cells)-1: 
                        if knowledge_clue_nested > knowledge_clue and knowledge_clue_nested-knowledge_clue == 1:    
                            # print('ererere')       
                            new_knowledge = [knowledge_cells_nested-knowledge_cells_nested.intersection(knowledge_cells), 1]
                            if new_knowledge not in knowledge_base:
                                knowledge_base.append(new_knowledge)
                            new_knowledge = [knowledge_cells-knowledge_cells_nested.intersection(knowledge_cells), 0]
                            if new_knowledge not in knowledge_base:
                                knowledge_base.append(new_knowledge)
                            return knowledge_base
    return knowledge_base

def improved_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
    knowledge_base = []

    for safe_cell in safe_cells:
        knowledge_clue = int(query(game_board, safe_cell))     
        neighbours = get_neighbours(dim, safe_cell)

        knowledge_cells = set()
        for neighbour in neighbours:
            if neighbour in mine_cells:
                knowledge_clue -= 1
            if neighbour in hidden_cells:
                knowledge_cells.add(neighbour)

        if knowledge_cells:
            new_knowledge = [knowledge_cells, knowledge_clue]
            if new_knowledge not in knowledge_base:
                knowledge_base.append([knowledge_cells, knowledge_clue])    
    
    
    knowledge_base = solve_knowledgebase_subset(knowledge_base)
    knowledge_base = solve_knowledgebase_subsequence(knowledge_base)
    print_knowlegde_base(knowledge_base)

    for knowledge in knowledge_base:
        knowledge_cells = knowledge[0]
        knowledge_clue = knowledge[1]
        for knowledge_nested in knowledge_base:
            if knowledge != knowledge_nested:
                knowledge_cells_nested = knowledge_nested[0]
                knowledge_clue_nested = knowledge_nested[1]

                if len(knowledge_cells_nested) < len(knowledge_cells):
                    if knowledge_cells_nested.issubset(knowledge_cells):
                        new_knowledge = [knowledge_cells-knowledge_cells_nested, knowledge_clue-knowledge_clue_nested]
                        if new_knowledge not in knowledge_base:
                            print('new knowledge:', new_knowledge)
                            knowledge_base.append(new_knowledge)


    for knowledge in knowledge_base:
        knowledge_cells = knowledge[0]
        knowledge_clue = knowledge[1]
        
        if knowledge_clue == 0:
            for cell in knowledge_cells:
                hidden_cells.remove(cell)
                safe_cells.add(cell)
            return True

        if len(knowledge_cells) == knowledge_clue:
            for cell in knowledge_cells:
                hidden_cells.remove(cell)
                mine_cells.add(cell)
            return True                
                            
    return False


dim = 10
n = 30
            
game_board = make_board(dim, n)

safe_cells = set()
mine_cells = set()
hidden_cells = initialize_hidden_cells(dim)
knowledge_base = []
print("\nInitial boards")
print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)

while True:
    if len(hidden_cells) == 0:
        print("\nGame finished: no more hidden cells")
        break

    if basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
        print("\nBasic agent made move")
        print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)
        time.sleep(0)
    elif improved_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
        print("\nImproved agent made move------------------------------------------")
        print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)
        time.sleep(0)
    else:
        random_cell = rand.choice(tuple(hidden_cells))
        print("\nMaking random query at ---------------------------------------------", random_cell)
        type_of_celll = query(game_board, random_cell)
        if type_of_celll.isdigit():
            safe_cells.add(random_cell)
        else:
            mine_cells.add(random_cell)            
        hidden_cells.remove(random_cell)
        print_both_board(game_board, dim, safe_cells, mine_cells, hidden_cells)

## uncomment to here

# # ####################### IMPROVED AGENT GRAPH ##########################
# ### uncomment from here
# def basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
#     safely_identified_mines = 0
#     inferred = False
#     for safe_cell in safe_cells:
#         mines = count_neighbouring_mines(dim, safe_cell, mine_cells)
#         safe = count_neighbouring_safe(dim, safe_cell, safe_cells)
#         hidden = count_neighbouring_hidden(dim, safe_cell, hidden_cells)
#         clue = int(query(game_board, safe_cell))       

#         if clue - mines == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     mine_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     safely_identified_mines += 1
#                     inferred = True
#             if inferred:
#                 return True, safely_identified_mines

#         if len(get_neighbours(dim, safe_cell)) - clue - safe == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     safe_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     inferred = True
#             if inferred:
#                 return True, safely_identified_mines

#     return inferred, safely_identified_mines

# def solve_knowledgebase_subset(knowledge_base):
#     for knowledge in knowledge_base:
#         knowledge_cells = knowledge[0]
#         knowledge_clue = knowledge[1]
#         for knowledge_nested in knowledge_base:
#             if knowledge != knowledge_nested:
#                 knowledge_cells_nested = knowledge_nested[0]
#                 knowledge_clue_nested = knowledge_nested[1]

#                 if len(knowledge_cells_nested) < len(knowledge_cells):
#                     if knowledge_cells_nested.issubset(knowledge_cells):
#                         new_knowledge = [knowledge_cells-knowledge_cells_nested, knowledge_clue-knowledge_clue_nested]
#                         if new_knowledge not in knowledge_base:
#                             # print('new knowledge:', new_knowledge)
#                             knowledge_base.append(new_knowledge)
#                             knowledge_base = solve_knowledgebase_subset(knowledge_base)
#                             return knowledge_base
#     return knowledge_base

# def solve_knowledgebase_subsequence(knowledge_base):
#     for knowledge in knowledge_base:
#         knowledge_cells = knowledge[0]
#         knowledge_clue = knowledge[1]
#         for knowledge_nested in knowledge_base:
#             if knowledge != knowledge_nested:
#                 knowledge_cells_nested = knowledge_nested[0]
#                 knowledge_clue_nested = knowledge_nested[1]

#                 if len(knowledge_cells_nested) == len(knowledge_cells):
#                     if len(knowledge_cells_nested.intersection(knowledge_cells)) == len(knowledge_cells)-1: 
#                         if knowledge_clue_nested > knowledge_clue and knowledge_clue_nested-knowledge_clue == 1:    
#                             # print('ererere')       
#                             new_knowledge = [knowledge_cells_nested-knowledge_cells_nested.intersection(knowledge_cells), 1]
#                             if new_knowledge not in knowledge_base:
#                                 knowledge_base.append(new_knowledge)
#                             new_knowledge = [knowledge_cells-knowledge_cells_nested.intersection(knowledge_cells), 0]
#                             if new_knowledge not in knowledge_base:
#                                 knowledge_base.append(new_knowledge)
#                             return knowledge_base
#     return knowledge_base

# def improved_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
#     knowledge_base = []

#     for safe_cell in safe_cells:
#         knowledge_clue = int(query(game_board, safe_cell))     
#         neighbours = get_neighbours(dim, safe_cell)

#         knowledge_cells = set()
#         for neighbour in neighbours:
#             if neighbour in mine_cells:
#                 knowledge_clue -= 1
#             if neighbour in hidden_cells:
#                 knowledge_cells.add(neighbour)

#         if knowledge_cells:
#             new_knowledge = [knowledge_cells, knowledge_clue]
#             if new_knowledge not in knowledge_base:
#                 knowledge_base.append([knowledge_cells, knowledge_clue]) 
    
    
#     # print_knowlegde_base(knowledge_base)

#     knowledge_base = solve_knowledgebase_subset(knowledge_base)
#     knowledge_base = solve_knowledgebase_subsequence(knowledge_base)


#     for knowledge in knowledge_base:
#         knowledge_cells = knowledge[0]
#         knowledge_clue = knowledge[1]

#         cell_count = len(knowledge_cells)
        
#         if knowledge_clue == 0:
#             for cell in knowledge_cells:
#                 hidden_cells.remove(cell)
#                 safe_cells.add(cell)
#             return True, 0

#         if len(knowledge_cells) == knowledge_clue:
#             for cell in knowledge_cells:
#                 hidden_cells.remove(cell)
#                 mine_cells.add(cell)
#             return True, cell_count       
                            
#     return False, 0

# dim = 20
# runs = 10
# densities_interval = 5
# dataX = range(1, dim*dim+1, densities_interval)
# dataY = []

# for mine_density in dataX:
#     safely_identified_mines = 0
#     for run in range(runs):
#         game_board = make_board(dim, mine_density)

#         safe_cells = set()
#         mine_cells = set()
#         hidden_cells = initialize_hidden_cells(dim)

#         while True:
#             if len(hidden_cells) == 0:
#                 break
#             inferred, mines = basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells)
#             if not inferred:
#                 inferred, mines = improved_agent(game_board, dim, safe_cells, mine_cells, hidden_cells)
#             if inferred:
#                 safely_identified_mines += mines
#             else:
#                 random_cell = rand.choice(tuple(hidden_cells))
#                 type_of_celll = query(game_board, random_cell)
#                 if type_of_celll.isdigit():
#                     safe_cells.add(random_cell)
#                 else:
#                     mine_cells.add(random_cell)            
#                 hidden_cells.remove(random_cell)
                
#     print(safely_identified_mines, mine_density*runs)
#     dataY.append(safely_identified_mines/(mine_density*runs))

# plt.plot(dataX, dataY)
# plt.title("Basic agent vs improved agent")
# plt.ylabel("Safely identified mines/total mines")
# plt.xlabel("Total mines")
# plt.legend(["Basic agent", "Improved agent"])
# plt.show()

### uncomment to here

### DO NOT UNCOMMENT EXTRA CODE
# # ####################### GLOBAL INFORMATION IMPROVED AGENT GRAPH ##########################
# def basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells):
#     safely_identified_mines = 0
#     inferred = False
#     for safe_cell in safe_cells:
#         mines = count_neighbouring_mines(dim, safe_cell, mine_cells)
#         safe = count_neighbouring_safe(dim, safe_cell, safe_cells)
#         hidden = count_neighbouring_hidden(dim, safe_cell, hidden_cells)
#         clue = int(query(game_board, safe_cell))       

#         if clue - mines == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     mine_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     safely_identified_mines += 1
#                     inferred = True
#             if inferred:
#                 return True, safely_identified_mines

#         if len(get_neighbours(dim, safe_cell)) - clue - safe == hidden:
#             for neighbour in get_neighbours(dim, safe_cell):
#                 if neighbour in hidden_cells:
#                     safe_cells.add(neighbour)
#                     hidden_cells.remove(neighbour)
#                     inferred = True
#             if inferred:
#                 return True, safely_identified_mines

#     return inferred, safely_identified_mines

# def solve_knowledgebase(knowledge_base):
#     for knowledge in knowledge_base:
#         knowledge_cells = knowledge[0]
#         knowledge_clue = knowledge[1]
#         for knowledge_nested in knowledge_base:
#             if knowledge != knowledge_nested:
#                 knowledge_cells_nested = knowledge_nested[0]
#                 knowledge_clue_nested = knowledge_nested[1]

#                 if len(knowledge_cells_nested) < len(knowledge_cells):
#                     if knowledge_cells_nested.issubset(knowledge_cells):
#                         new_knowledge = [knowledge_cells-knowledge_cells_nested, knowledge_clue-knowledge_clue_nested]
#                         if new_knowledge not in knowledge_base:
#                             # print('new knowledge:', new_knowledge)
#                             knowledge_base.append(new_knowledge)
#                             knowledge_base = solve_knowledgebase(knowledge_base)
#                             return knowledge_base
#     return knowledge_base
    

# def improved_agent(game_board, dim, safe_cells, mine_cells, hidden_cells, mine_left):
#     knowledge_base = []
    
#     clue_cells = set()
#     total_clue = 0

#     for safe_cell in safe_cells:
#         knowledge_clue = int(query(game_board, safe_cell))     
#         neighbours = get_neighbours(dim, safe_cell)

#         knowledge_cells = set()
#         for neighbour in neighbours:
#             if neighbour in mine_cells:
#                 knowledge_clue -= 1
#             if neighbour in hidden_cells:
#                 knowledge_cells.add(neighbour)
#                 clue_cells.add(neighbour)
                

#         if knowledge_cells:
#             new_knowledge = [knowledge_cells, knowledge_clue]
#             if new_knowledge not in knowledge_base:
#                 total_clue += knowledge_clue
#                 knowledge_base.append([knowledge_cells, knowledge_clue]) 
    
    
#     print_knowlegde_base(knowledge_base)
#     # print('-----', mine_left)
#     if mine_left != 0:
#         for knowledge in knowledge_base:
#             for nested_knowledge in knowledge_base:
#                 if len(nested_knowledge[0]) < len(knowledge[0]):
#                         if nested_knowledge[0].intersection(knowledge[0]):
#                             print('minus from total clue',nested_knowledge[1], nested_knowledge[0])
#                             total_clue -= nested_knowledge[1]
#         hidden_cell_x = set()
#         if total_clue == mine_left:
#             for hidden_cell in hidden_cells:
#                 if hidden_cell not in clue_cells:
#                     safe_cells.add(hidden_cell)
#                 else:
#                     hidden_cell_x.add(hidden_cell)
#             hidden_cells = hidden_cell_x
#             print('foifdnfd fdit', total_clue)
#             return True, 0

#     knowledge_base = solve_knowledgebase(knowledge_base)


#     for knowledge in knowledge_base:
#         knowledge_cells = knowledge[0]
#         knowledge_clue = knowledge[1]

#         cell_count = len(knowledge_cells)
        
#         if knowledge_clue == 0:
#             for cell in knowledge_cells:
#                 hidden_cells.remove(cell)
#                 safe_cells.add(cell)
#             return True, 0

#         if len(knowledge_cells) == knowledge_clue:
#             for cell in knowledge_cells:
#                 hidden_cells.remove(cell)
#                 mine_cells.add(cell)
#             return True, cell_count       
                            
#     return False, 0

# dim = 10
# runs = 10
# densities_interval = 20
# dataX = range(1, dim*dim+1, densities_interval)
# dataY = []

# for mine_density in dataX:
#     safely_identified_mines = 0
#     for run in range(runs):
#         game_board = make_board(dim, mine_density)

#         safe_cells = set()
#         mine_cells = set()
#         hidden_cells = initialize_hidden_cells(dim)
#         mine_left = mine_density

#         while True:
#             if len(hidden_cells) == 0:
#                 break
#             inferred, mines = basic_agent(game_board, dim, safe_cells, mine_cells, hidden_cells)
#             if not inferred:
#                 inferred, mines = improved_agent(game_board, dim, safe_cells, mine_cells, hidden_cells, mine_left)
#             if inferred:
#                 mine_left -= mines
#                 print('after inferred mine left',mine_left)
#                 safely_identified_mines += mines
#             else:
#                 random_cell = rand.choice(tuple(hidden_cells))
#                 type_of_celll = query(game_board, random_cell)
#                 if type_of_celll.isdigit():
#                     safe_cells.add(random_cell)
#                 else:
#                     mine_cells.add(random_cell)  
#                     mine_left -= 1          
#                 hidden_cells.remove(random_cell)
                
#     print(safely_identified_mines, mine_density*runs)
#     dataY.append(safely_identified_mines/(mine_density*runs))

# plt.plot(dataX, dataY)
# plt.title("Basic agent vs improved agent")
# plt.ylabel("Safely identified mines/total mines")
# plt.xlabel("Total mines")
# # plt.legend(["Basic agent", "Improved agent"])
# plt.show()
### DO NOT UNCOMMENT EXTRA CODE