Here is the initial python code for the base: 
game.py
import random
from settings import GRID_WIDTH, GRID_HEIGHT


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)  # Initial direction (moving upward)

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        # Add a new segment to the snake at the tail position
        self.body.append(self.body[-1])

    def set_direction(self, direction):
        # Prevent the snake from reversing
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def check_collision(self):
        # Check if the snake's head collides with its body
        head = self.body[0]
        return head in self.body[1:]

    def check_wall_collision(self, walls):
        head_x, head_y = self.body[0]
        # Check collision with border walls or grid boundaries
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        # Check collision with internal walls
        return (head_x, head_y) in walls.positions


class Fruit:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def new_position(self, snake_body, wall_positions):
        # Ensure fruit doesn't spawn on the snake or walls
        while True:
            self.position = self.random_position()
            if self.position not in snake_body and self.position not in wall_positions:
                break


class Wall:
    def __init__(self):
        self.positions = []

    def add_wall(self, snake_body, fruit_position):

        def is_adjacent_or_diagonal(pos, walls):
            # Check if the position is adjacent or diagonal to any existing wall
            x, y = pos
            neighbors = [
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
            ]
            return any(neighbor in walls for neighbor in neighbors)

        # Collect all potential positions on the grid
        potential_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake_body
               and (x, y) != fruit_position
               and (x, y) not in self.positions
               and not is_adjacent_or_diagonal((x, y), self.positions)
        ]

        # Check if there are any valid positions left
        if potential_positions:
            new_wall = random.choice(potential_positions)  # Choose a random valid position
            self.positions.append(new_wall)
        else:
            print("No space available to add a new wall.")

main.py
from random import choice
import pygame
import sys
from game import Snake, Fruit, Wall
from render import initialize_screen, draw_elements
from qlearning import train_qlearning, get_state, take_action, load_q_table
from bfs import *
from gbfs import *
from utils import *

def main_menu(screen, score=None):
    # Use a readable font size
    font = pygame.font.Font(None, 30)

    # Define each line of text separately
    line1 = "Press 1 for User Mode"
    line2 = "Press 2 for BFS AI"
    line3 = "Press 3 for Monte Carlo AI"
    line4 = "Press 4 for Q-Learning AI"
    line5 = "Press 5 for GBFS AI"
    score_text = f"Last Score: {score}" if score is not None else ""  # Display score if available

    # Render each line of text
    text1 = font.render(line1, True, (255, 255, 255))
    text2 = font.render(line2, True, (255, 255, 255))
    text3 = font.render(line3, True, (255, 255, 255))
    text4 = font.render(line4, True, (255, 255, 255))
    text5 = font.render(line5, True, (255, 255, 255))
    score_display = font.render(score_text, True, (255, 255, 255))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Display each line at a specified position, with spacing between lines
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    screen.blit(text3, (10, 70))
    screen.blit(text4, (10, 100))
    screen.blit(text5, (10, 130))
    screen.blit(score_display, (10, 160))  # Display score below menu options

    # Update the display to show the text
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "USER"
                elif event.key == pygame.K_2:
                    return "BFS"
                elif event.key == pygame.K_3:
                    return "MONTE_CARLO"
                elif event.key == pygame.K_4:
                    return "Q_LEARNING"
                elif event.key == pygame.K_5:
                    return "GBFS"


