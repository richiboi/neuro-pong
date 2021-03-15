import pygame
import math
from emg import EMG

pygame.init()

WIN_WIDTH = 1024
WIN_HEIGHT = 512

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong pong")
clock = pygame.time.Clock()

# === NEW PLAYER CLASS ==============================


class Player():

    paddle_width = 20
    paddle_height = 100
    paddle_x_vel = 8
    paddle_y_vel = 20

    def reset(self, x, y):
        self.rect = pygame.Rect(x, y, self.paddle_width, self.paddle_height)
        self.score = 0

    def __init__(self, x, y):
        self.reset(x, y)

    def move_horz(self, dir):
        # check boundary - left-mid, right-mid
        if (30 <= self.rect.x + dir * self.paddle_x_vel <= WIN_WIDTH//2 - 100 - self.paddle_width
                or WIN_WIDTH//2 + 100 <= self.rect.x + dir * self.paddle_x_vel <= WIN_WIDTH-30-self.paddle_width):
            self.rect.x += dir * self.paddle_x_vel

    def move_vert(self, dir):
        if 0 < self.rect.y + dir*self.paddle_y_vel < WIN_HEIGHT-self.paddle_height:
            self.rect.y += dir * self.paddle_y_vel

    def draw(self):
        pygame.draw.rect(win, (255, 255, 255), self.rect)

# =====Ball class=====================


class Ball():
    size = 16
    max_return_angle = 0.9
    initial_vel = 2.5

    def reset(self):
        self.rect = pygame.Rect(WIN_WIDTH // 2, 50, self.size, self.size)
        self.vel = self.initial_vel
        self.angle = -0.6
        self.serve_count = 30

    def __init__(self):
        self.reset()

    def move(self):
        if self.serve_count > 0:
            self.serve_count -= 1
            return

        self.rect.x += math.cos(self.angle) * self.vel
        self.rect.y += math.sin(self.angle) * self.vel
        #print(self.angle, self.rect.y)

    def check_wall_bounce(self):
        # Top collisions flip angle
        if self.rect.y > WIN_HEIGHT-self.size:
            self.angle = -self.angle
            self.rect.y = WIN_HEIGHT-self.size-1
            print('1')

        if self.rect.y < 0:
            self.angle = -self.angle
            self.rect.y = 1
            print(self.angle)
            print('2')

        if self.rect.x < 0 or self.rect.x > WIN_WIDTH - self.size:
            self.angle = math.pi - self.angle

    def check_scored(self, player1, player2):
        if self.rect.x < 0:
            player2.score += 1
            self.reset()

        if self.rect.x > WIN_WIDTH - self.size:
            player1.score += 1
            self.reset()

        if player1.score == 10 or player2.score == 10:
            if player1.score == 10:
                game_over_loop(player1)
            if player2.score == 10:
                game_over_loop(player2)
            player1.reset(40, 200)
            player2.reset(WIN_WIDTH-40, 200)
            self.reset()

    def check_player_collide(self, player1, player2):

        if self.rect.colliderect(player1.rect):
            rel_y = self.rect.y + self.size//2 - player1.rect.y
            return_angle = (2 * self.max_return_angle * rel_y /
                            player1.paddle_height) - self.max_return_angle

            self.angle = return_angle
            self.vel = self.initial_vel + abs(return_angle * 6)
            self.rect.left = player1.rect.right

        elif self.rect.colliderect(player2.rect):
            rel_y = self.rect.y + self.size//2 - player2.rect.y
            return_angle = (2 * self.max_return_angle * rel_y /
                            player2.paddle_height) - self.max_return_angle

            self.angle = math.pi - return_angle
            self.vel = self.initial_vel + abs(return_angle * 6)
            self.rect.right = player2.rect.left

    def draw(self, player1, player2):
        self.move()
        self.check_wall_bounce()
        self.check_player_collide(player1, player2)
        self.check_scored(player1, player2)
        pygame.draw.rect(win, (255, 255, 255), self.rect)


# ==========================
def draw_env(player1, player2):
    # Display line and text
    pygame.draw.line(win, (255, 255, 255), (WIN_WIDTH//2, 0),
                     (WIN_WIDTH//2, WIN_HEIGHT), 4)
    font = pygame.font.Font('freesansbold.ttf', 40)
    p1text = font.render(str(player1.score), True, (255, 255, 255))
    p2text = font.render(str(player2.score), True, (255, 255, 255))
    win.blit(p1text, (WIN_WIDTH//2 - 66, 50))
    win.blit(p2text, (WIN_WIDTH//2 + 50, 50))


def redraw_window(player1, player2, ball):
    win.fill((0, 0, 0))
    draw_env(player1, player2)

    player1.draw()
    player2.draw()
    ball.draw(player1, player2)
    pygame.display.update()


def game_over_loop(winner):
    run = True
    while run:
        pygame.time.delay(5)
        clock.tick(60)
        win.fill((0, 0, 0))

        rect_width = 300
        rect_height = 100
        rect_x = WIN_WIDTH//2-rect_width//2
        rect_y = WIN_HEIGHT//2-rect_height//2
        pygame.draw.rect(win, (255, 255, 255),
                         (rect_x, rect_y, rect_width, rect_height))
        # display the text
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render('Game over! Press Y to try again', True, (0, 0, 0))
        win.blit(text, (rect_x + 30, rect_y + 20))

        pygame.display.update()

        # Check keys for reset
        keys = pygame.key.get_pressed()

        if keys[pygame.K_y]:
            print('Game reset')
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# ==== MAIN LOOP ========================


def main():
    player1 = Player(40, 200)
    player2 = Player(WIN_WIDTH-60, 200)
    ball = Ball()

    emg = EMG(0)

    run = True

    while run:
        pygame.time.delay(5)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # no repeat keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    print('c')

        # Check keys
        keys = pygame.key.get_pressed()

        # player 1
        # if keys[pygame.K_w]:
        #     player1.move_vert(-1)

        # if keys[pygame.K_s]:
        #     player1.move_vert(1)

        player1.move_vert(emg.read())

        # player 2
        if keys[pygame.K_UP]:
            player2.move_vert(-1)

        if keys[pygame.K_DOWN]:
            player2.move_vert(1)

        redraw_window(player1, player2, ball)


main()

pygame.quit()
