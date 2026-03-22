#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐍 贪吃蛇游戏 - 增强版
作者: zzidcn & FengClaw
版本: 2.0

改进特性:
- 统一中英文支持
- 音效系统
- 多种游戏模式
- 主题切换
- 更好的用户体验
"""

import pygame
import sys
import random
import os
import json
import math
from enum import Enum

# 初始化Pygame和混音器（用于音效）
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'dark_green': (0, 200, 0),
    'blue': (0, 0, 255),
    'dark_blue': (0, 0, 150),
    'gray': (128, 128, 128),
    'light_gray': (200, 200, 200),
    'dark_gray': (50, 50, 50),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'pink': (255, 192, 203),
    'cyan': (0, 255, 255),
    'lime': (50, 205, 50),
}

# 游戏状态枚举
class GameState(Enum):
    MENU = 0
    RUNNING = 1
    PAUSED = 2
    GAME_OVER = 3
    SETTINGS = 4

# 游戏模式枚举
class GameMode(Enum):
    CLASSIC = 0      # 经典模式
    ENDLESS = 1      # 无尽模式（穿墙）
    SPEED = 2        # 速度挑战模式

# 主题枚举
class Theme(Enum):
    CLASSIC = 0      # 经典绿色
    OCEAN = 1        # 海洋蓝色
    FIRE = 2         # 火焰红色
    NEON = 3         # 霓虹多彩

class Snake:
    def __init__(self, theme=Theme.CLASSIC):
        self.theme = theme
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 初始向右
        self.score = 0
        self.grow_to = 3
        self.speed = 10  # 初始速度 (FPS)
        self.food_eaten = 0
        self.last_move_time = pygame.time.get_ticks()
        
    def get_head_position(self):
        return self.positions[0]
    
    def get_snake_color(self, segment_index):
        """根据主题和段落索引获取蛇身颜色"""
        base_colors = {
            Theme.CLASSIC: COLORS['green'],
            Theme.OCEAN: COLORS['blue'],
            Theme.FIRE: COLORS['red'],
            Theme.NEON: COLORS['cyan']
        }
        
        base_color = base_colors[self.theme]
        # 蛇头更亮，身体渐变
        if segment_index == 0:
            return tuple(min(255, c + 50) for c in base_color)
        else:
            # 身体颜色渐变
            factor = max(0.3, 1.0 - (segment_index / max(self.length, 10)))
            return tuple(int(c * factor) for c in base_color)
    
    def move(self, game_mode):
        """移动蛇"""
        current = self.get_head_position()
        x, y = self.direction
        
        # 计算新位置
        new_x = current[0] + x
        new_y = current[1] + y
        
        # 处理边界
        if game_mode == GameMode.ENDLESS:
            # 无尽模式：穿墙
            new_x = new_x % GRID_WIDTH
            new_y = new_y % GRID_HEIGHT
        else:
            # 经典模式：撞墙游戏结束
            if (new_x < 0 or new_x >= GRID_WIDTH or 
                new_y < 0 or new_y >= GRID_HEIGHT):
                return False
        
        new_position = (new_x, new_y)
        
        # 检查是否撞到自己（除了最后一个格子，因为蛇在移动）
        if new_position in self.positions[:-1]:
            return False
            
        self.positions.insert(0, new_position)
        
        # 如果不需要增长，移除尾部
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True
    
    def change_direction(self, direction):
        """改变方向，防止直接反向"""
        # 禁止直接反向移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = COLORS['red']
        self.spawn()
    
    def spawn(self, snake_positions=None):
        """生成食物，避免生成在蛇身上"""
        if snake_positions is None:
            snake_positions = []
            
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if self.position not in snake_positions:
                break
        
        # 随机食物颜色
        color_options = [COLORS['red'], COLORS['yellow'], COLORS['orange'], COLORS['purple']]
        self.color = random.choice(color_options)

class SoundManager:
    """音效管理器"""
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.load_sounds()
    
    def load_sounds(self):
        """加载音效（如果文件存在）"""
        try:
            # 创建简单的音效（如果没有音频文件）
            self.create_simple_sounds()
        except Exception as e:
            print(f"音效加载失败: {e}")
            self.enabled = False
    
    def create_simple_sounds(self):
        """创建简单的程序化音效"""
        # 吃食物音效
        eat_sound = self.generate_tone(880, 0.1)  # A5音符
        self.sounds['eat'] = eat_sound
        
        # 游戏结束音效
        game_over_sound = self.generate_tone(220, 0.3)  # A3音符
        self.sounds['game_over'] = game_over_sound
        
        # 移动音效（可选）
        # move_sound = self.generate_tone(440, 0.05)
        # self.sounds['move'] = move_sound
    
    def generate_tone(self, frequency, duration):
        """生成简单音调"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = pygame.sndarray.array(pygame.mixer.Sound(buffer=bytearray(frames * 2)))
        
        # 简单正弦波
        for i in range(frames):
            value = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            arr[i][0] = value  # 左声道
            arr[i][1] = value  # 右声道
            
        return pygame.sndarray.make_sound(arr)
    
    def play(self, sound_name):
        """播放音效"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass

class HighScoreManager:
    """最高分管理器"""
    def __init__(self, filename="high_score.json"):
        self.filename = filename
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        """加载最高分"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 初始化默认最高分
                return {
                    'classic': 0,
                    'endless': 0,
                    'speed': 0
                }
        except Exception as e:
            print(f"加载最高分失败: {e}")
            return {'classic': 0, 'endless': 0, 'speed': 0}
    
    def save_high_scores(self):
        """保存最高分"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.high_scores, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存最高分失败: {e}")
    
    def update_high_score(self, mode, score):
        """更新最高分"""
        mode_key = mode.name.lower()
        if score > self.high_scores.get(mode_key, 0):
            self.high_scores[mode_key] = score
            self.save_high_scores()
            return True
        return False
    
    def get_high_score(self, mode):
        """获取指定模式的最高分"""
        mode_key = mode.name.lower()
        return self.high_scores.get(mode_key, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 贪吃蛇游戏 - 增强版")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 游戏对象
        self.snake = Snake()
        self.food = Food()
        self.sound_manager = SoundManager()
        self.high_score_manager = HighScoreManager()
        
        # 游戏状态
        self.game_state = GameState.MENU
        self.game_mode = GameMode.CLASSIC
        self.current_theme = Theme.CLASSIC
        
        # 控制变量
        self.last_move_time = 0
        self.move_delay = 100  # 毫秒
        
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.MENU:
                    self.handle_menu_input(event.key)
                elif self.game_state == GameState.RUNNING:
                    self.handle_game_input(event.key)
                elif self.game_state == GameState.PAUSED:
                    self.handle_paused_input(event.key)
                elif self.game_state == GameState.GAME_OVER:
                    self.handle_game_over_input(event.key)
                elif self.game_state == GameState.SETTINGS:
                    self.handle_settings_input(event.key)
        
        return True
    
    def handle_menu_input(self, key):
        """处理菜单输入"""
        if key == pygame.K_1:
            self.game_mode = GameMode.CLASSIC
            self.start_new_game()
        elif key == pygame.K_2:
            self.game_mode = GameMode.ENDLESS
            self.start_new_game()
        elif key == pygame.K_3:
            self.game_mode = GameMode.SPEED
            self.start_new_game()
        elif key == pygame.K_s:
            self.game_state = GameState.SETTINGS
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def handle_game_input(self, key):
        """处理游戏输入"""
        if key == pygame.K_UP:
            self.snake.change_direction((0, -1))
        elif key == pygame.K_DOWN:
            self.snake.change_direction((0, 1))
        elif key == pygame.K_LEFT:
            self.snake.change_direction((-1, 0))
        elif key == pygame.K_RIGHT:
            self.snake.change_direction((1, 0))
        elif key == pygame.K_SPACE:
            self.game_state = GameState.PAUSED
        elif key == pygame.K_m:
            self.game_state = GameState.MENU
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def handle_paused_input(self, key):
        """处理暂停输入"""
        if key == pygame.K_SPACE:
            self.game_state = GameState.RUNNING
        elif key == pygame.K_m:
            self.game_state = GameState.MENU
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def handle_game_over_input(self, key):
        """处理游戏结束输入"""
        if key == pygame.K_RETURN or key == pygame.K_r:
            self.start_new_game()
        elif key == pygame.K_m:
            self.game_state = GameState.MENU
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def handle_settings_input(self, key):
        """处理设置输入"""
        if key == pygame.K_c:
            self.current_theme = Theme.CLASSIC
        elif key == pygame.K_o:
            self.current_theme = Theme.OCEAN
        elif key == pygame.K_f:
            self.current_theme = Theme.FIRE
        elif key == pygame.K_n:
            self.current_theme = Theme.NEON
        elif key == pygame.K_m:
            self.game_state = GameState.MENU
        elif key == pygame.K_ESCAPE:
            self.game_state = GameState.MENU
    
    def start_new_game(self):
        """开始新游戏"""
        self.snake = Snake(self.current_theme)
        self.food = Food()
        self.food.spawn(self.snake.positions)
        self.game_state = GameState.RUNNING
        self.last_move_time = pygame.time.get_ticks()
    
    def update(self):
        """更新游戏状态"""
        if self.game_state != GameState.RUNNING:
            return
        
        current_time = pygame.time.get_ticks()
        # 根据蛇的速度计算移动延迟
        speed_factor = max(50, 200 - (self.snake.speed * 5))  # 速度越快，延迟越短
        
        if current_time - self.last_move_time > speed_factor:
            self.last_move_time = current_time
            
            # 移动蛇
            if not self.snake.move(self.game_mode):
                # 游戏结束
                self.sound_manager.play('game_over')
                self.high_score_manager.update_high_score(self.game_mode, self.snake.score)
                self.game_state = GameState.GAME_OVER
                return
            
            # 检查是否吃到食物
            if self.snake.get_head_position() == self.food.position:
                self.snake.food_eaten += 1
                self.snake.grow_to += 1
                self.snake.score += 10
                
                # 每吃3个食物增加速度
                if self.snake.food_eaten % 3 == 0:
                    self.snake.speed += 1
                
                self.sound_manager.play('eat')
                self.food.spawn(self.snake.positions)
    
    def draw(self):
        """绘制游戏"""
        self.screen.fill(COLORS['black'])
        
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.RUNNING or self.game_state == GameState.PAUSED:
            self.draw_game()
            if self.game_state == GameState.PAUSED:
                self.draw_pause_overlay()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.game_state == GameState.SETTINGS:
            self.draw_settings()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """绘制主菜单"""
        # 标题
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("🐍 贪吃蛇游戏", True, COLORS['white'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # 菜单选项
        menu_items = [
            "1 - 经典模式 (Classic Mode)",
            "2 - 无尽模式 (Endless Mode)", 
            "3 - 速度挑战 (Speed Challenge)",
            "S - 设置 (Settings)",
            "ESC - 退出 (Exit)"
        ]
        
        for i, item in enumerate(menu_items):
            text = self.font.render(item, True, COLORS['white'])
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 200 + i*50))
            self.screen.blit(text, text_rect)
        
        # 显示各模式最高分
        high_scores_text = [
            f"经典模式最高分: {self.high_score_manager.get_high_score(GameMode.CLASSIC)}",
            f"无尽模式最高分: {self.high_score_manager.get_high_score(GameMode.ENDLESS)}",
            f"速度模式最高分: {self.high_score_manager.get_high_score(GameMode.SPEED)}"
        ]
        
        for i, text in enumerate(high_scores_text):
            score_text = self.small_font.render(text, True, COLORS['light_gray'])
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 450 + i*30))
            self.screen.blit(score_text, score_rect)
    
    def draw_settings(self):
        """绘制设置菜单"""
        title = self.font.render("⚙️ 设置 (Settings)", True, COLORS['white'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # 主题选项
        theme_items = [
            "C - 经典主题 (Classic Green)",
            "O - 海洋主题 (Ocean Blue)", 
            "F - 火焰主题 (Fire Red)",
            "N - 霓虹主题 (Neon Colors)"
        ]
        
        current_theme_text = f"当前主题: {self.current_theme.name}"
        current_theme = self.small_font.render(current_theme_text, True, COLORS['yellow'])
        current_theme_rect = current_theme.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(current_theme, current_theme_rect)
        
        for i, item in enumerate(theme_items):
            color = COLORS['white']
            if (self.current_theme == Theme.CLASSIC and i == 0 or
                self.current_theme == Theme.OCEAN and i == 1 or
                self.current_theme == Theme.FIRE and i == 2 or
                self.current_theme == Theme.NEON and i == 3):
                color = COLORS['yellow']
                
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 200 + i*50))
            self.screen.blit(text, text_rect)
        
        # 返回菜单
        back_text = self.font.render("M - 返回主菜单", True, COLORS['light_gray'])
        back_rect = back_text.get_rect(center=(WINDOW_WIDTH//2, 450))
        self.screen.blit(back_text, back_rect)
    
    def draw_game(self):
        """绘制游戏场景"""
        # 绘制网格背景
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLORS['dark_gray'], (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLORS['dark_gray'], (0, y), (WINDOW_WIDTH, y), 1)
        
        # 绘制蛇
        for i, pos in enumerate(self.snake.positions):
            color = self.snake.get_snake_color(i)
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, COLORS['black'], rect, 1)  # 边框
        
        # 绘制食物
        food_rect = pygame.Rect(
            self.food.position[0] * GRID_SIZE, 
            self.food.position[1] * GRID_SIZE, 
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(self.screen, self.food.color, food_rect)
        pygame.draw.rect(self.screen, COLORS['black'], food_rect, 1)
        
        # 绘制UI信息
        score_text = self.font.render(f"分数: {self.snake.score}", True, COLORS['white'])
        self.screen.blit(score_text, (10, 10))
        
        high_score = self.high_score_manager.get_high_score(self.game_mode)
        high_score_text = self.font.render(f"最高分: {high_score}", True, COLORS['yellow'])
        self.screen.blit(high_score_text, (10, 50))
        
        mode_text = self.small_font.render(f"模式: {self.game_mode.name}", True, COLORS['light_gray'])
        self.screen.blit(mode_text, (WINDOW_WIDTH - 150, 10))
        
        speed_text = self.small_font.render(f"速度: {self.snake.speed}", True, COLORS['light_gray'])
        self.screen.blit(speed_text, (WINDOW_WIDTH - 150, 40))
    
    def draw_pause_overlay(self):
        """绘制暂停覆盖层"""
        # 半透明覆盖
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("⏸️ 游戏暂停", True, COLORS['white'])
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.small_font.render("按空格键继续", True, COLORS['light_gray'])
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明覆盖
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("💀 游戏结束!", True, COLORS['red'])
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font.render(f"最终分数: {self.snake.score}", True, COLORS['white'])
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # 检查是否打破记录
        if self.high_score_manager.update_high_score(self.game_mode, self.snake.score):
            record_text = self.font.render("🎉 新纪录!", True, COLORS['yellow'])
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            self.screen.blit(record_text, record_rect)
        
        restart_text = self.small_font.render("按 ENTER 或 R 重新开始", True, COLORS['light_gray'])
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.small_font.render("按 M 返回主菜单", True, COLORS['light_gray'])
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 130))
        self.screen.blit(menu_text, menu_rect)
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 限制帧率
        
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()