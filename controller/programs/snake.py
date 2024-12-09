from __future__ import annotations

import math
import time
from copy import deepcopy
from random import randrange
from threading import Thread

import numpy as np

from controller.data import PixelDisplay, dimensions, draw_lines_on

BIN = 4
# Ensure BIN is divisible by 4
assert BIN % 4 == 0, "BIN must be divisible by 4"

GAME_HEIGHT = math.floor(dimensions.height / BIN)
GAME_WIDTH = math.floor(dimensions.width / BIN)

# Colors
SURFACE_CLR = (0, 0, 0)
APPLE_CLR = (220, 50, 50)
SNAKE_CLR = (50, 220, 50)
HEAD_CLR = (90, 120, 190)

# Game Settings
INITIAL_SNAKE_LENGTH = 3
WAIT_SECONDS_AFTER_WIN = 15
MAX_MOVES_WITHOUT_EATING = GAME_HEIGHT * GAME_WIDTH * 10
SNAKE_MAX_LENGTH = GAME_HEIGHT * GAME_WIDTH - INITIAL_SNAKE_LENGTH

# Variables used in BFS algorithm
GRID = [[i, j] for i in range(GAME_WIDTH) for j in range(GAME_HEIGHT)]


# Helper functions
def get_neighbors(position):
    neighbors = [
        [position[0] + 1, position[1]],
        [position[0] - 1, position[1]],
        [position[0], position[1] + 1],
        [position[0], position[1] - 1],
    ]
    in_grid_neighbors = []
    for pos in neighbors:
        if pos in GRID:
            in_grid_neighbors.append(pos)
    return in_grid_neighbors


def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


# Each position is a tuple because python doesn't allow hashing lists
ADJACENCY_DICT = {tuple(pos): get_neighbors(pos) for pos in GRID}


