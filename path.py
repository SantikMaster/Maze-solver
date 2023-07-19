from collections import deque

def find_shortest_path(grid, start, end):
    # Get the dimensions of the grid
    rows = len(grid)
    cols = len(grid[0])

    # Create a queue for BFS
    queue = deque([(start, [])])  # (position, path)

    # Keep track of visited positions
    visited = set([start])
    #print(visited)
    # Define possible movements (up, down, left, right)
    movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        position, path = queue.popleft()

        if position == end:
            return path + [position]

        for dx, dy in movements:
            new_x = position[0] + dx
            new_y = position[1] + dy

            # Check if the new position is valid and unvisited
            if 0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] == ' ' and (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), path + [position]))
                visited.add((new_x, new_y))
                #print((new_x, new_y))

    # If no path is found
    return None

