from tkinter import *
import random
import pygame
from PIL import Image, ImageTk

# Initialize pygame mixer
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("game_point.mp3")  
game_over_sound = pygame.mixer.Sound("game_over.mp3")  


GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25  
BODY_PARTS = 1
SNAKE_COLOUR = "#90EE90"
FOOD_COLOUR = "yellow"
BACKGROUND_COLOR = "black"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([GAME_HEIGHT / 2, GAME_WIDTH / 2])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="Snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")

def next_turn(snake, food):
    global direction
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        eat_sound.play()  # Play eat sound
        canvas.delete("food")
        food.spawn_food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collision(snake):
        game_over()
    else:        
        root.after(SPEED, next_turn, snake, food)  


def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction   
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction                       

def check_collision(snake):
    x,y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        print("!!Game Over!!")
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("!!Game Over!!")
            return True
    return False    

def restart_game():
    global score, direction
    score = 0
    direction = ""
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food(canvas)
    next_turn(snake, food)

def game_over():
    game_over_sound.play()  # Play game over sound
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consola",70), text="GAME OVER", fill="yellow", tag="game")
    for widget in root.winfo_children():
        if isinstance(widget, Button) and widget["text"] == "Restart":
            widget.destroy()
    restart_button = Button(root, text="Restart", command=restart_game, font=("arial",40), foreground="cyan", bg=BACKGROUND_COLOR)
    restart_button.grid(row=0,column=1,sticky="e",padx=10,pady=10)        

root = Tk()
root.title("Snake Game")
root.resizable(True, True)
root.configure(bg=BACKGROUND_COLOR) 
score = 0
direction = ""

label = Label(root, text="Score:{}".format(score), font=("arial", 40),foreground="cyan", bg=BACKGROUND_COLOR)  # Set background color of the label
label.grid(row=0, column=0, sticky="w", padx=10, pady=10)


canvas = Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.grid(row=1, column=0, columnspan=2,sticky="ew")

root.update()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (root_width / 2))
y = int((screen_height / 2) - (root_height / 2))

root.geometry(f"{root_width}x{root_height}+{x}+{y}")

root.bind("<Left>", lambda event: change_direction('left'))
root.bind("<Right>", lambda event: change_direction('right'))
root.bind("<Up>", lambda event: change_direction('up'))
root.bind("<Down>", lambda event: change_direction('down'))  
snake = Snake()
food = Food(canvas)
next_turn(snake, food)

root.mainloop()