def game_loop(mode, Q_table=None):
    screen = initialize_screen()
    clock = pygame.time.Clock()

    snake = Snake()
    fruit = Fruit()
    walls = Wall()
    score = 0  # Initialize score counter
    walls_count = 0  # Initialize wall counter

    # Add border walls to the walls object
    for x in range(GRID_WIDTH):
        walls.positions.append((x, 0))  # Top border
        walls.positions.append((x, GRID_HEIGHT - 1))  # Bottom border
    for y in range(GRID_HEIGHT):
        walls.positions.append((0, y))  # Left border
        walls.positions.append((GRID_WIDTH - 1, y))  # Right border

    fruit.new_position(snake.body, walls.positions)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif mode == "USER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))

        # Snake movement and logic based on the mode
        if mode == "USER":
            snake.move()
        elif mode == "Q_LEARNING":
            state = get_state(snake, fruit, walls)
            if state not in Q_table:
                print(f"State {state} not found in Q-table. Taking random action.")
                action = choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            else:
                action = max(Q_table[state], key=Q_table[state].get)
                print("action found in q table")
            take_action(action, snake)  # Execute the chosen action
        elif mode == "BFS":
            bfs_path = [] if 'bfs_path' not in locals() else bfs_path
            if not bfs_path:
                bfs_path = bfs(snake, fruit, walls)

            if bfs_path:
                action = bfs_path.pop(0)
                take_action(action, snake)
        elif mode == "GBFS":
            gbfs_path = [] if 'gbfs_path' not in locals() else gbfs_path
            if not gbfs_path:
                gbfs_path = gbfs(snake, fruit, walls)

            if gbfs_path:
                action = gbfs_path.pop(0)
                take_action(action, snake)

        # Check for collisions with walls or boundaries
        if snake.check_collision() or snake.check_wall_collision(walls):
            return score  # Return the score to main menu on game over

        # Check if the snake eats the fruit
        if snake.body[0] == fruit.position:
            gbfs_path = []
            bfs_path = []
            snake.grow()
            score += 10
            walls.add_wall(snake.body, fruit.position)
            walls_count += 1
            fruit.new_position(snake.body, walls.positions)

        # Draw all elements, including score and wall count
        draw_elements(screen, snake, fruit, walls, score, walls_count)

        # Control the game speed
        clock.tick(FPS)


if __name__ == "__main__":
    screen = initialize_screen()

    # Load an existing Q-table or train a new one
    Q_table = load_q_table("q_table.pkl")
    # if not Q_table:
    #     Q_table = train_qlearning()

    score = None

    while True:
        mode = main_menu(screen, score)
        score = game_loop(mode, Q_table if mode == "Q_LEARNING" else None)

render.py
import pygame
from settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT, BLACK, GREEN, RED, BLUE, \
    SCALE_FACTOR


def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game with AI")
    return screen


