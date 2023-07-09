import math
import time
import numpy as np
from src.algs import draw_text
import src.data.state as state
from copy import deepcopy
from random import randrange
from collections import deque
from threading import Thread


BIN = 2
assert not BIN % 2, "Bin must be an even number"

MAX_FPS = 30


GAME_HEIGHT = math.floor(state.HEIGHT / BIN)
GAME_WIDTH = math.floor(state.WIDTH / BIN)

# Colors
SURFACE_CLR = (0, 0, 0)

APPLE_CLR = (220, 50, 50)

SNAKE_CLR = (50, 220, 50)

HEAD_CLR = (90, 190, 150)

# Game Settings
INITIAL_SNAKE_LENGTH = 3
WAIT_SECONDS_AFTER_WIN = (
    15  # If snake wins the game, wait for this amount of seconds before restarting
)
MAX_MOVES_WITHOUT_EATING = (
    GAME_HEIGHT * GAME_WIDTH * 2
)  # Snake will die after this amount of moves without eating apple
SNAKE_MAX_LENGTH = (
    GAME_HEIGHT * GAME_WIDTH - INITIAL_SNAKE_LENGTH
)  # Max number of apples snake can eat

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
    def __init__(self):
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

        self.path = []
        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

        self.display_queue = deque()

        self.time_between_frames = 1 / MAX_FPS
        self.last_update = time.time()

    def draw(self):
        pixels = np.zeros((state.HEIGHT, state.WIDTH, 3), dtype=np.int)

        # draw apple
        apple_x, apple_y = self.apple.pos[1], self.apple.pos[0]
        pixels[apple_x][apple_y] = APPLE_CLR

        # draw snake
        for count, sqr in enumerate(self.squares):
            if count == 0:
                color = HEAD_CLR
            else:
                color = SNAKE_CLR
            pixels[sqr.pos[1], sqr.pos[0]] = color

        def unbin(pixels):
            top_left_quarter = pixels[:GAME_HEIGHT, :GAME_WIDTH]
            # Get the top left quarter (16x16)
            top_left_quarter = pixels[:GAME_HEIGHT, :GAME_WIDTH]

            # Repeat each pixel value in x and y direction to form 2x2 pixel groups
            upscaled = np.repeat(np.repeat(top_left_quarter, BIN, axis=0), BIN, axis=1)

            return upscaled

        pixels = unbin(pixels)
        self.display_queue.appendleft(pixels)

        while len(self.display_queue) > 10000:
            time.sleep(1)

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
        tail = self.squares[-1]  # Tail before adding new square

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
        self.squares[-1].is_tail = True  # Tail after adding new square

    def reset(self):
        self.__init__()

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

    def go_to(self, position):  # Set head direction to target position
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
    def bfs(self, s, e):  # Find shortest path between (start_position, end_position)
        q = [s]  # Queue
        visited = {tuple(pos): False for pos in GRID}

        visited[s] = True

        # Prev is used to find the parent node of each node to create a feasible path
        prev = {tuple(pos): None for pos in GRID}

        while q:  # While queue is not empty
            node = q.pop(0)
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = e  # Starting from end node, we will find the parent node of each node

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == s:
                path.append(e)
                return path
            path.insert(0, p_node)

        return []  # Path not available

    def create_virtual_snake(
        self,
    ):  # Creates a copy of snake (same size, same position, etc..)
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
        # If there is only 1 apple left for snake to win and it's adjacent to head
        if self.score == SNAKE_MAX_LENGTH - 1 and self.apple.pos in get_neighbors(
            self.head.pos
        ):
            winning_path = [tuple(self.apple.pos)]
            print("Snake is about to win..")
            return winning_path

        v_snake = self.create_virtual_snake()

        # Let the virtual snake check if path to apple is available
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))

        # This will be the path to virtual snake tail after it follows path_1
        path_2 = []

        if path_1:
            for pos in path_1:
                v_snake.go_to(pos)
                v_snake.move()

            v_snake.add_square()  # Because it will eat an apple
            path_2 = v_snake.get_path_to_tail()

        if path_2:  # If there is a path between v_snake and it's tail
            return path_1  # Choose BFS path to apple (Fastest and shortest path)

        # If path_1 or path_2 not available, test these 3 conditions:
        # 1- Make sure that the longest path to tail is available
        # 2- If score is even, choose longest_path_to_tail() to follow the tail, if odd use any_safe_move()
        # 3- Change the follow tail method if the snake gets stuck in a loop
        if (
            self.longest_path_to_tail()
            and self.score % 2 == 0
            and self.moves_without_eating < MAX_MOVES_WITHOUT_EATING / 2
        ):
            # Choose longest path to tail
            return self.longest_path_to_tail()

        # Play any possible safe move and make sure path to tail is available
        if self.any_safe_move():
            return self.any_safe_move()

        # If path to tail is available
        if self.get_path_to_tail():
            # Choose shortest path to tail
            return self.get_path_to_tail()

        # Snake couldn't find a path and will probably die
        print("No available path, snake in danger!")

    def update(self):
        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])

        self.draw()
        self.move()

        def show_result(is_dead: bool):
            if is_dead:
                lines = ["The  Snake  is", "Dead", "", f"{self.total_moves}  Moves"]
                color = APPLE_CLR
            else:
                color = SNAKE_CLR
                lines = [
                    "The  Snake  is",
                    "Victorious",
                    "",
                    f"{self.total_moves}  Moves",
                ]

            color_pixels = np.full((state.HEIGHT, state.WIDTH, 3), color, dtype=np.int)

            empty_pixels = np.zeros((state.HEIGHT, state.WIDTH, 3), dtype=np.int)

            for _ in range(5):
                self.display_queue.appendleft(color_pixels)
                self.display_queue.appendleft(empty_pixels)

            pixels = draw_text(empty_pixels, lines)
            self.display_queue.appendleft(pixels)

        if (
            self.score == GAME_WIDTH * GAME_HEIGHT - INITIAL_SNAKE_LENGTH
        ):  # If snake wins the game
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


def snake_loop():
    while True:
        state.snake.update()


def snake():
    if state.snake is None:
        state.snake = Snake()

        snake_thread = Thread(target=snake_loop)
        snake_thread.start()

    if (
        time.time() - state.snake.last_update > state.snake.time_between_frames
        and state.snake.display_queue
    ):
        state.display.display_matrix(pixels=state.snake.display_queue.pop())
        state.snake.last_update = time.time()
    else:
        time.sleep(0.01)
    
    print(f"available frames: {len(state.snake.display_queue)}")
