#!/usr/bin/env python3
"""
改进版贪吃蛇游戏打包脚本
支持音效、配置文件和更多资源
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查并安装依赖"""
    dependencies = ['pygame']
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} 已安装")
        except ImportError:
            print(f"❌ {dep} 未安装，正在安装...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
                print(f"✅ {dep} 安装成功")
            except Exception as e:
                print(f"❌ {dep} 安装失败: {e}")
                return False
    return True

def create_dist_directory():
    """创建dist目录"""
    dist_dir = Path(__file__).parent / 'dist'
    dist_dir.mkdir(exist_ok=True)
    return dist_dir

def build_with_pyinstaller():
    """使用PyInstaller打包"""
    # 基础命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--clean',
        '--name', 'SnakeGame_Enhanced',
        '--add-data', 'game_config.json' + os.pathsep + '.',
    ]
    
    # 添加图标（如果有）
    icon_path = Path('snake_icon.ico')
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
    
    # 添加主脚本
    cmd.append('snake_game_improved.py')
    
    print("🚀 开始打包改进版贪吃蛇游戏...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 打包成功!")
        print("📦 可执行文件位置: dist/SnakeGame_Enhanced")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 打包过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    print("🐍 贪吃蛇游戏打包工具 - 改进版")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，无法继续打包")
        return
    
    # 创建dist目录
    create_dist_directory()
    
    # 打包
    if build_with_pyinstaller():
        print("\n🎉 打包完成！")
        print("💡 使用方法:")
        print("   Linux: ./dist/SnakeGame_Enhanced")
        print("   Windows: dist\\SnakeGame_Enhanced.exe")
    else:
        print("\n❌ 打包失败，请检查错误信息")

if __name__ == "__main__":
    main()