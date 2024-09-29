import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load assets
PLAYER_IMAGE = pygame.Surface((50, 50))
PLAYER_IMAGE.fill((0, 0, 255))  # Player color

OBSTACLE_IMAGE = pygame.Surface((50, 50))
OBSTACLE_IMAGE.fill((255, 0, 0))  # Obstacle color

BACKGROUND_IMAGE = pygame.Surface((WIDTH, HEIGHT))
BACKGROUND_IMAGE.fill((135, 206, 235))  # Sky color

# Font
FONT = pygame.font.Font(None, 36)

class Player:
    def __init__(self):
        self.rect = PLAYER_IMAGE.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.score = 0
        self.speed = 5

    def draw(self, surface):
        surface.blit(PLAYER_IMAGE, self.rect)

    def update(self):
        self.score += 1  # Increment score for each frame

class Obstacle:
    def __init__(self, x):
        self.rect = OBSTACLE_IMAGE.get_rect(topleft=(x, 0))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed  # Move downwards

    def draw(self, surface):
        surface.blit(OBSTACLE_IMAGE, self.rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Subway Surfer Clone")
    clock = pygame.time.Clock()

    player = Player()
    obstacles = []
    spawn_timer = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.rect.left > 0:
                player.rect.x -= player.speed  # Move left
            if keys[pygame.K_d] and player.rect.right < WIDTH:
                player.rect.x += player.speed  # Move right
            if keys[pygame.K_w] and player.rect.top > 0:
                player.rect.y -= player.speed  # Move up
            if keys[pygame.K_s] and player.rect.bottom < HEIGHT:
                player.rect.y += player.speed  # Move down

            # Spawn obstacles
            spawn_timer += 1
            if spawn_timer > 30:  # Adjust spawn rate
                spawn_timer = 0
                x = random.randint(0, WIDTH - 50)
                obstacles.append(Obstacle(x))

            # Update and draw obstacles
            for obstacle in obstacles[:]:
                obstacle.update()
                if obstacle.rect.top > HEIGHT:
                    obstacles.remove(obstacle)  # Remove off-screen obstacles
                if obstacle.rect.colliderect(player.rect):
                    game_over = True  # Collision detected

            player.update()

        # Fill the screen
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Draw player and obstacles
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Display score
        draw_text(screen, f"Score: {player.score}", (10, 10))

        if game_over:
            draw_text(screen, "Game Over!", (WIDTH // 2 - 70, HEIGHT // 2 - 20))
            draw_text(screen, "Press R to Restart", (WIDTH // 2 - 100, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

        if game_over and keys[pygame.K_r]:
            main()  # Restart the game

def draw_text(surface, text, position, color=BLACK):
    label = FONT.render(text, True, color)
    surface.blit(label, position)

if __name__ == "__main__":
    main()
