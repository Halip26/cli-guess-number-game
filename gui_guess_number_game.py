import pygame
import random
import sys
import os

# -----------------------
# Config
# -----------------------
MIN_VAL = 1
MAX_VAL = 100
WIDTH, HEIGHT = 360, 640  # gunakan ukuran portrait mirip Tkinter
FPS = 30

# Colors (converted from your Tkinter hex)
BG_COLOR = (247, 249, 252)  # #f7f9fc
CARD_COLOR = (255, 255, 255)  # white
ACCENT = (75, 123, 236)  # #4b7bec
MUTED = (107, 114, 128)  # #6b7280
TEXT = (17, 24, 39)  # #111827
ORANGE = (237, 134, 0)
GREEN = (4, 204, 17)
RED = (237, 0, 0)
BLUE = (0, 71, 237)
BLACK = (0, 0, 0)
PALE_BLUE = (173, 216, 230)

# Fonts sizes (will use SysFont fallback)
TITLE_SIZE = 22
SUBTITLE_SIZE = 14
DESC_SIZE = 12
INPUT_SIZE = 20
RESULT_SIZE = 16
ATTEMPTS_SIZE = 12
FOOTER_SIZE = 10

# -----------------------
# Initialize Pygame
# -----------------------
pygame.init()
try:
    pygame.mixer.init()
    # optional music file; if not present, ignore
    music_path = "music/retro-game-music-245230.mp3"
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
except Exception:
    # ignore audio errors
    pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Number Game by Mr. Halip")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Segoe UI", TITLE_SIZE, bold=True)
subtitle_font = pygame.font.SysFont("Segoe UI", SUBTITLE_SIZE)
desc_font = pygame.font.SysFont("Segoe UI", DESC_SIZE)
input_font = pygame.font.SysFont("Segoe UI", INPUT_SIZE)
result_font = pygame.font.SysFont("Segoe UI", RESULT_SIZE)
attempts_font = pygame.font.SysFont("Segoe UI", ATTEMPTS_SIZE, italic=True)
footer_font = pygame.font.SysFont("Segoe UI", FOOTER_SIZE)


# -----------------------
# Game state & helpers
# -----------------------
def new_game():
    global secret, attempts, input_text, result_message, result_color, game_over
    secret = random.randint(MIN_VAL, MAX_VAL)
    attempts = 0
    input_text = ""
    result_message = "Make your first guess!"
    result_color = TEXT
    game_over = False
    # debug: print("Secret:", secret)


def reset_game_full():
    new_game()
    # reset attempts left display uses attempts_left variable
    global attempts_left
    attempts_left = 10  # default attempts allowed


# initial state
new_game()
attempts_left = 10

# UI geometry (relative to WIDTH/HEIGHT)
pad_x = int(WIDTH * 0.05)
card_w = WIDTH - pad_x * 2
top_card_h = int(HEIGHT * 0.22)
mid_card_h = int(HEIGHT * 0.28)
bottom_card_h = int(HEIGHT * 0.32)

top_card_rect = pygame.Rect(pad_x, int(HEIGHT * 0.04), card_w, top_card_h)
mid_card_rect = pygame.Rect(pad_x, int(HEIGHT * 0.30), card_w, mid_card_h)
bottom_card_rect = pygame.Rect(pad_x, int(HEIGHT * 0.62), card_w, bottom_card_h)

# Input box inside mid card
input_box_rect = pygame.Rect(
    mid_card_rect.x + 16, mid_card_rect.y + 40, mid_card_rect.width - 32, 48
)

# Buttons (drawn as rectangles)
btn_w = 120
btn_h = 36
btn_gap = 12
guess_btn_rect = pygame.Rect(
    mid_card_rect.centerx - btn_w - btn_gap // 2,
    mid_card_rect.y + mid_card_rect.height - 60,
    btn_w,
    btn_h,
)
reset_btn_rect = pygame.Rect(
    mid_card_rect.centerx + btn_gap // 2,
    mid_card_rect.y + mid_card_rect.height - 60,
    btn_w,
    btn_h,
)

