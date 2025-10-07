import pygame
import random
import heapq
import os

WIDTH, HEIGHT = 600,600
GRID_SIZE = 33
ROWS = HEIGHT//GRID_SIZE
COLS = WIDTH//GRID_SIZE

BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.g = float('inf')  
        self.f = float('inf')  
        self.parent = None  
    def draw(self, win):
        if self.walls["top"]:
            pygame.draw.line(win, BLACK, (self.x, self.y), (self.x + GRID_SIZE, self.y), 2)
        if self.walls["right"]:
            pygame.draw.line(win, BLACK, (self.x + GRID_SIZE, self.y), (self.x + GRID_SIZE, self.y + GRID_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(win, BLACK, (self.x + GRID_SIZE, self.y + GRID_SIZE), (self.x, self.y + GRID_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(win, BLACK, (self.x, self.y + GRID_SIZE), (self.x, self.y), 2)

    def highlight(self, win, color):
        pygame.draw.rect(win, color, (self.x + 2, self.y + 2, GRID_SIZE - 4, GRID_SIZE - 4))
    def __lt__(self, other):
        return self.f < other.f
def remove_walls(current, next):
    dx = current.col - next.col
    dy = current.row - next.row

    if dx == 1: 
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False
    elif dy == 1:
        current.walls["top"] = False
        next.walls["bottom"] = False
    elif dy == -1: 
        current.walls["bottom"] = False
        next.walls["top"] = False
def generate_maze(grid):
    walls = []
    start = grid[0][0]
    start.visited = True
    walls.extend(get_neighbors(start, grid))

    while walls:
        wall = random.choice(walls)
        x, y, direction = wall
        current_cell = grid[x][y]
        next_cell = get_adjacent_cell(x, y, direction, grid)

        if next_cell and not next_cell.visited:
            remove_walls(current_cell, next_cell)
            next_cell.visited = True
            walls.extend(get_neighbors(next_cell, grid))

        walls.remove(wall)


def get_neighbors(cell, grid):
    neighbors = []
    for direction in DIRECTIONS:
        dx, dy = direction
        nx, ny = cell.row + dx, cell.col + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS:
            neighbors.append((cell.row, cell.col, direction))
    return neighbors


def get_adjacent_cell(x, y, direction, grid):
    dx, dy = direction
    nx, ny = x + dx, y + dy
    if 0 <= nx < ROWS and 0 <= ny < COLS:
        return grid[nx][ny]
    return None
def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)
def a_star(grid, start, goal):
    open_list = []
    closed_list = set()
    start.g = 0
    start.f = heuristic(start, goal)
    heapq.heappush(open_list, (start.f, start))

    while open_list:
        current = heapq.heappop(open_list)[1]
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]  

        closed_list.add(current)
        for dx, dy in DIRECTIONS:
            nx, ny = current.row + dx, current.col + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                neighbor = grid[nx][ny]

                if (dx == -1 and current.walls["top"]) or \
                   (dx == 1 and current.walls["bottom"]) or \
                   (dy == -1 and current.walls["left"]) or \
                   (dy == 1 and current.walls["right"]):
                    continue

                if neighbor in closed_list:
                    continue

                tentative_g = current.g + 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.f = neighbor.g + heuristic(neighbor, goal)
                    if not any(neighbor == item[1] for item in open_list):
                        heapq.heappush(open_list, (neighbor.f, neighbor))

    return [] 
def opposite_direction(dx, dy):
    if dx == -1 and dy == 0:
        return "bottom"
    elif dx == 1 and dy == 0:
        return "top"
    elif dx == 0 and dy == -1:
        return "right"
    elif dx == 0 and dy == 1:
        return "left"
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MaZE Mania")
    player_image = pygame.image.load(r"D:\MISSIONAP\Doraemon.png")  
    player_image = pygame.transform.scale(player_image, (GRID_SIZE, GRID_SIZE))
    goal_image = pygame.image.load(r"D:\MISSIONAP\Nobita.jpg")  
    goal_image = pygame.transform.scale(goal_image, (GRID_SIZE, GRID_SIZE)) 

    grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
    generate_maze(grid)
    player_row, player_col = 0, 0
    goal_row, goal_col = ROWS - 1, COLS - 1
    start_cell = grid[player_row][player_col]
    goal_cell = grid[goal_row][goal_col]
    path = a_star(grid, start_cell, goal_cell)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)
        win.fill(BEIGE)
        for row in grid:
            for cell in row:
                cell.draw(win)
        for cell in path:
            cell.highlight(win, TEAL)
        player_x = player_col * GRID_SIZE
        player_y = player_row * GRID_SIZE
        win.blit(player_image, (player_x, player_y))
        goal_x = goal_col * GRID_SIZE
        goal_y = goal_row * GRID_SIZE
        win.blit(goal_image, (goal_x, goal_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not grid[player_row][player_col].walls["top"]:
                    player_row -= 1
                if event.key == pygame.K_DOWN and not grid[player_row][player_col].walls["bottom"]:
                    player_row += 1
                if event.key == pygame.K_LEFT and not grid[player_row][player_col].walls["left"]:
                    player_col -= 1
                if event.key == pygame.K_RIGHT and not grid[player_row][player_col].walls["right"]:
                    player_col += 1
        if player_row == ROWS - 1 and player_col == COLS - 1:
            print("You reached the goal!")
            running = False  

        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":

    main()
