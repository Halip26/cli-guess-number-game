import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize mixer for music
pygame.mixer.init()

# load the music
pygame.mixer.music.load("music/retro-game-music-245230.mp3")
# set the volume to 20%
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # to looping the music

# Screen dimensions and colors
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (4, 204, 17)
RED = (237, 0, 0)
BLUE = (0, 71, 237)
ORANGE = (237, 134, 0)
PALE_BLUE = (173, 216, 230)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Number")

# Fonts
font = pygame.font.Font(None, 36)

# Random number
number = random.randint(1, 99)

# Game variables
input_text = ""
instruction_message = "Guess a number between 1 and 99: "
result_message = ""
result_number = ""
result_color = BLACK
game_over = False


# Main game loop
def main():
    global input_text, result_message, result_color, game_over, number, result_number

    # Initialize attempts
    attempts = 10

    while True:
        screen.fill(PALE_BLUE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        guess = int(input_text)
                        if guess < number:
                            result_message = f"{input_text} number you guessed is low"
                            result_color = ORANGE  # Set color to orange
                        elif guess > number:
                            result_message = f"{input_text} number you guessed is high"
                            result_color = RED  # Set color to red
                        else:
                            result_message = "Congrats, you guessed it!"
                            result_number = f"The correct number was {number}"
                            result_color = GREEN  # Set color to green
                            game_over = True
                        input_text = ""
                    else:
                        result_message = "Please enter a valid number"
                        result_color = BLUE  # Set the color to blue
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 2:
                        input_text += event.unicode

        # Render the instruction message
        instruction_surface = font.render(instruction_message, True, BLACK)
        screen.blit(
            instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, 80)
        )

        # Draw the input box
        pygame.draw.rect(screen, BLACK, (150, 150, 300, 50), 2)

        # Render the input text
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (160, 160))

        # Render the result message (below the input box)
        result_surface = font.render(result_message, True, result_color)
        screen.blit(result_surface, (150, 220))

        # Render the result number message (below the result message)
        correct_number = font.render(result_number, True, result_color)
        screen.blit(correct_number, (150, 245))

        # Update the display
        pygame.display.flip()


# Run the game
main()
