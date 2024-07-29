import pygame
import random
import json
import os

# 初始化 Pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("坦克大战")

# 颜色定义
SOFT_WHITE = (230, 230, 230)
SOFT_BLACK = (20, 20, 20)
SOFT_RED = (255, 100, 100)
SOFT_GREEN = (100, 255, 100)
SOFT_BLUE = (100, 100, 255)

# 坦克类
class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 40
        self.height = 60
        self.speed = 5
        self.health = 6

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def hit(self):
        self.health -= 1

# 子弹类
class Bullet:
    def __init__(self, x, y, color, direction, speed=10):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.speed = speed
        self.direction = direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.speed * self.direction

# 敌人类
class Enemy:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 40
        self.height = 60
        self.speed = 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

    def shoot(self):
        return Bullet(self.x + self.width // 2, self.y + self.height, SOFT_RED, 1)

# 主游戏循环
def main():
    clock = pygame.time.Clock()
    running = True
    score = 0

    player_tank = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70, SOFT_GREEN)
    bullets = []
    enemy_bullets = []
    enemies = []

    # 读取排行榜
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_tank.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player_tank.move(1, 0)
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(player_tank.x + player_tank.width // 2, player_tank.y, SOFT_RED, -1))
        if keys[pygame.K_z]:  # 技能：发射更强的子弹
            bullets.append(Bullet(player_tank.x + player_tank.width // 2, player_tank.y, SOFT_RED, -1, speed=20))

        # 生成敌人
        if random.randint(1, 50) == 1:
            enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 40), 0, SOFT_BLUE))

        # 敌人发射子弹
        for enemy in enemies:
            if random.randint(1, 100) == 1:
                enemy_bullets.append(enemy.shoot())

        screen.fill(SOFT_BLACK)
        player_tank.draw(screen)

        for bullet in bullets:
            bullet.move()
            bullet.draw(screen)
            if bullet.y < 0:
                bullets.remove(bullet)

        for enemy_bullet in enemy_bullets:
            enemy_bullet.move()
            enemy_bullet.draw(screen)
            if enemy_bullet.y > SCREEN_HEIGHT:
                enemy_bullets.remove(enemy_bullet)
            if player_tank.x < enemy_bullet.x < player_tank.x + player_tank.width and player_tank.y < enemy_bullet.y < player_tank.y + player_tank.height:
                enemy_bullets.remove(enemy_bullet)
                player_tank.hit()

        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)
            if enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)
            for bullet in bullets:
                if enemy.x < bullet.x < enemy.x + enemy.width and enemy.y < bullet.y < enemy.y + enemy.height:
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # 显示分数和血量
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, SOFT_WHITE)
        health_text = font.render(f"Health: {player_tank.health}", True, SOFT_WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

        # 显示排行榜
        leaderboard_text = font.render("Leaderboard:", True, SOFT_WHITE)
        screen.blit(leaderboard_text, (SCREEN_WIDTH - 200, 10))
        for i, score_entry in enumerate(leaderboard[:5]):
            rank_text = font.render(f"{i + 1}. {score_entry}", True, SOFT_WHITE)
            screen.blit(rank_text, (SCREEN_WIDTH - 200, 50 + i * 30))

        pygame.display.flip()
        clock.tick(60)

        if player_tank.health <= 0:
            running = False

    # 保存排行榜
    leaderboard.append(score)
    leaderboard = sorted(leaderboard, reverse=True)[:5]
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

    pygame.quit()

if __name__ == "__main__":
    main()