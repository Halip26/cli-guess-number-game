import pygame
import random
import sys
import os

# Config
MIN_VAL = 1
MAX_VAL = 100
WIDTH, HEIGHT = 360, 640
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Number Game by Mr. Halip")
clock = pygame.time.Clock()

# Optional: lihat daftar font sistem (uncomment untuk debug)
# pygame.font.init()
# print("Available system fonts:", pygame.font.get_fonts())


# --- FONT LOADING STRATEGY ---
# 1) Coba muat file TTF lokal jika ada
# 2) Jika tidak ada, fallback ke SysFont dengan nama populer
def load_font(
    preferred_ttf_path, size, fallback_name="arial", bold=False, italic=False
):
    """
    Mengembalikan objek pygame.font.Font atau pygame.font.SysFont.
    preferred_ttf_path: path ke file .ttf yang ingin dipakai (string)
    size: ukuran font (int)
    fallback_name: nama font sistem jika file tidak ditemukan
    """
    try:
        if preferred_ttf_path and os.path.exists(preferred_ttf_path):
            return pygame.font.Font(preferred_ttf_path, size)
    except Exception:
        pass
    # fallback ke SysFont
    return pygame.font.SysFont(fallback_name, size, bold=bold, italic=italic)


# Contoh: letakkan Roboto-Regular.ttf di folder "fonts/Roboto-Regular.ttf"
base_folder = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
roboto_path = os.path.join(
    base_folder, "fonts", "Roboto-Medium.ttf"
)  # ubah sesuai lokasi TTF

# Buat font dengan prioritas TTF lokal, lalu fallback ke Arial
title_font = load_font(roboto_path, 24, fallback_name="arial", bold=True)
subtitle_font = load_font(roboto_path, 14, fallback_name="arial")
desc_font = load_font(roboto_path, 12, fallback_name="arial")
input_font = load_font(roboto_path, 20, fallback_name="arial")
result_font = load_font(roboto_path, 16, fallback_name="arial")
attempts_font = load_font(roboto_path, 12, fallback_name="arial")
footer_font = load_font(roboto_path, 10, fallback_name="arial")


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

    # Top card content
    title_text = "Guess the Number Game"
    subtitle_text = "by Mr. Halip"
    desc_text = f"Guess the secret number between {MIN_VAL} and {MAX_VAL}. Enter a number and press Guess."

    title_surf = title_font.render(title_text, True, ACCENT)
    screen.blit(title_surf, (int(top_card_rect.x + 16), int(top_card_rect.y + 12)))

    subtitle_surf = subtitle_font.render(subtitle_text, True, MUTED)
    screen.blit(
        subtitle_surf,
        (
            int(top_card_rect.x + 16),
            int(top_card_rect.y + 12 + title_surf.get_height() + 6),
        ),
    )

    desc_surf = desc_font.render(desc_text, True, MUTED)
    screen.blit(
        desc_surf,
        (int(top_card_rect.x + 16), int(top_card_rect.y + top_card_rect.height - 28)),
    )

    # Mid card: input label and box
    input_label_surf = desc_font.render("Your guess", True, MUTED)
    screen.blit(
        input_label_surf, (int(mid_card_rect.x + 16), int(mid_card_rect.y + 12))
    )

    pygame.draw.rect(screen, BLACK, input_box_rect, 2, border_radius=4)
    input_surface = input_font.render(input_text, True, TEXT)
    input_y = (
        input_box_rect.y + (input_box_rect.height - input_surface.get_height()) // 2
    )
    screen.blit(input_surface, (int(input_box_rect.x + 8), int(input_y)))

    # Buttons
    pygame.draw.rect(screen, ACCENT, guess_btn_rect, border_radius=6)
    guess_text = desc_font.render("Guess", True, (255, 255, 255))
    screen.blit(
        guess_text,
        (
            int(guess_btn_rect.centerx - guess_text.get_width() // 2),
            int(guess_btn_rect.centery - guess_text.get_height() // 2),
        ),
    )

    pygame.draw.rect(screen, (230, 233, 239), reset_btn_rect, border_radius=6)
    reset_text = desc_font.render("Reset", True, TEXT)
    screen.blit(
        reset_text,
        (
            int(reset_btn_rect.centerx - reset_text.get_width() // 2),
            int(reset_btn_rect.centery - reset_text.get_height() // 2),
        ),
    )

    # Bottom card: result
    result_surf = result_font.render(result_message, True, result_color)
    screen.blit(
        result_surf, (int(bottom_card_rect.x + 16), int(bottom_card_rect.y + 18))
    )
    if game_over:
        secret_line = f"The correct number was {secret}"
        secret_surf = desc_font.render(secret_line, True, MUTED)
        screen.blit(
            secret_surf,
            (
                int(bottom_card_rect.x + 16),
                int(bottom_card_rect.y + 18 + result_surf.get_height() + 8),
            ),
        )

    # Attempts label top center
    attempts_text = f"Attempts: {attempts}"
    attempts_surf = attempts_font.render(attempts_text, True, MUTED)
    screen.blit(attempts_surf, (int(WIDTH // 2 - attempts_surf.get_width() // 2), 20))

    # Footer tip
    footer_text = "Tip: Press Enter to submit"
    footer_surf = footer_font.render(footer_text, True, MUTED)
    screen.blit(
        footer_surf,
        (
            int(footer_pos[0] - footer_surf.get_width() // 2),
            int(footer_pos[1] - footer_surf.get_height()),
        ),
    )

    # Game over overlay
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        screen.blit(overlay, (0, 0))
        go_msg = "You won! Press C to play again or Q to quit."
        go_surf = result_font.render(go_msg, True, GREEN)
        screen.blit(
            go_surf, (int(WIDTH // 2 - go_surf.get_width() // 2), int(HEIGHT // 2 - 10))
        )
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            new_game()
        if keys[pygame.K_q]:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
