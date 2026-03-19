# 🪟 Windows版本生成说明

## 📋 生成步骤

要在Windows系统上生成可执行文件，请按以下步骤操作：

### 1. 安装Python和依赖
```cmd
# 下载并安装Python 3.12 (https://www.python.org/downloads/)
# 打开命令提示符并运行：
pip install pygame pyinstaller
```

### 2. 下载游戏源代码
从GitHub仓库下载以下文件：
- `snake_game_fixed.py`
- `high_score.json` (可选，用于保存最高分)

### 3. 生成Windows EXE
在包含游戏文件的目录中运行：
```cmd
pyinstaller --onefile --windowed --name "SnakeGame_Feng" snake_game_fixed.py
```

### 4. 获取可执行文件
生成的文件位于 `dist/SnakeGame_Feng.exe`

## 🎮 游戏功能
- **完整贪吃蛇游戏**: 移动、食物、计分、碰撞检测
- **精美界面**: 彩色蛇身、动态食物、网格背景  
- **高分保存**: 自动保存最高分记录
- **流畅体验**: 优化的性能和控制响应

## 📁 文件结构
```
├── SnakeGame_Feng.exe     # Windows可执行文件
├── snake_game_fixed.py    # 游戏源代码
└── high_score.json       # 最高分记录（自动生成）
```

## ⚙️ 系统要求
- **操作系统**: Windows 7/8/10/11
- **内存**: 512MB RAM (推荐 1GB+)
- **存储空间**: 50MB 可用空间
- **Python**: 不需要（已打包为独立exe）

## 🎯 使用方法
1. 双击 `SnakeGame_Feng.exe` 运行游戏
2. 使用方向键控制蛇的移动
3. 按空格键暂停/继续游戏
4. 游戏结束后按R重新开始，按M返回菜单

---

**注意**: 由于当前环境是Linux系统，无法直接生成Windows exe文件。请按照上述说明在Windows系统上生成。