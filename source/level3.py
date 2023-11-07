import random

def heuristic(node, goal):
    # Euclidean distance heuristic
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5


def get_neighbors(pos, maze):
    neighbors = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up

    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        if (
            0 <= x < len(maze)
            and 0 <= y < len(maze[0])
            and (maze[x][y] == 0 or maze[x][y] == 2)
        ):
            neighbors.append((x, y))

    return neighbors

def get_neighbors_blind_search(pos, maze, ghosts):
    neighbors = []
    scopeLength = 4
    directions = [(scopeLength, 0), (0, scopeLength), (-scopeLength, 0), (0, -scopeLength)]

    while (len(neighbors) == 0):
        scopeLength -= 1
        directions = [(scopeLength, 0), (0, scopeLength), (-scopeLength, 0), (0, -scopeLength)]

        for dx, dy in directions:
            x, y = pos[0] + dx, pos[1] + dy
            if (
                0 <= x < len(maze)
                and 0 <= y < len(maze[0])
                and (maze[x][y] == 0 or maze[x][y] == 2)
                and  check_safe_move((x, y), ghosts)
            ):
                neighbors.append((x, y))

        if (scopeLength == 1):
            break

    return neighbors

def get_ghost_neighbors(pos, maze):
    neighbors = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up

    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != 1:
            neighbors.append((x, y))

    return neighbors


def check_safe_move(pos, ghosts):
    for ghost in ghosts:
        if heuristic(pos, ghost) <= 1:
            return False
    return True


def get_moveable_pos(maze, pos, ghosts):
    res = []
    neighbors = get_neighbors_blind_search(pos, maze, ghosts)
    for neighbor in neighbors:
        res.append(neighbor)
    return res


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


def find_object(maze, entity):
    res = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == entity:
                res.append((i, j))
    return res



def astar(maze, start, goal):
    start_node = tuple(start)

    queue = [(heuristic(start_node, goal), start_node, 0)]  # Using a queue: (total_cost, current_node, score)
    queueDistance = dict()
    visited = set()
    came_from = {}

    while queue:
        distance, current_node, score = queue.pop(0)

        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        visited.add(current_node)

        for neighbor in get_neighbors(current_node, maze):
            total_cost = (distance - heuristic(current_node, goal) +  1) + heuristic(neighbor, goal)
            if ((neighbor not in queueDistance) or (neighbor in queueDistance  and total_cost < queueDistance[neighbor])) and neighbor not in visited:
                queueDistance[neighbor] = total_cost
                came_from[neighbor] = current_node
                queue.append((total_cost, neighbor, score - 1))

        queue.sort(
            key=lambda x: x[0], reverse=False
        ) 
   
    return reconstruct_path(came_from, current_node) 


def change_path(pacmanPos, ghosts, mazePacman):
    moveablePos = get_neighbors(pacmanPos, mazePacman)
    for pos in moveablePos:
        if check_safe_move(pos, ghosts) == True:
            pacmanPos = pos
            break
    return pacmanPos


def ghost_move(maze, ghosts, mazePacman):
    ghostsPos = []
    for ghost in ghosts:
        neighbors = get_ghost_neighbors(ghost, maze)
        if (len(neighbors) == 0):
            continue

        move = random.choice(neighbors)
        maze[move[0]][move[1]] = 3
        maze[ghost[0]][ghost[1]] = 0
        ghostsPos.append(move)
    return maze, ghostsPos, mazePacman

