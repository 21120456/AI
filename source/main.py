from game import Pacman, Cookie, Wall, Ghost, GameRenderer
from controller import PacmanGameController
from utils import translate_maze_to_screen
from MyApp import *
import time


def game_initialize():
    level = int(input("Input level of game (1/2/3/4): "))
    map = input("Choose map (1/2): ")
    maze_name = f"../input/level{level}_map{map}.txt"
    speed = int(input("Input game speed (ms): "))
    return maze_name, level, speed


if __name__ == "__main__":
    unified_size = 32
    run = True
    file_result = open(f"../output/result.txt", "w")
    while run:
        pacman_game = MyApp()
        pacman_game.run()

        level = pacman_game.current_level
        map = pacman_game.current_map_index
        maze_name = f"../input/level{level}_map{map}.txt"
        speed = 250

        pacman_game = PacmanGameController(maze_name)
        size = pacman_game.size
        game_renderer = GameRenderer(size[1] * unified_size, size[0] * unified_size)

        if level == 1 or level == 2:
            start = time.time()
            pacman_path = pacman_game.search.get_path_lv1_lv2()
            ghosts_path = []
            path_calculation_time = time.time() - start
        elif level == 3:
            start = time.time()
            pacman_path, ghosts_path, status = pacman_game.search.get_path_lv3()
            pacman_game.set_status(status)
            path_calculation_time = time.time() - start
        elif level == 4:
            start = time.time()
            pacman_path, ghosts_path, status = pacman_game.search.get_path_lv4()
            pacman_game.set_status(status)
            path_calculation_time = time.time() - start

        if not isinstance(pacman_path, bool):
            for y, row in enumerate(pacman_game.maze):
                for x, column in enumerate(row):
                    if column == 1:
                        game_renderer.add_wall(Wall(game_renderer, x, y, unified_size))
            for cookie_space in pacman_game.cookie_spaces:
                translated = translate_maze_to_screen(cookie_space)
                cookie = Cookie(
                    game_renderer,
                    translated[0] + unified_size / 2,
                    translated[1] + unified_size / 2,
                )
                game_renderer.add_cookie(cookie)

            for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
                translated = translate_maze_to_screen(ghost_spawn)
                ghost_path = [
                    translate_maze_to_screen(sublist[i]) for sublist in ghosts_path
                ]
                ghost = Ghost(
                    game_renderer,
                    translated[0],
                    translated[1],
                    unified_size,
                    pacman_game,
                    ghost_path,
                    pacman_game.ghost_colors[i % 4],
                )
                game_renderer.add_ghost(ghost)

            pacman_path = [translate_maze_to_screen(item) for item in pacman_path]

            pacman = Pacman(
                game_renderer,
                pacman_game,
                pacman_game.pacman_pos[0] * unified_size,
                pacman_game.pacman_pos[1] * unified_size,
                unified_size,
                pacman_path,
            )

            game_renderer.add_hero(pacman)
            game_renderer.set_level(level)
            start = time.time()
            game_renderer.tick(speed)
            execution_time = time.time() - start
            file_result.write("Level: ")
            file_result.write(str(level) + "\n")
            file_result.write("Map: ")
            file_result.write(str(map) + "\n")
            file_result.write("Path calculation time:")
            file_result.write(str(path_calculation_time) + "\n")
            file_result.write("Execution time:")
            file_result.write(str(execution_time) + "\n")
        else:
            file_result.write("Cant find any path to get to the food")
