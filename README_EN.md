# 🐍 Snake Game - Feng's Edition

## 🎮 Features
- **Beautiful Interface**: Colorful snake body, dynamic food colors, grid background
- **Complete Functionality**: High score saving, dynamic difficulty, pause/resume
- **Smooth Experience**: Optimized performance and responsive controls
- **English Interface**: Fixed encoding issues for better compatibility

## 📁 File Structure
```
├── SnakeGame_Feng          # Executable file (Linux)
├── snake_game_fixed.py     # Game source code (English version)
├── README_EN.md           # Usage instructions
└── high_score.json        # High score record (auto-generated)
```

## 🚀 Usage
1. **Run directly**: Double-click `SnakeGame_Feng` or run in terminal:
   ```bash
   ./SnakeGame_Feng
   ```

2. **Game Controls**:
   - **Arrow Keys**: Control snake movement direction
   - **SPACE**: Pause/Resume game
   - **ENTER**: Start new game
   - **R**: Restart after game over
   - **M**: Return to main menu
   - **ESC**: Exit game

3. **Game Rules**:
   - Eat food to increase score and length
   - Speed increases every 3 foods eaten
   - Game ends when snake hits itself
   - High score is automatically saved

## 💡 Technical Details
- **Language**: Python 3.12 + Pygame 2.5.2
- **Packaging**: PyInstaller 6.19.0
- **File Size**: ~34MB (includes all dependencies)
- **Requirements**: Linux system with graphical interface

---

**Enjoy the game! 🎮**