# Footer tip position
footer_pos = (WIDTH // 2, HEIGHT - 10)

# -----------------------
# Main loop
# -----------------------
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard input
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN:
                # submit guess
                raw = input_text.strip()
                input_text = ""  # clear immediately as requested
                if raw == "":
                    result_message = "No input provided. Enter a number."
                    result_color = MUTED
                else:
                    if raw.lstrip("-").isdigit():
                        guess = int(raw)
                        attempts += 1
                        if guess < MIN_VAL or guess > MAX_VAL:
                            result_message = (
                                f"{guess} is out of range ({MIN_VAL}-{MAX_VAL})."
                            )
                            result_color = ORANGE
                        else:
                            if guess == secret:
                                result_message = f"{guess} is correct! You won in {attempts} attempts."
                                result_color = GREEN
                                game_over = True
                            elif guess > secret:
                                result_message = f"{guess} is too high, guess again."
                                result_color = RED
                            else:
                                result_message = f"{guess} is too low, guess again."
                                result_color = ORANGE
                    else:
                        result_message = f"'{raw}' is not a valid integer."
                        result_color = BLUE
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                # accept only digits and limit length to 3 (since MAX_VAL=100)
                if event.unicode.isdigit() and len(input_text) < 3:
                    input_text += event.unicode

        # mouse clicks for buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if guess_btn_rect.collidepoint(mx, my) and not game_over:
                # simulate pressing Enter
                raw = input_text.strip()
                input_text = ""
                if raw == "":
                    result_message = "No input provided. Enter a number."
                    result_color = MUTED
                else:
                    if raw.lstrip("-").isdigit():
                        guess = int(raw)
                        attempts += 1
                        if guess < MIN_VAL or guess > MAX_VAL:
                            result_message = (
                                f"{guess} is out of range ({MIN_VAL}-{MAX_VAL})."
                            )
                            result_color = ORANGE
                        else:
                            if guess == secret:
                                result_message = f"{guess} is correct! You won in {attempts} attempts."
                                result_color = GREEN
                                game_over = True
                            elif guess > secret:
                                result_message = f"{guess} is too high, guess again."
                                result_color = RED
                            else:
                                result_message = f"{guess} is too low, guess again."
                                result_color = ORANGE
                    else:
                        result_message = f"'{raw}' is not a valid integer."
                        result_color = BLUE
            if reset_btn_rect.collidepoint(mx, my):
                reset_game_full()

    # Draw background
    screen.fill(BG_COLOR)

    # Draw top card
    pygame.draw.rect(screen, CARD_COLOR, top_card_rect, border_radius=6)
    # Title and subtitle
    title_surf = title_font.render("Guess the Number Game", True, ACCENT)
    screen.blit(title_surf, (top_card_rect.x + 16, top_card_rect.y + 12))
    subtitle_surf = subtitle_font.render("by Mr. Halip", True, MUTED)
    screen.blit(
        subtitle_surf,
        (top_card_rect.x + 16, top_card_rect.y + 12 + title_surf.get_height() + 6),
    )
    # Description
    desc_text = f"Guess the secret number between {MIN_VAL} and {MAX_VAL}. Enter a number and press Guess."
    desc_surf = desc_font.render(desc_text, True, MUTED)
    screen.blit(
        desc_surf, (top_card_rect.x + 16, top_card_rect.y + top_card_rect.height - 28)
    )

    # Draw mid card
    pygame.draw.rect(screen, CARD_COLOR, mid_card_rect, border_radius=6)
    # Input label
    input_label = desc_font.render("Your guess", True, MUTED)
    screen.blit(input_label, (mid_card_rect.x + 16, mid_card_rect.y + 12))
    # Input box
    pygame.draw.rect(screen, BLACK, input_box_rect, 2, border_radius=4)
    # Input text centered vertically
    input_surface = input_font.render(input_text, True, TEXT)
    screen.blit(
        input_surface,
        (
            input_box_rect.x + 8,
            input_box_rect.y
            + (input_box_rect.height - input_surface.get_height()) // 2,
        ),
    )

    # Draw buttons
    pygame.draw.rect(screen, ACCENT, guess_btn_rect, border_radius=6)
    guess_text = desc_font.render("Guess", True, (255, 255, 255))
    screen.blit(
        guess_text,
        (
            guess_btn_rect.centerx - guess_text.get_width() // 2,
            guess_btn_rect.centery - guess_text.get_height() // 2,
        ),
    )

    pygame.draw.rect(screen, (230, 233, 239), reset_btn_rect, border_radius=6)
    reset_text = desc_font.render("Reset", True, TEXT)
    screen.blit(
        reset_text,
        (
            reset_btn_rect.centerx - reset_text.get_width() // 2,
            reset_btn_rect.centery - reset_text.get_height() // 2,
        ),
    )

    # Draw bottom card
    pygame.draw.rect(screen, CARD_COLOR, bottom_card_rect, border_radius=6)
    # Result message
    result_surf = result_font.render(result_message, True, result_color)
    screen.blit(result_surf, (bottom_card_rect.x + 16, bottom_card_rect.y + 18))
    # If game over and secret known, show the secret line
    if game_over:
        secret_line = desc_font.render(f"The correct number was {secret}", True, MUTED)
        screen.blit(
            secret_line,
            (
                bottom_card_rect.x + 16,
                bottom_card_rect.y + 18 + result_surf.get_height() + 8,
            ),
        )

    # Attempts label (top center)
    attempts_surf = attempts_font.render(f"Attempts: {attempts}", True, MUTED)
    screen.blit(attempts_surf, (WIDTH // 2 - attempts_surf.get_width() // 2, 20))

    # Footer tip
    footer_surf = footer_font.render("Tip: Press Enter to submit", True, MUTED)
    screen.blit(
        footer_surf,
        (
            footer_pos[0] - footer_surf.get_width() // 2,
            footer_pos[1] - footer_surf.get_height(),
        ),
    )

    # If game over, overlay message and options
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        screen.blit(overlay, (0, 0))
        go_msg = result_font.render(
            "You won! Press C to play again or Q to quit.", True, GREEN
        )
        screen.blit(go_msg, (WIDTH // 2 - go_msg.get_width() // 2, HEIGHT // 2 - 10))
        # handle keys for restart/quit while game_over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            reset_game_full()
        if keys[pygame.K_q]:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