class Square:
    def __init__(self, pos, is_apple=False):
        self.pos = pos
        self.is_apple = is_apple
        self.is_tail = False
        self.dir = [-1, 0]  # [x, y] Direction

        if self.is_apple:
            self.dir = [0, 0]

    def move(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    def hitting_wall(self):
        if (
            (self.pos[0] <= -1)
            or (self.pos[0] >= GAME_WIDTH)
            or (self.pos[1] <= -1)
            or (self.pos[1] >= GAME_HEIGHT)
        ):
            return True
        else:
            return False


class Snake:

    _BG = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)

    def __init__(self):
        self.reset()

    def reset(self):
        self.is_dead = False
        self.squares_start_pos = [
            [GAME_WIDTH // 2 + i, GAME_HEIGHT // 2] for i in range(INITIAL_SNAKE_LENGTH)
        ]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square(
            [randrange(GAME_WIDTH), randrange(GAME_HEIGHT)], is_apple=True
        )

        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True

        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

        self._pixels = self._BG.copy()

    @property
    def pixels(self) -> PixelDisplay:
        return self._pixels

    def start(self):
        Thread(target=self._main_loop, daemon=True).start()

    def _main_loop(self):
        debounce = 0.01
        last_t = time.monotonic
        while True:
            self.update()
            self._pixels = self._snake_pixels()
            t = time.monotonic()
            time.sleep(max(0.01, debounce - (t - last_t())))

    def _snake_pixels(self):
        pixels = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)

        # Prepare arrays to store directions and segment types
        curr_directions = np.zeros((GAME_HEIGHT, GAME_WIDTH, 2), dtype=np.int32)
        prev_directions = np.zeros((GAME_HEIGHT, GAME_WIDTH, 2), dtype=np.int32)
        next_directions = np.zeros((GAME_HEIGHT, GAME_WIDTH, 2), dtype=np.int32)
        segment_types = np.zeros(
            (GAME_HEIGHT, GAME_WIDTH), dtype=np.int32
        )  # 0: straight, 1: corner, 2: tail, 3: head

        # Draw apple
        apple_x, apple_y = self.apple.pos[0], self.apple.pos[1]
        x_start = apple_x * BIN
        y_start = apple_y * BIN
        pixels[y_start : y_start + BIN, x_start : x_start + BIN] = APPLE_CLR

        # Draw snake
        for idx, sqr in enumerate(self.squares):
            x_grid, y_grid = sqr.pos[0], sqr.pos[1]

            # Store current direction
            curr_directions[y_grid, x_grid] = sqr.dir

            # Store previous and next directions
            if idx > 0:
                prev_dir = [
                    self.squares[idx - 1].pos[0] - sqr.pos[0],
                    self.squares[idx - 1].pos[1] - sqr.pos[1],
                ]
            else:
                prev_dir = [0, 0]  # Head segment has no previous segment

            if idx < len(self.squares) - 1:
                next_dir = [
                    self.squares[idx + 1].pos[0] - sqr.pos[0],
                    self.squares[idx + 1].pos[1] - sqr.pos[1],
                ]
            else:
                next_dir = [0, 0]  # Tail segment has no next segment

            prev_directions[y_grid, x_grid] = prev_dir
            next_directions[y_grid, x_grid] = next_dir

            # Determine the segment type
            if idx == 0:
                segment_types[y_grid, x_grid] = 3  # Head segment
            elif idx == len(self.squares) - 1:
                segment_types[y_grid, x_grid] = 2  # Tail segment
            elif prev_dir != next_dir:
                segment_types[y_grid, x_grid] = 1  # Corner
            else:
                segment_types[y_grid, x_grid] = 0  # Straight

            # Draw the segment directly onto the pixels array
            x_start = x_grid * BIN
            y_start = y_grid * BIN
            color = HEAD_CLR if idx == 0 else SNAKE_CLR
            if segment_types[y_grid, x_grid] == 0:  # Straight segment
                dir_x, dir_y = sqr.dir
                if dir_x != 0:  # Horizontal movement
                    # Draw horizontal line
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start : x_start + BIN,
                    ] = color
                elif dir_y != 0:  # Vertical movement
                    # Draw vertical line
                    pixels[
                        y_start : y_start + BIN,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color
            elif segment_types[y_grid, x_grid] == 1:  # Corner segment
                # Draw a 2x2 square in the center
                pixels[
                    y_start + BIN // 4 : y_start + 3 * BIN // 4,
                    x_start + BIN // 4 : x_start + 3 * BIN // 4,
                ] = color

                # Extend lines based on previous direction
                prev_dir_x, prev_dir_y = prev_directions[y_grid, x_grid]
                if prev_dir_x == -1:
                    # Left extension
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start : x_start + BIN // 2,
                    ] = color
                elif prev_dir_x == 1:
                    # Right extension
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start + BIN // 2 : x_start + BIN,
                    ] = color
                if prev_dir_y == -1:
                    # Up extension
                    pixels[
                        y_start : y_start + BIN // 2,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color
                elif prev_dir_y == 1:
                    # Down extension
                    pixels[
                        y_start + BIN // 2 : y_start + BIN,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color

                # Extend lines based on next direction
                next_dir_x, next_dir_y = next_directions[y_grid, x_grid]
                if next_dir_x == -1:
                    # Left extension
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start : x_start + BIN // 2,
                    ] = color
                elif next_dir_x == 1:
                    # Right extension
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start + BIN // 2 : x_start + BIN,
                    ] = color
                if next_dir_y == -1:
                    # Up extension
                    pixels[
                        y_start : y_start + BIN // 2,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color
                elif next_dir_y == 1:
                    # Down extension
                    pixels[
                        y_start + BIN // 2 : y_start + BIN,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color
            elif segment_types[y_grid, x_grid] == 2:  # Tail segment
                # Draw a half-piece connected to the previous segment
                prev_dir_x, prev_dir_y = prev_directions[y_grid, x_grid]

                # Draw a small square at the center
                pixels[
                    y_start + BIN // 4 : y_start + 3 * BIN // 4,
                    x_start + BIN // 4 : x_start + 3 * BIN // 4,
                ] = color

                # Extend line based on previous direction only
                if prev_dir_x == -1:
                    # Left extension
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start : x_start + BIN // 2,
                    ] = color
                elif prev_dir_x == 1:
                    # Right extension
                    pixels[
                        y_start + BIN // 4 : y_start + 3 * BIN // 4,
                        x_start + BIN // 2 : x_start + BIN,
                    ] = color
                if prev_dir_y == -1:
                    # Up extension
                    pixels[
                        y_start : y_start + BIN // 2,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color
                elif prev_dir_y == 1:
                    # Down extension
                    pixels[
                        y_start + BIN // 2 : y_start + BIN,
                        x_start + BIN // 4 : x_start + 3 * BIN // 4,
                    ] = color

            elif segment_types[y_grid, x_grid] == 3:  # Head segment
                dir_x, dir_y = sqr.dir
                # Adjust the head size to 3x2 pixels
                # head_width = 4
                # head_height = 3

                if dir_x != 0:  # Moving horizontally
                    if dir_x == -1:
                        # Moving left
                        pixels[
                            y_start + BIN // 4 : y_start + 3 * BIN // 4,
                            x_start + BIN // 4 : x_start + 4,
                        ] = color
                    else:
                        # Moving right
                        pixels[
                            y_start + BIN // 4 : y_start + 3 * BIN // 4,
                            x_start + BIN - 4 : x_start + BIN - BIN // 4,
                        ] = color
                elif dir_y != 0:  # Moving vertically
                    if dir_y == -1:
                        # Moving up
                        pixels[
                            y_start + BIN // 4 : y_start + 4,
                            x_start + BIN // 4 : x_start + 3 * BIN // 4,
                        ] = color
                    else:
                        # Moving down
                        pixels[
                            y_start + BIN - 4 : y_start + BIN - BIN // 4,
                            x_start + BIN // 4 : x_start + 3 * BIN // 4,
                        ] = color
        return pixels

    def set_direction(self, direction):
        if direction == "left":
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def move(self):
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.move([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.move(sqr.dir)
        self.moves_without_eating += 1

    def add_square(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]

        direction = tail.dir
        if direction == [1, 0]:
            self.squares.append(Square([tail.pos[0] - 1, tail.pos[1]]))
        if direction == [-1, 0]:
            self.squares.append(Square([tail.pos[0] + 1, tail.pos[1]]))
        if direction == [0, 1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] - 1]))
        if direction == [0, -1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] + 1]))

        self.squares[-1].dir = direction
        self.squares[-1].is_tail = True

    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    def generate_apple(self):
        self.apple = Square(
            [randrange(GAME_WIDTH), randrange(GAME_HEIGHT)], is_apple=True
        )
        if not self.is_position_free(self.apple.pos):
            self.generate_apple()

    def eating_apple(self):
        if (
            self.head.pos == self.apple.pos
            and not self.is_virtual_snake
            and not self.won_game
        ):
            self.generate_apple()
            self.moves_without_eating = 0
            self.score += 1
            return True

    def go_to(self, position):
        if self.head.pos[0] - 1 == position[0]:
            self.set_direction("left")
        if self.head.pos[0] + 1 == position[0]:
            self.set_direction("right")
        if self.head.pos[1] - 1 == position[1]:
            self.set_direction("up")
        if self.head.pos[1] + 1 == position[1]:
            self.set_direction("down")

    def is_position_free(self, position):
        if (
            position[0] >= GAME_WIDTH
            or position[0] < 0
            or position[1] >= GAME_HEIGHT
            or position[1] < 0
        ):
            return False
        for sqr in self.squares:
            if sqr.pos == position:
                return False
        return True

    # Breadth First Search Algorithm
    def bfs(self, s, e):
        q = [s]
        visited = {tuple(pos): False for pos in GRID}

        visited[s] = True
        prev = {tuple(pos): None for pos in GRID}

        while q:
            node = q.pop(0)
            if node == e:
                break
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = e

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:  # type: ignore
                return []
            p_node = prev[p_node]
            if p_node == s:
                path.append(e)
                return path
            path.insert(0, p_node)

        return []

    def create_virtual_snake(self):
        v_snake = Snake()
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_square()

        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = deepcopy(self.squares[i].pos)
            sqr.dir = deepcopy(self.squares[i].dir)

        v_snake.dir = deepcopy(self.dir)
        v_snake.turns = deepcopy(self.turns)
        v_snake.apple.pos = deepcopy(self.apple.pos)
        v_snake.apple.is_apple = True
        v_snake.is_virtual_snake = True

        return v_snake

    def get_path_to_tail(self):
        tail_pos = deepcopy(self.squares[-1].pos)
        self.squares.pop(-1)
        path = self.bfs(tuple(self.head.pos), tuple(tail_pos))
        self.add_square()
        return path

    def get_available_neighbors(self, pos):
        valid_neighbors = []
        neighbors = get_neighbors(tuple(pos))
        for n in neighbors:
            if self.is_position_free(n) and self.apple.pos != n:
                valid_neighbors.append(tuple(n))
        return valid_neighbors

    def longest_path_to_tail(self):
        neighbors = self.get_available_neighbors(self.head.pos)
        path = []
        if neighbors:
            dis = -9999
            for n in neighbors:
                if distance(n, self.squares[-1].pos) > dis:
                    v_snake = self.create_virtual_snake()
                    v_snake.go_to(n)
                    v_snake.move()
                    if v_snake.eating_apple():
                        v_snake.add_square()
                    if v_snake.get_path_to_tail():
                        path.append(n)
                        dis = distance(n, self.squares[-1].pos)
            if path:
                return [path[-1]]

    def any_safe_move(self):
        neighbors = self.get_available_neighbors(self.head.pos)
        path = []
        if neighbors:
            path.append(neighbors[randrange(len(neighbors))])
            v_snake = self.create_virtual_snake()
            for move in path:
                v_snake.go_to(move)
                v_snake.move()
            if v_snake.get_path_to_tail():
                return path
            else:
                return self.get_path_to_tail()

    def set_path(self):
        if self.score == SNAKE_MAX_LENGTH - 1 and self.apple.pos in get_neighbors(
            self.head.pos
        ):
            winning_path = [tuple(self.apple.pos)]
            print("Snake is about to win..")
            return winning_path

        v_snake = self.create_virtual_snake()
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))
        path_2 = []

        if path_1:
            for pos in path_1:
                v_snake.go_to(pos)
                v_snake.move()

            v_snake.add_square()
            path_2 = v_snake.get_path_to_tail()

        if path_2:
            return path_1

        if (
            self.longest_path_to_tail()
            and self.score % 2 == 0
            and self.moves_without_eating < MAX_MOVES_WITHOUT_EATING / 2
        ):
            return self.longest_path_to_tail()

        if self.any_safe_move():
            return self.any_safe_move()

        if self.get_path_to_tail():
            return self.get_path_to_tail()

        print("No available path, snake in danger!")

    def update(self):
        path = self.set_path()
        if path:
            self.go_to(path[0])

        self.move()

        def show_result(is_dead: bool):
            if is_dead:
                lines = ["The Snake", "Is Dead", "", f"{self.total_moves} Moves"]
                color = APPLE_CLR
            else:
                color = SNAKE_CLR
                lines = [
                    "The Snake",
                    "Wins",
                    "",
                    f"{self.total_moves} Moves",
                ]

            color_pixels = np.full(
                (dimensions.height, dimensions.width, 3), color, dtype=np.int32
            )

            for _ in range(3):
                self._pixels = color_pixels
                time.sleep(0.4)
                self._pixels = self._BG.copy()
                time.sleep(0.4)

            self._pixels = draw_lines_on(pixels=self._BG.copy(), lines=lines)
            time.sleep(5)

        if self.score == GAME_WIDTH * GAME_HEIGHT - INITIAL_SNAKE_LENGTH:
            self.won_game = True
            print("Snake won the game after {} moves".format(self.total_moves))
            show_result(self.is_dead)
            self.reset()

        self.total_moves += 1

        if self.hitting_self() or self.head.hitting_wall():
            print("Snake is dead, trying again..")
            self.is_dead = True
            show_result(self.is_dead)
            self.reset()

        if self.moves_without_eating == MAX_MOVES_WITHOUT_EATING:
            print("Snake got stuck, trying again..")
            self.is_dead = True
            show_result(self.is_dead)
            self.reset()

        if self.eating_apple():
            self.add_square()
