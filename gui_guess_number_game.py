import pygame
import pygame.freetype as freetype
import random
import sys
import os

# Config
MIN_VAL = 1
MAX_VAL = 100
WIDTH, HEIGHT = 460, 640
FPS = 30

# Colors
BG_COLOR = (247, 249, 252)
CARD_COLOR = (255, 255, 255)
ACCENT = (75, 123, 236)
MUTED = (107, 114, 128)
TEXT = (17, 24, 39)
ORANGE = (237, 134, 0)
GREEN = (4, 204, 17)
RED = (237, 0, 0)
BLUE = (0, 71, 237)
BLACK = (0, 0, 0)

# Init
pygame.init()
# Use SCALED to improve DPI handling on high-DPI displays
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Guess the Number Game by Mr. Halip")
clock = pygame.time.Clock()

# Optional music
try:
    pygame.mixer.init()
    music_path = "music/retro-game-music-245230.mp3"
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
except Exception:
    pass

# Use freetype for crisper text
freetype.init()
title_font = freetype.SysFont("Segoe UI", 22, bold=True)
subtitle_font = freetype.SysFont("Segoe UI", 14)
desc_font = freetype.SysFont("Segoe UI", 12)
input_font = freetype.SysFont("Segoe UI", 20)
result_font = freetype.SysFont("Segoe UI", 16)
attempts_font = freetype.SysFont("Segoe UI", 12, italic=True)
footer_font = freetype.SysFont("Segoe UI", 10)


# Game state
def new_game():
    global secret, attempts, input_text, result_message, result_color, game_over
    secret = random.randint(MIN_VAL, MAX_VAL)
    attempts = 0
    input_text = ""
    result_message = "Make your first guess!"
    result_color = TEXT
    game_over = False


new_game()

# UI geometry
pad_x = int(WIDTH * 0.05)
card_w = WIDTH - pad_x * 2
top_card_h = int(HEIGHT * 0.22)
mid_card_h = int(HEIGHT * 0.28)
bottom_card_h = int(HEIGHT * 0.32)

top_card_rect = pygame.Rect(pad_x, int(HEIGHT * 0.04), card_w, top_card_h)
mid_card_rect = pygame.Rect(pad_x, int(HEIGHT * 0.30), card_w, mid_card_h)
bottom_card_rect = pygame.Rect(pad_x, int(HEIGHT * 0.62), card_w, bottom_card_h)

input_box_rect = pygame.Rect(
    mid_card_rect.x + 16, mid_card_rect.y + 40, mid_card_rect.width - 32, 48
)

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

footer_pos = (WIDTH // 2, HEIGHT - 10)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN:
                raw = input_text.strip()
                input_text = ""  # clear immediately
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
                if event.unicode.isdigit() and len(input_text) < 3:
                    input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if guess_btn_rect.collidepoint(mx, my) and not game_over:
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
                new_game()

    # Draw background and cards
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, CARD_COLOR, top_card_rect, border_radius=6)
    pygame.draw.rect(screen, CARD_COLOR, mid_card_rect, border_radius=6)
    pygame.draw.rect(screen, CARD_COLOR, bottom_card_rect, border_radius=6)

    # Top card content (use render_to for crisper text)
    title_text = "Guess the Number Game"
    subtitle_text = "by Mr. Halip"
    desc_text = f"Guess the secret number between {MIN_VAL} and {MAX_VAL}. Enter a number and press Guess."

    # integer positions for sharp rendering
    title_x = top_card_rect.x + 16
    title_y = top_card_rect.y + 12
    title_font.render_to(screen, (title_x, title_y), title_text, ACCENT)

    subtitle_y = title_y + 28
    subtitle_font.render_to(screen, (title_x, subtitle_y), subtitle_text, MUTED)

    desc_y = top_card_rect.y + top_card_rect.height - 28
    # wrap description manually if too long (simple approach)
    desc_font.render_to(screen, (title_x, desc_y), desc_text, MUTED)

    # Mid card: input label and box
    input_label_y = mid_card_rect.y + 12
    desc_font.render_to(
        screen, (mid_card_rect.x + 16, input_label_y), "Your guess", MUTED
    )

    pygame.draw.rect(screen, BLACK, input_box_rect, 2, border_radius=4)
    # center vertically using integer math
    input_surface_y = (
        input_box_rect.y + (input_box_rect.height - input_font.get_sized_height()) // 2
    )
    input_font.render_to(
        screen, (input_box_rect.x + 8, int(input_surface_y)), input_text, TEXT
    )

    # Buttons
    pygame.draw.rect(screen, ACCENT, guess_btn_rect, border_radius=6)
    desc_font.render_to(
        screen,
        (guess_btn_rect.centerx - 20, guess_btn_rect.centery - 8),
        "Guess",
        (255, 255, 255),
    )

    pygame.draw.rect(screen, (230, 233, 239), reset_btn_rect, border_radius=6)
    desc_font.render_to(
        screen, (reset_btn_rect.centerx - 20, reset_btn_rect.centery - 8), "Reset", TEXT
    )

    # Bottom card: result
    result_font.render_to(
        screen,
        (bottom_card_rect.x + 16, bottom_card_rect.y + 18),
        result_message,
        result_color,
    )
    if game_over:
        secret_line = f"The correct number was {secret}"
        desc_font.render_to(
            screen,
            (
                bottom_card_rect.x + 16,
                bottom_card_rect.y + 18 + result_font.get_sized_height() + 8,
            ),
            secret_line,
            MUTED,
        )

    # Attempts label top center
    attempts_text = f"Attempts: {attempts}"
    attempts_surf_w = attempts_font.get_rect(attempts_text).width
    attempts_font.render_to(
        screen, (WIDTH // 2 - attempts_surf_w // 2, 20), attempts_text, MUTED
    )

    # Footer tip
    footer_text = "Tip: Press Enter to submit"
    footer_w = footer_font.get_rect(footer_text).width
    footer_font.render_to(
        screen,
        (footer_pos[0] - footer_w // 2, footer_pos[1] - footer_font.get_sized_height()),
        footer_text,
        MUTED,
    )

    # Game over overlay
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        screen.blit(overlay, (0, 0))
        go_msg = "You won! Press C to play again or Q to quit."
        result_font.render_to(
            screen,
            (WIDTH // 2 - result_font.get_rect(go_msg).width // 2, HEIGHT // 2 - 10),
            go_msg,
            GREEN,
        )
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            new_game()
        if keys[pygame.K_q]:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