def draw_elements(screen, snake, fruit, walls, score, walls_count):
    screen.fill(BLACK)  # Clear the screen

    # Draw border walls around the grid
    for x in range(GRID_WIDTH + 2):  # Include one cell on each side
        pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE * SCALE_FACTOR, 0, GRID_SIZE * SCALE_FACTOR,
                                                   GRID_SIZE * SCALE_FACTOR))
        pygame.draw.rect(screen, BLUE,
                         pygame.Rect(x * GRID_SIZE * SCALE_FACTOR, (GRID_HEIGHT + 1) * GRID_SIZE * SCALE_FACTOR,
                                     GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))
    for y in range(GRID_HEIGHT + 2):  # Include one cell on top and bottom
        pygame.draw.rect(screen, BLUE, pygame.Rect(0, y * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR,
                                                   GRID_SIZE * SCALE_FACTOR))
        pygame.draw.rect(screen, BLUE,
                         pygame.Rect((GRID_WIDTH + 1) * GRID_SIZE * SCALE_FACTOR, y * GRID_SIZE * SCALE_FACTOR,
                                     GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Draw the snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(segment[0] * GRID_SIZE * SCALE_FACTOR, segment[1] * GRID_SIZE * SCALE_FACTOR,
                                     GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Draw the fruit
    pygame.draw.rect(screen, RED, pygame.Rect(fruit.position[0] * GRID_SIZE * SCALE_FACTOR,
                                              fruit.position[1] * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR,
                                              GRID_SIZE * SCALE_FACTOR))

    # Draw the walls
    for wall in walls.positions:
        pygame.draw.rect(screen, BLUE,
                         pygame.Rect(wall[0] * GRID_SIZE * SCALE_FACTOR, wall[1] * GRID_SIZE * SCALE_FACTOR,
                                     GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Display score and wall count
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    walls_text = font.render(f"Walls: {walls_count}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Display score in top left corner
    screen.blit(walls_text, (10, 50))  # Display wall count below the score

    pygame.display.flip()  # Update the display

settings.py
# Grid settings
GRID_SIZE = 20        # Size of each grid square in pixels
GRID_WIDTH = 20       # Number of columns in the grid
GRID_HEIGHT = 20      # Number of rows in the grid

# Scaling factor to make the window larger
SCALE_FACTOR = 2

# Scaled screen dimensions
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE * SCALE_FACTOR
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE * SCALE_FACTOR

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)    # Snake color
RED = (255, 0, 0)      # Fruit color
BLUE = (0, 0, 255)     # Wall color

# Game settings
FPS = 15               # Frames per second (game speed)

utils.py
from settings import GRID_WIDTH, GRID_HEIGHT, FPS

# Reward values
REWARD_FRUIT = 100
REWARD_COLLISION = -1000
REWARD_STEP = -1

def is_safe(x, y, walls, snake_body):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and (x, y) not in walls.positions and (x, y) not in snake_body

def calculate_reward(snake, fruit, walls):
    if snake.check_wall_collision(walls) or snake.check_collision():
        return REWARD_COLLISION
    elif snake.body[0] == fruit.position:
        return REWARD_FRUIT
    else:
        return REWARD_STEP

def take_action(action, snake):
    if action == 'UP':
        snake.set_direction((0, -1))
    elif action == 'DOWN':
        snake.set_direction((0, 1))
    elif action == 'LEFT':
        snake.set_direction((-1, 0))
    elif action == 'RIGHT':
        snake.set_direction((1, 0))
    snake.move()

and here is my java code for A-sta search: 
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class SnakeGameGUI extends JPanel implements ActionListener {
    private final int TILE_SIZE = 30;
    private final int ROWS = 20;
    private final int COLS = 20;
    private final int TARGET_SCORE = 1000;

    private boolean[][] walls;
    private java.util.Set<Point> snakeBody;
    private Point snakeHead;
    private Point apple;
    private int score;
    private javax.swing.Timer timer;

    public SnakeGameGUI() {
        setPreferredSize(new Dimension(COLS * TILE_SIZE, ROWS * TILE_SIZE));
        setBackground(Color.BLACK);
        setFocusable(true);
        initializeGame();
    }

    private void initializeGame() {
        walls = new boolean[ROWS][COLS];
        snakeBody = new LinkedHashSet<>();
        snakeHead = new Point(ROWS / 2, COLS / 2);
        snakeBody.add(snakeHead);
        score = 0;

        placeApple();
        timer = new javax.swing.Timer(50, this);
        timer.start();
    }

    private void placeApple() {
        Random rand = new Random();
        do {
            apple = new Point(rand.nextInt(ROWS), rand.nextInt(COLS));
        } while (snakeBody.contains(apple) || walls[apple.x][apple.y] || !isReachable(apple));
        placeRandomWall();
    }

    private void placeRandomWall() {
        Random rand = new Random();
        Point wall;
        do {
            wall = new Point(rand.nextInt(ROWS), rand.nextInt(COLS));
        } while (snakeBody.contains(wall) || walls[wall.x][wall.y] || wall.equals(apple));
        walls[wall.x][wall.y] = true;
    }

    private boolean isReachable(Point target) {
        return AStarPathfinding(snakeHead, target) != null;
    }

    private java.util.List<Point> AStarPathfinding(Point start, Point goal) {
        PriorityQueue<Node> openList = new PriorityQueue<>(Comparator.comparingInt(n -> n.f));
        java.util.Map<Point, Node> allNodes = new HashMap<>();

        Node startNode = new Node(start, null, 0, manhattanDistance(start, goal));
        openList.add(startNode);
        allNodes.put(start, startNode);

        while (!openList.isEmpty()) {
            Node current = openList.poll();

            if (current.point.equals(goal)) {
                return reconstructPath(current);
            }

            for (Point neighbor : getNeighbors(current.point)) {
                int tentativeG = current.g + 1;
                Node neighborNode = allNodes.getOrDefault(neighbor, new Node(neighbor, null, Integer.MAX_VALUE, manhattanDistance(neighbor, goal)));

                if (tentativeG < neighborNode.g) {
                    neighborNode.g = tentativeG;
                    neighborNode.f = tentativeG + neighborNode.h;
                    neighborNode.parent = current;
                    allNodes.put(neighbor, neighborNode);

                    if (!openList.contains(neighborNode)) {
                        openList.add(neighborNode);
                    }
                }
            }
        }
        return null; // No path found
    }

    private java.util.List<Point> reconstructPath(Node node) {
        java.util.List<Point> path = new ArrayList<>();
        while (node != null) {
            path.add(0, node.point);
            node = node.parent;
        }
        return path;
    }

    private int manhattanDistance(Point a, Point b) {
        return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
    }

    private java.util.List<Point> getNeighbors(Point p) {
        java.util.List<Point> neighbors = new ArrayList<>();
        int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        for (int[] dir : directions) {
            int newX = p.x + dir[0];
            int newY = p.y + dir[1];
            Point neighbor = new Point(newX, newY);

            if (newX >= 0 && newY >= 0 && newX < ROWS && newY < COLS &&
                !walls[newX][newY] && !snakeBody.contains(neighbor)) {
                neighbors.add(neighbor);
            }
        }
        return neighbors;
    }

    private void moveSnake() {
        java.util.List<Point> path = AStarPathfinding(snakeHead, apple);

        if (path == null || path.size() < 2) {
            timer.stop();
            JOptionPane.showMessageDialog(this, "Game Over! No valid path to the apple.");
            System.exit(0);
        }

        Point nextHead = path.get(1);

        if (isCollision(nextHead)) {
            timer.stop();
            JOptionPane.showMessageDialog(this, "Game Over! Final Score: " + score);
            System.exit(0);
        }

        snakeBody.add(nextHead);
        snakeHead = nextHead;

        if (snakeHead.equals(apple)) {
            score += 10;
            if (score >= TARGET_SCORE) {
                timer.stop();
                JOptionPane.showMessageDialog(this, "You Win! Final Score: " + score);
                System.exit(0);
            }
            placeApple();
        } else {
            snakeBody.remove(snakeBody.iterator().next());
        }
    }

    private boolean isCollision(Point point) {
        return point.x < 0 || point.y < 0 || point.x >= ROWS || point.y >= COLS ||
               walls[point.x][point.y] || snakeBody.contains(point);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        moveSnake();
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                g.setColor(Color.GRAY);
                g.drawRect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            }
        }

        g.setColor(Color.DARK_GRAY);
        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                if (walls[row][col]) {
                    g.fillRect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE);
                }
            }
        }

        g.setColor(Color.RED);
        g.fillOval(apple.y * TILE_SIZE, apple.x * TILE_SIZE, TILE_SIZE, TILE_SIZE);

        g.setColor(Color.GREEN);
        for (Point p : snakeBody) {
            g.fillRect(p.y * TILE_SIZE, p.x * TILE_SIZE, TILE_SIZE, TILE_SIZE);
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Snake Game with A*");
        SnakeGameGUI game = new SnakeGameGUI();

        frame.add(game);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }

    private static class Node {
        Point point;
        Node parent;
        int g;
        int h;
        int f;

        Node(Point point, Node parent, int g, int h) {
            this.point = point;
            this.parent = parent;
            this.g = g;
            this.h = h;
            this.f = g + h;
        }
    }
}

transate my java code into python, keep it in astar.py and integrate it with the base python code given above, so that everything works fine. Igonore the gui of my java code instead integrate the A-star search part with the GUI and other settings of the python codes given above.

