import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 640, 440
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128,128,128)
YELLOW = (255, 255, 102)

# Set directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        # Body size, and default random direction when game starts
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head = self.body[0]
        x, y = self.direction
        # Declares new head when moving
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        # If head hits snake body, returns False and ends game
        if new_head in self.body[1:]:
            return False
        # if head hits border, returns False and ends game
        if new_head[0] == 0 or new_head[0] >= (GRID_WIDTH -1) or new_head[1] == 0 or new_head[1] >= (GRID_HEIGHT -1):
            return False
        self.body.insert(0, new_head)
        #Removes tail of snake if the snake doesn't hit a food block
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, direction):
        # Changing direction can't be the opposite direction, if direction is right the following direction != left, has to be up,down, or right
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
            return self.direction

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        # Draws snake body
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)


# Food class
class Food:
    def __init__(self):
        # Spawning of food across screen
        self.position = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))

    def draw(self, surface):
        # Draws food blocks
        pygame.draw.rect(surface, YELLOW, (self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Border: 
     def __init__(self):
         self.startx = 0
         self.starty = 0
    
     def draw(self, surface):
        # Draws border for snake to avoid
         pygame.draw.rect(surface, RED, pygame.Rect(self.startx, self.starty, WIDTH, HEIGHT), 20)

class PlayButton: # Placement and drawing of play button
    def __init__(self):
        self.rect = pygame.Rect(260, 180, 100, 40)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        font = pygame.font.Font(None, 32)
        text = font.render("Play", True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class QuitButton: # PLacement and drawing of quit button
    def __init__(self):
        self.rect = pygame.Rect(260, 230, 100, 40)
    
    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        font = pygame.font.Font(None, 32)
        text = font.render("Quit", True, WHITE)
        text_rect = text.get_rect(center= self.rect.center)
        surface.blit(text, text_rect)


class PlayerScore: # Placement and drawing of player's score
    def __init__(self):
        self.score_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.points = 0

    def add_score(self):
        # Adds 10 points everytime a food block is hit
        self.points += 10   

    def score(self, surface):
        # Displays score throughout game
        value = self.score_font.render("Your Score: " + str(self.points), True, WHITE)
        surface.blit(value, [20,-3])
    
    def end_score(self, surface):
        # Displays final player score after game ends
        value = self.score_font.render("Final Score: " + str(self.points), True, WHITE)
        surface.blit(value, [250, 220])


class HighScore(): #Placement and drawing of high score
    def __init__(self):
        self.score_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.high_score_list = []
        self.read_highscore('highscore.txt')

    def read_highscore(self, filename): 
        # Opens text file, cleans it, adds each line to a list and sorts it from greatest int to lowest
        with open(filename, 'r') as text_file:
            for line in text_file:
                clean_line = line.strip()
                if clean_line:
                    self.high_score_list.append(int(clean_line))
        self.high_score_list.sort(reverse=True)

    def write_highscore(self,filename, score):
        # Writes each player score to text file as string
        with open (filename, 'a') as text_file:
            text_file.write(str(score)+ '\n')

    def display_highscore(self, surface):
        # Draws highest score from the text file list on top right of screen
        if self.high_score_list:
            max_score = self.high_score_list[0]
            value = self.score_font.render("High Score: " + str(max_score), True, WHITE)
            surface.blit(value, [490,-3])

    def update_highscore(self, score):
        # Adds score to highscore list, sorts from greatest to least, and calls write_highscore function)
        self.high_score_list.append(score)
        self.high_score_list.sort(reverse=True)
        self.write_highscore('highscore.txt',score)

# Game function
def game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game - Roger Galan')
    clock = pygame.time.Clock()

    # Declares classes as variables
    snake = Snake()
    food = Food()
    border = Border()
    play_button = PlayButton()
    quit_button = QuitButton()
    player_score = PlayerScore()
    high_score = HighScore()

    running = True
    game_started = False
    game_over = False

    while running:
        # Sets key binds for every button that can be pressed in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_KP_ENTER:
                    game_started = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.rect.collidepoint(event.pos):
                        game_started = True
                        time.sleep(1)
                    elif quit_button.rect.collidepoint(event.pos):
                        pygame.quit()

        
        screen.fill(BLACK)

        if game_started:
            # Snake will move, grow if eats food, spawn another food block, display player score, and display high score
            if snake.move():
                if snake.body[0] == food.position:
                    snake.grow_snake()
                    food = Food()
                    player_score.add_score() #calls add score function
                
                snake.draw(screen)
                food.draw(screen)
                border.draw(screen)
                player_score.score(screen)
                high_score.display_highscore(screen)
                pygame.display.flip()
   
            else:
                # When snake hits itself or border, final score will display for 2 sec and add score to highscore.txt file
                game_over = True
                player_score.end_score(screen)
                high_score.update_highscore(player_score.points)
                pygame.display.update()
                time.sleep(2)
        else:
            # Main menu screen
            play_button.draw(screen)
            quit_button.draw(screen)
            border.draw(screen)
            high_score.display_highscore(screen)
            pygame.display.flip()

        if game_over:
            # Resets the game
            snake = Snake()
            food = Food()
            player_score = PlayerScore()
            border.draw(screen)
            game_started = False
            game_over = False
            play_button.draw(screen)
            quit_button.draw(screen)
            player_score.score(screen)
            pygame.display.flip()        
        

        clock.tick(10)

    pygame.quit()

# Runs the program
if __name__ == "__main__":
    game()