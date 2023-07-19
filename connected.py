from collections import deque

def is_connected(tilmap, start, end):
    rows = len(tilmap)
    cols = len(tilmap[0])
    
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True
    
    while queue:
        current = queue.popleft()
        if current == end:
            return True
        
        row, col = current
        neighbors = get_neighbors(row, col, rows, cols)
        
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if not visited[n_row][n_col] and tilmap[n_row][n_col] == ' ':
                queue.append(neighbor)
                visited[n_row][n_col] = True
    
    return False

def get_neighbors(row, col, rows, cols):
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors