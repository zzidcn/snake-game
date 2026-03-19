import pygame
import sys
import random
import os
import json

# 初始化Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# 游戏状态
GAME_RUNNING = 0
GAME_OVER = 1
GAME_PAUSED = 2
GAME_MENU = 3

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 初始向右
        self.score = 0
        self.grow_to = 3
        self.speed = 10  # 初始速度
        self.food_eaten = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # 检查是否撞到自己
        if new_position in self.positions[1:]:
            return False  # 游戏结束
        
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True  # 游戏继续
    
    def grow(self):
        self.grow_to += 1
        self.score += 10
        self.food_eaten += 1
        # 每吃3个食物增加速度
        if self.food_eaten % 3 == 0:
            self.speed = min(self.speed + 1, 20)
    
    def change_direction(self, direction):
        # 禁止反向移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

class Food:
    def __init__(self):
        self.colors = [RED, YELLOW, PURPLE, ORANGE]
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
        self.current_color = random.choice(self.colors)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game - Feng\'s Edition')
        self.clock = pygame.time.Clock()
        
        # 字体设置 - 使用英文避免编码问题
        self.font_large = pygame.font.SysFont('Arial', 36)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        
        self.snake = Snake()
        self.food = Food()
        self.state = GAME_MENU
        self.game_speed = self.snake.speed
        self.high_score = self.load_high_score()
        
    def load_high_score(self):
        """加载最高分"""
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0
        
    def save_high_score(self):
        """保存最高分"""
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
        
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw_snake(self):
        for i, pos in enumerate(self.snake.positions):
            if i == 0:  # 头部
                color = GREEN
            elif i == len(self.snake.positions) - 1:  # 尾部
                color = BLUE
            else:  # 身体
                # 渐变效果
                ratio = i / len(self.snake.positions)
                r = int(0 + ratio * 0)
                g = int(255 - ratio * 55)
                b = int(0 + ratio * 200)
                color = (r, g, b)
                
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)  # 添加边框
            
            # 绘制眼睛（只在头部）
            if i == 0:
                eye_size = GRID_SIZE // 5
                # 根据方向确定眼睛位置
                if self.snake.direction == (1, 0):  # 右
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.right - eye_size, rect.top + eye_size*2), eye_size)
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.right - eye_size, rect.bottom - eye_size*2), eye_size)
                elif self.snake.direction == (-1, 0):  # 左
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.left + eye_size, rect.top + eye_size*2), eye_size)
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.left + eye_size, rect.bottom - eye_size*2), eye_size)
                elif self.snake.direction == (0, -1):  # 上
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.left + eye_size*2, rect.top + eye_size), eye_size)
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.right - eye_size*2, rect.top + eye_size), eye_size)
                elif self.snake.direction == (0, 1):  # 下
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.left + eye_size*2, rect.bottom - eye_size), eye_size)
                    pygame.draw.circle(self.screen, BLACK, 
                                     (rect.right - eye_size*2, rect.bottom - eye_size), eye_size)
    
    def draw_food(self):
        pos = self.food.position
        rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, self.food.current_color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 1)  # 添加边框
        # 绘制食物内的装饰
        inner_rect = pygame.Rect(rect.left + GRID_SIZE//4, rect.top + GRID_SIZE//4, 
                                GRID_SIZE//2, GRID_SIZE//2)
        pygame.draw.rect(self.screen, DARK_BLUE, inner_rect)
    
    def draw_score(self):
        score_text = self.font_medium.render(f"Score: {self.snake.score}", True, WHITE)
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, YELLOW)
        speed_text = self.font_small.render(f"Speed: {self.snake.speed}", True, WHITE)
        length_text = self.font_small.render(f"Length: {len(self.snake.positions)}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        self.screen.blit(speed_text, (10, 70))
        self.screen.blit(length_text, (10, 90))
    
    def draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("Game Over!", True, RED)
        score_text = self.font_medium.render(f"Final Score: {self.snake.score}", True, WHITE)
        if self.snake.score > self.high_score:
            self.high_score = self.snake.score
            self.save_high_score()
            new_record_text = self.font_medium.render("🎉 New Record! 🎉", True, YELLOW)
            self.screen.blit(new_record_text, (WINDOW_WIDTH//2 - new_record_text.get_width()//2, 
                                              WINDOW_HEIGHT//2 + 20))
        
        restart_text = self.font_medium.render("Press R to Restart", True, WHITE)
        menu_text = self.font_medium.render("Press M for Menu", True, WHITE)
        quit_text = self.font_medium.render("Press ESC to Quit", True, WHITE)
        
        self.screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                                          WINDOW_HEIGHT//2 - 80))
        self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 
                                      WINDOW_HEIGHT//2 - 20))
        self.screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                                        WINDOW_HEIGHT//2 + 60))
        self.screen.blit(menu_text, (WINDOW_WIDTH//2 - menu_text.get_width()//2, 
                                     WINDOW_HEIGHT//2 + 100))
        self.screen.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 
                                     WINDOW_HEIGHT//2 + 140))
    
    def draw_pause(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("Game Paused", True, WHITE)
        continue_text = self.font_medium.render("Press SPACE to Continue", True, WHITE)
        menu_text = self.font_medium.render("Press M for Menu", True, WHITE)
        
        self.screen.blit(pause_text, (WINDOW_WIDTH//2 - pause_text.get_width()//2, 
                                      WINDOW_HEIGHT//2 - 30))
        self.screen.blit(continue_text, (WINDOW_WIDTH//2 - continue_text.get_width()//2, 
                                         WINDOW_HEIGHT//2 + 20))
        self.screen.blit(menu_text, (WINDOW_WIDTH//2 - menu_text.get_width()//2, 
                                     WINDOW_HEIGHT//2 + 60))
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title_text = self.font_large.render("🐍 Snake Game", True, GREEN)
        subtitle_text = self.font_medium.render("Feng's Edition", True, YELLOW)
        
        start_text = self.font_medium.render("Press ENTER to Start", True, WHITE)
        controls_text = self.font_small.render("Arrow Keys to Move | SPACE to Pause | ESC to Exit", True, LIGHT_GRAY)
        high_score_text = self.font_medium.render(f"Highest Score: {self.high_score}", True, YELLOW)
        
        self.screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 150))
        self.screen.blit(subtitle_text, (WINDOW_WIDTH//2 - subtitle_text.get_width()//2, 200))
        self.screen.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, 300))
        self.screen.blit(controls_text, (WINDOW_WIDTH//2 - controls_text.get_width()//2, 350))
        self.screen.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, 400))
    
    def check_collision(self):
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            # 确保食物不会生成在蛇身上
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.state == GAME_RUNNING:
                        if event.key == pygame.K_UP:
                            self.snake.change_direction((0, -1))
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction((0, 1))
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction((-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction((1, 0))
                        elif event.key == pygame.K_SPACE:
                            self.state = GAME_PAUSED
                        elif event.key == pygame.K_ESCAPE:
                            self.state = GAME_MENU
                    elif self.state == GAME_PAUSED:
                        if event.key == pygame.K_SPACE:
                            self.state = GAME_RUNNING
                        elif event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                            self.state = GAME_MENU
                    elif self.state == GAME_OVER:
                        if event.key == pygame.K_r:
                            self.snake.reset()
                            self.food.randomize_position()
                            self.state = GAME_RUNNING
                        elif event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                            self.state = GAME_MENU
                    elif self.state == GAME_MENU:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            self.snake.reset()
                            self.food.randomize_position()
                            self.state = GAME_RUNNING
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
            
            # 更新游戏状态
            if self.state == GAME_RUNNING:
                if not self.snake.update():
                    self.state = GAME_OVER
                
                self.check_collision()
                self.game_speed = self.snake.speed  # 更新游戏速度
            
            # 绘制游戏画面
            if self.state == GAME_MENU:
                self.draw_menu()
            else:
                self.screen.fill(BLACK)
                self.draw_grid()
                self.draw_snake()
                self.draw_food()
                self.draw_score()
                
                if self.state == GAME_OVER:
                    self.draw_game_over()
                elif self.state == GAME_PAUSED:
                    self.draw_pause()
            
            pygame.display.update()
            if self.state == GAME_RUNNING:
                self.clock.tick(self.game_speed)
            else:
                self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()