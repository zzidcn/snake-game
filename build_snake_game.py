import os
import sys
import subprocess
import shutil

def build_snake_game():
    """构建贪吃蛇游戏的可执行文件"""
    
    # 检查pygame是否安装
    try:
        import pygame
        print("✅ pygame 已安装")
    except ImportError:
        print("❌ pygame 未安装，正在安装...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pygame"], check=True)
            print("✅ pygame 安装成功")
        except Exception as e:
            print(f"❌ pygame 安装失败: {e}")
            return False
    
    # 创建dist目录
    dist_dir = os.path.join(os.path.dirname(__file__), 'dist')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # PyInstaller打包命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',           # 单文件模式
        '--windowed',          # 无控制台窗口
        '--name', 'SnakeGame_峰哥版',  # 可执行文件名
        '--clean',             # 清理临时文件
        'snake_game_enhanced.py'
    ]
    
    print("🚀 开始打包贪吃蛇游戏...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 运行打包命令
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode == 0:
            print("✅ 打包成功！")
            
            # 查找生成的exe文件
            exe_path = None
            for root, dirs, files in os.walk(dist_dir):
                for file in files:
                    if file.endswith('.exe') or (not file.endswith(('.dll', '.pyd', '.manifest')) and '.' not in file):
                        exe_path = os.path.join(root, file)
                        break
                if exe_path:
                    break
            
            if exe_path and os.path.exists(exe_path):
                final_exe = os.path.join(os.path.dirname(__file__), 'SnakeGame_峰哥版.exe')
                shutil.copy2(exe_path, final_exe)
                print(f"🎮 贪吃蛇游戏已生成: {final_exe}")
                print("\n📋 使用说明:")
                print("1. 双击 SnakeGame_峰哥版.exe 运行游戏")
                print("2. 方向键控制蛇的移动")
                print("3. 空格键暂停/继续")
                print("4. R键重新开始，M键返回菜单")
                print("5. 游戏会自动保存最高分记录")
                return True
            else:
                print("⚠️ 未找到生成的exe文件，请检查dist目录")
                return False
                
        else:
            print("❌ 打包失败:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 打包过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = build_snake_game()
    if success:
        print("\n🎉 贪吃蛇游戏打包完成！")
    else:
        print("\n💥 打包失败，请检查错误信息")