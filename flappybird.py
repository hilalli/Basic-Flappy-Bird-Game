import tkinter as tk
import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 50
PIPE_GAP = 150
SKY_COLOR = "#87CEEB"  # Light blue color for sky
CLOUD_COLOR = "#FFFFFF"  # White color for clouds
SUN_COLOR = "#FFD700"  # Gold color for sun


class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird Game")

        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # Initialize tkinter
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()

        # Game variables
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_dy = 0
        self.pipes = []
        self.score = 0
        self.game_over = False

        # Create restart and exit buttons
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)

        # Bind spacebar for jumping
        self.root.bind('<space>', self.jump)

        # Draw initial game screen
        self.draw_background()
        self.draw_bird()
        self.draw_pipes()
        self.score_text = self.canvas.create_text(50, 50, text=f"Score: {self.score}", anchor=tk.NW, font=("Arial", 14))

        # Start game loop
        self.game_loop()

    def game_loop(self):
        while not self.game_over:
            self.canvas.delete("pipes")

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            # Update bird position
            self.bird_dy += 1
            self.bird_y += self.bird_dy

            # Check for collisions or out of bounds
            if self.bird_y < 0 or self.bird_y + BIRD_HEIGHT > SCREEN_HEIGHT:
                self.game_over = True
            elif self.check_collision():
                self.game_over = True

            # Update pipes and check collisions
            self.update_pipes()

            # Check for scoring
            self.check_scoring()

            # Check for winning condition
            if self.score >= 10:
                self.game_over = True
                self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, text="Congratulations you win the game :)",
                                        font=("Arial", 24), fill="black")

            # Redraw bird and score
            self.canvas.delete("bird")
            self.draw_bird()
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

            # Update tkinter canvas
            self.canvas.update()

            # Limit frame rate
            self.clock.tick(30)

        if not self.score >= 100:
            # Game over logic
            self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, text=f"Final Score: {self.score}",
                                    font=("Arial", 24), fill="black")

        # Show restart and exit buttons
        self.restart_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.exit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def restart_game(self):
        # Hide buttons
        self.restart_button.place_forget()
        self.exit_button.place_forget()

        # Reset game variables and canvas
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_dy = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.canvas.delete("all")
        self.draw_background()
        self.draw_bird()
        self.draw_pipes()
        self.score_text = self.canvas.create_text(50, 50, text=f"Score: {self.score}", anchor=tk.NW, font=("Arial", 14))

        # Start game loop again
        self.game_loop()

    def jump(self, event):
        self.bird_dy = -100

    def draw_background(self):
        # Draw sky background
        self.canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill=SKY_COLOR, outline="")

        # Draw sun
        sun_x = 50
        sun_y = 50
        sun_radius = 30
        self.canvas.create_oval(sun_x - sun_radius, sun_y - sun_radius, sun_x + sun_radius, sun_y + sun_radius,
                                fill=SUN_COLOR, outline="")

        # Draw clouds
        self.draw_cloud(100, 100, 60, 30)
        self.draw_cloud(250, 150, 80, 40)
        self.draw_cloud(300, 70, 50, 25)

    def draw_cloud(self, x, y, width, height):
        # Draw cloud as a series of overlapping ovals
        self.canvas.create_oval(x, y, x + width, y + height, fill=CLOUD_COLOR, outline="")
        self.canvas.create_oval(x - width // 2, y + height // 4, x + width // 2, y + height * 3 // 4, fill=CLOUD_COLOR,
                                outline="")
        self.canvas.create_oval(x + width // 2, y + height // 4, x + width * 3 // 2, y + height * 3 // 4,
                                fill=CLOUD_COLOR, outline="")

    def draw_bird(self):
        # Draw bird as a yellow oval with a beak
        bird_x = 50
        bird_y = self.bird_y
        self.canvas.create_oval(bird_x, bird_y, bird_x + BIRD_WIDTH, bird_y + BIRD_HEIGHT, fill="yellow", outline="",
                                tag="bird")
        self.canvas.create_polygon(bird_x + BIRD_WIDTH, bird_y + BIRD_HEIGHT // 2, bird_x + BIRD_WIDTH + 10,
                                   bird_y + BIRD_HEIGHT // 2 - 5, bird_x + BIRD_WIDTH + 10,
                                   bird_y + BIRD_HEIGHT // 2 + 5, fill="orange", outline="", tag="bird")

    def draw_pipes(self):
        # Draw initial pipes
        for pipe in self.pipes:
            self.canvas.create_rectangle(pipe['x'], 0, pipe['x'] + PIPE_WIDTH, pipe['y'], fill="green", tag="pipes")
            self.canvas.create_rectangle(pipe['x'], pipe['y'] + PIPE_GAP, pipe['x'] + PIPE_WIDTH, SCREEN_HEIGHT,
                                         fill="green", tag="pipes")

    def update_pipes(self):
        # Update existing pipes
        for pipe in self.pipes:
            pipe['x'] -= 5
            self.canvas.create_rectangle(pipe['x'], 0, pipe['x'] + PIPE_WIDTH, pipe['y'], fill="green", tag="pipes")
            self.canvas.create_rectangle(pipe['x'], pipe['y'] + PIPE_GAP, pipe['x'] + PIPE_WIDTH, SCREEN_HEIGHT,
                                         fill="green", tag="pipes")

        # Generate new pipes
        if len(self.pipes) == 0 or self.pipes[-1]['x'] < SCREEN_WIDTH - 200:
            pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
            self.pipes.append({'x': SCREEN_WIDTH, 'y': pipe_height})

    def check_collision(self):
        # Check for collision with pipes
        bird_x1, bird_y1 = 50, self.bird_y
        bird_x2, bird_y2 = bird_x1 + BIRD_WIDTH, bird_y1 + BIRD_HEIGHT

        for pipe in self.pipes:
            pipe_x1, pipe_y1 = pipe['x'], 0
            pipe_x2, pipe_y2 = pipe['x'] + PIPE_WIDTH, pipe['y']
            pipe2_x1, pipe2_y1 = pipe['x'], pipe['y'] + PIPE_GAP
            pipe2_x2, pipe2_y2 = pipe['x'] + PIPE_WIDTH, SCREEN_HEIGHT

            if (bird_x2 > pipe_x1 and bird_x1 < pipe_x2 and bird_y2 > pipe_y1 and bird_y1 < pipe_y2) or \
                    (bird_x2 > pipe2_x1 and bird_x1 < pipe2_x2 and bird_y2 > pipe2_y1 and bird_y1 < pipe2_y2):
                return True

        return False

    def check_scoring(self):
        # Check for scoring by passing pipes
        bird_mid_x = 50 + BIRD_WIDTH // 2

        for pipe in self.pipes:
            pipe_mid_x = pipe['x'] + PIPE_WIDTH // 2

            if pipe_mid_x == bird_mid_x:
                self.score += 1


# Main tkinter window
root = tk.Tk()
game = FlappyBirdGame(root)
root.mainloop()