def initMazePacmanView(maze):
    rows = len(maze)
    cols = len(maze[0])

    # Khởi tạo mảng  2 chiều mới với kích thước và giá trị như yêu cầu
    mazePacman = [[4 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                mazePacman[i][j] = 1
    return mazePacman


def update_maze_pacman(maze, mazePacman, pacmanPos, mazeFood):
    rows = len(maze)
    cols = len(maze[0])
    top = (pacmanPos[0] - 3) if (pacmanPos[0] - 3) > 0 else 1
    down = (pacmanPos[0] + 3) if (pacmanPos[0] + 3) < (rows - 1) else (rows - 2)
    left = (pacmanPos[1] - 3) if (pacmanPos[1] - 3) > 0 else 1
    right = (pacmanPos[1] + 3) if (pacmanPos[1] + 3) < (cols - 1) else (cols - 2)

    for i in range(top - 4, down + 4):
        if i >= 0 and i <= rows - 1:
            for j in range(left - 4, right + 4):
                if j >= 0 and j <= cols - 1:
                    mazePacman[i][j] = 4
                    if (abs(i - pacmanPos[0]) + abs(j - pacmanPos[1]) <= 3) or maze[i][j] == 1:
                        mazePacman[i][j] = maze[i][j]
                        if mazeFood[i][j] == 2:
                            mazePacman[i][j] = mazeFood[i][j]

    return mazePacman


def initfoodmaze(maze):
    mazeFood = [[maze[row][col] for col in range(len(maze[0]))] for row in range(len(maze))]
    return mazeFood


def eatFood(maze, pacmanPos, foods, countFood, mazePacman,mazeFood):
    if pacmanPos in foods:
        foods.pop(foods.index(pacmanPos))
        maze[pacmanPos[0]][pacmanPos[1]] = 0
        mazePacman[pacmanPos[0]][pacmanPos[1]] = 0
        mazeFood[pacmanPos[0]][pacmanPos[1]] = 0
        countFood = countFood - 1

    return maze, foods, mazePacman, countFood

def changeGoal(pacmanPos, foods, ghosts, mazePacman):
    foodsSorted = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
    foods = foodsSorted

    movevablePos = get_moveable_pos(mazePacman, pacmanPos, ghosts)
    if foods:
        res = foods[0]
    elif len(movevablePos) > 0:       
        res = movevablePos[random.randint(0,len(movevablePos) - 1)]
    else:
        res = 0 
    return res



def handleAStar(maze, start, goal, foods, ghosts, countFood, mazePacman, mazeFood):
    pacmanPos = start
    pathSolution = [pacmanPos]
    ghostsPath = [ghosts]
    blocked = 0

    while True:
        mazePacman = update_maze_pacman(maze, mazePacman, pacmanPos, mazeFood)
        foods = find_object(mazePacman, 2)
        # foods = find_object(mazeFood, 2)
        print("_______________")
        print(f"length food: {len(foods)}")
        print(f"count food: {countFood}")
        print(foods)

        if (countFood == 0):
            break
        if pacmanPos == goal:
            maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman, mazeFood)
            if (countFood == 0):
                break

        goal = changeGoal(pacmanPos, foods, ghosts, mazePacman)
        
        if goal == 0:
            blocked += 1
            if (blocked == 5):
                print("Lose blocked")
                return maze, pathSolution, foods, ghosts, ghostsPath, "blocked", countFood, mazePacman
            else:
                pathSolution.append(pacmanPos)
                maze, ghosts, mazePacman = ghost_move(maze, ghosts, mazePacman)
                ghostsPath.append(ghosts)
                if pacmanPos in ghosts:
                    print("Lose dead")
                    return maze, pathSolution, foods, ghosts, ghostsPath, "dead", countFood, mazePacman
                continue
        
        pacmanPath = astar(maze, pacmanPos, goal)
        
        if len(pacmanPath) == 1:
            maze, ghosts, mazePacman = ghost_move(maze, ghosts, mazePacman)
            ghostsPath.append(ghosts)
            pacmanPos = pacmanPath[0]
            pathSolution.append(pacmanPos)
            maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman, mazeFood)
        else:
            pacmanPos = pacmanPath.pop(0)
            maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman, mazeFood)

            for pos in pacmanPath:
                maze, ghosts, mazePacman = ghost_move(maze, ghosts, mazePacman)
                mazePacman = update_maze_pacman(maze, mazePacman, pacmanPos, mazeFood)
                isSafe = check_safe_move(pos, ghosts)
                ghostsPath.append(ghosts)
                
                if (isSafe):
                    pacmanPos = pos
                    pathSolution.append(pacmanPos)
                else:
                    # mazePacman = update_maze_pacman(maze, mazePacman, pacmanPos, mazeFood)
                    pacmanPos = change_path(pacmanPos, ghosts, mazePacman)
                    maze, foods, mazePacman, countFood = eatFood(maze, pacmanPos, foods, countFood, mazePacman, mazeFood)
                    pathSolution.append(pacmanPos)
                    if pacmanPos in ghosts:
                        print("Lose dead")
                        return maze, pathSolution, foods, ghosts, ghostsPath, "dead", countFood, mazePacman
                    break

    print("Win")
    return maze, pathSolution, foods, ghosts, ghostsPath, "alive", countFood, mazePacman


def handleMainLv3(maze, start):
    start = [start[1],start[0]]

    mazeFood = initfoodmaze(maze)
    mazePacman = initMazePacmanView(maze)

    pacmanPos = tuple(start)
    pacmanRes = [start]
    mazePacman = update_maze_pacman(maze, mazePacman, pacmanPos, mazeFood)

    ghosts = find_object(maze, 3)
    ghostsRes = [ghosts]
    
    countFood = len(find_object(maze, 2))

    foods = find_object(mazePacman, 2)  
    foods = sorted(foods, key=lambda food: heuristic(pacmanPos, food))
    
    if (len(foods) > 0):
        value = foods[0]
    else:
        value = {}

    maze, pacmanPath, foods, ghosts, ghostsPath, status, countFood, mazePacman = handleAStar(
        maze, pacmanPos, value, foods, ghosts, countFood, mazePacman, mazeFood
    )
    
    pacmanPos = pacmanPath[len(pacmanPath) - 1]
    pacmanRes += pacmanPath[1:]
    ghostsRes += ghostsPath[1:]
    
    
    # print("PACMAN", pacmanRes)
    # print("GHOSTS", ghostsRes)
    
    return pacmanRes, ghostsRes, status