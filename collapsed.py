import random

T1 = [['@', '@', '@'],
      [' ', ' ', ' '],
      ['@', ' ', '@']]
T2 = [['@', ' ', '@'],
      [' ', ' ', ' '],
      ['@', '@', '@']]

T3 = [['@', ' ', '@'],
      ['@', ' ', ' '],
      ['@', ' ', '@']]

T4 = [['@', ' ', '@'],
      [' ', ' ', '@'],
      ['@', ' ', '@']]

I1 = [['@', '@', '@'],
      [' ', ' ', ' '],
      ['@', '@', '@']]
I2 = [['@', ' ', '@'],
      ['@', ' ', '@'],
      ['@', ' ', '@']]

O1 = [['@', ' ', '@'],
      [' ', ' ', ' '],
      ['@', ' ', '@']]

E1 = [['@', '@', '@'],
      ['@', ' ', '@'],
      ['@', ' ', '@']]

E2 = [['@', ' ', '@'],
      ['@', ' ', '@'],
      ['@', '@', '@']]

E3 = [['@', '@', '@'],
      ['@', ' ', ' '],
      ['@', '@', '@']]

E4 = [['@', '@', '@'],
      [' ', ' ', '@'],
      ['@', '@', '@']]

A1 = [['@', '@', '@'],
      ['@', '@', '@'],
      ['@', '@', '@']]

L1 = [['@', '@', '@'],
      ['@', ' ', ' '],
      ['@', ' ', '@']]

L2 = [['@', ' ', '@'],
      [' ', ' ', '@'],
      ['@', '@', '@']]

L3 = [['@', '@', '@'],
      ['@', ' ', ' '],
      ['@', ' ', '@']]

L4 = [['@', '@', '@'],
      [' ', ' ', '@'],
      ['@', ' ', '@']]

tiles = [T1, T2, T3, T4, I1, I2, O1, E1, E2, E3, E4, A1, L1, L2, L3, L4, L1, L2, L3, L4, T1, T2, T3, T4]

def calculate_entropy(valid_tiles):
    #unique_tiles = set(valid_tiles)
    return len(valid_tiles)


def generate_map(width, height):
    map_grid = [[' ' for _ in range(width)] for _ in range(height)]
    tile_size = 3

    # Place the first tile randomly
    first_tile = random.choice(tiles)
    place_tile(map_grid, first_tile, 0, 0)

    # Generate the map by placing tiles that match at their edges
    while True:
        empty_cells = get_cells(map_grid)
        if len(empty_cells) == 0:
            break

        cell = random.choice(empty_cells)
        minenropy = 100
        for cells in empty_cells:
            x, y = cells[0], cells[1]
            valid_tiles = get_valid_tiles(map_grid, x, y)
            entropy = calculate_entropy(valid_tiles)
            if (entropy<minenropy):
                minenropy=entropy
                cell = cells


        x, y = cell[0], cell[1]
        valid_tiles = get_valid_tiles(map_grid, x, y)
        #entropy = calculate_entropy(valid_tiles)


        if len(valid_tiles) == 0:
            raise ValueError("No valid tiles to place at position ({}, {})".format(x, y))

        tile = random.choice(valid_tiles)
        place_tile(map_grid, tile, x, y)

    mapsize=len(map_grid[0])
    for i in range(mapsize):
        map_grid[0][i] = '@'
        map_grid[i][0] = '@'
        map_grid[mapsize-1][i] = '@'
        map_grid[i][mapsize-1] = '@'
    return map_grid

def get_empty_cells(map_grid):
    empty_cells = []

    for y in range(len(map_grid)):
        for x in range(len(map_grid[0])):
            if map_grid[y][x] == ' ':
                empty_cells.append((x, y))
    return empty_cells


def get_cells(map_grid):
    empty_cells = []

    for y in range(0,len(map_grid),3):
        for x in range(0,len(map_grid[0]),3):
            if map_grid[y][x] == ' ':
                empty_cells.append((x, y))
    return empty_cells

def get_valid_tiles(map_grid, x, y):
    valid_tiles = []
    for tile in tiles:
        if is_valid_tile(map_grid, tile, x, y):
            valid_tiles.append(tile)
    return valid_tiles

def is_valid_tile(map_grid, tile, x, y):
    tile_size = len(tile)
    if x + tile_size > len(map_grid[0]) or y + tile_size > len(map_grid):
        print('Wrong grid size')
        return False

#check every edge
    mapsize=len(map_grid[0])

    #we check if the corners of tilemap is @ then it is not empty
    #if it is not empty then we check the middle of the tiles edge to coincide
    if x>0 :
        if(map_grid[y ][x-1] == '@' and tile[1][0] != map_grid[y + 1][x-1]):
            return False    #left edge
    if x<mapsize-3:
        if(map_grid[y ][x+3] == '@' and tile[1][2] != map_grid[y + 1][x+3]):
            return False    #right edge

    if y>0 :
        if(map_grid[y-1][x] == '@' and tile[0 ][1] != map_grid[y -1][x+1]):
            return False
    if y<mapsize-3 :
        if(map_grid[y+3][x] == '@' and tile[2][1] != map_grid[y+3][x+1]):
            return False

    return True

def place_tile(map_grid, tile, x, y):
    tile_size = len(tile)
    for j in range(tile_size):
        for i in range(tile_size):
            map_grid[y + j][x + i] = tile[j][i]

