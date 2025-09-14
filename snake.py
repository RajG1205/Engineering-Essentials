import pygame
import random
import sys

# --- Configuration ---
CELL = 20                # Size of each cell (pixels)
COLS, ROWS = 30, 20      # Grid size
WIDTH, HEIGHT = CELL * COLS, CELL * ROWS

# Colors (R, G, B)
SNAKE_COLOR = (17, 168, 79)
FOOD_COLOR = (219, 50, 54)
BG_COLOR = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (240, 240, 240)

# Directions
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)


# --- Snake Class ---
class Snake:
    def __init__(self):
        x, y = COLS // 2, ROWS // 2
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.dir = RIGHT
        self.grow = False

    def head(self):
        return self.body[0]

    def move(self):
        hx, hy = self.head()
        dx, dy = self.dir
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_dir(self, new_dir):
        opposite = (-self.dir[0], -self.dir[1])
        if new_dir != opposite:
            self.dir = new_dir


# --- Food Class ---
class Food:
    def __init__(self, snake_body):
        self.position = self.random_pos(snake_body)

    def random_pos(self, snake_body):
        choices = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake_body]
        return random.choice(choices) if choices else None

    def respawn(self, snake_body):
        self.position = self.random_pos(snake_body)


# --- Drawing Functions ---
def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))


def draw_block(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
    pygame.draw.rect(surface, color, rect)


def draw_text_center(surface, text, size, y_offset=0, bold=True):
    font = pygame.font.SysFont("consolas", size, bold=bold)
    text_surf = font.render(text, True, TEXT_COLOR)
    rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    surface.blit(text_surf, rect)


# --- Main Game ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Snake Game - Levels")
    clock = pygame.time.Clock()
    font_small = pygame.font.SysFont("consolas", 20)

    # --- Level Selection ---
    level, FPS = None, 10
    while level is None:
        screen.fill(BG_COLOR)
        draw_text_center(screen, "Snake Game", 50, -100)
        draw_text_center(screen, "Select Level", 36, -40)
        draw_text_center(screen, "1. Easy   2. Medium   3. Hard", 28, 20)
        draw_text_center(screen, "Press 1 / 2 / 3", 22, 70, bold=False)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level, FPS = 1, 8
                elif event.key == pygame.K_2:
                    level, FPS = 2, 12
                elif event.key == pygame.K_3:
                    level, FPS = 3, 18

    # --- Initialize Game ---
    snake = Snake()
    food = Food(snake.body)
    score, high_score, game_over = 0, 0, False
    running = True

    # --- Game Loop ---
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    snake.change_dir(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.change_dir(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.change_dir(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.change_dir(RIGHT)
                elif event.key == pygame.K_r and game_over:
                    # Restart
                    snake = Snake()
                    food = Food(snake.body)
                    score, game_over = 0, False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            snake.move()
            hx, hy = snake.head()

            # --- Rule 1: Collision with walls ---
            if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:
                game_over = True

            # --- Rule 2: Collision with self ---
            elif snake.head() in snake.body[1:]:
                game_over = True

            # --- Rule 3: Food Eaten ---
            if food.position and snake.head() == food.position:
                snake.grow = True
                score += 1
                if score > high_score:
                    high_score = score
                food.respawn(snake.body)

        # --- Draw everything ---
        screen.fill(BG_COLOR)
        draw_grid(screen)

        # Food as square
        if food.position:
            draw_block(screen, food.position, FOOD_COLOR)

        # Snake as square
        for segment in snake.body:
            draw_block(screen, segment, SNAKE_COLOR)

        # Score & High Score Display
        score_surf = font_small.render(f"Score: {score}", True, TEXT_COLOR)
        high_score_surf = font_small.render(f"High Score: {high_score}", True, TEXT_COLOR)
        screen.blit(score_surf, (8, 8))
        screen.blit(high_score_surf, (8, 30))

        # Game Over Screen
        if game_over:
            draw_text_center(screen, "GAME OVER", 48, -20)
            draw_text_center(screen, "Press R to Restart or Esc to Quit", 22, 30, bold=False)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# --- Run the Game ---
if __name__ == "__main__":

    main()

