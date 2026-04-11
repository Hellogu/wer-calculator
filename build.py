"""
WERify 打包脚本
使用 PyInstaller 打包为可执行文件
"""
import os
import sys
import shutil
import subprocess


def clean_build():
    """清理之前的构建文件"""
    print("[清理] 清理构建文件...")
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除 {dir_name}/")
    
    # 删除 spec 文件（除了我们自定义的）
    if os.path.exists('app.spec'):
        os.remove('app.spec')
        print("   删除 app.spec")
    print("[完成] 清理完成\n")


def build_executable():
    """使用 PyInstaller 打包"""
    print("[打包] 开始打包...")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("[错误] PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # 执行打包
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'WERify.spec'
    ]
    
    print(f"   执行: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode != 0:
        print("\n[错误] 打包失败")
        return False
    
    print("\n[完成] 打包成功！")
    return True


def copy_additional_files():
    """复制额外文件到输出目录"""
    print("\n[复制] 复制额外文件...")
    
    dist_dir = 'dist'
    files_to_copy = [
        'README.md',
        'requirements.txt',
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy(file_name, os.path.join(dist_dir, file_name))
            print(f"   复制 {file_name}")
    
    print("[完成] 复制完成\n")


def show_result():
    """显示打包结果"""
    print("=" * 60)
    print("[完成] 打包完成！")
    print("=" * 60)
    
    dist_dir = os.path.abspath('dist')
    exe_name = 'WERify.exe' if sys.platform == 'win32' else 'WERify'
    exe_path = os.path.join(dist_dir, exe_name)
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"\n可执行文件: {exe_path}")
        print(f"文件大小: {size:.2f} MB")
        print(f"\n使用方式:")
        print(f"  1. 双击运行 {exe_name}")
        print(f"  2. 浏览器访问 http://localhost:5000")
        print(f"  3. 支持局域网其他设备访问")
    else:
        print("\n[警告] 未找到输出文件，请检查打包日志")
    
    print("\n" + "=" * 60)


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("[WERify] 打包工具")
    print("=" * 60 + "\n")
    
    # 确认
    response = input("是否开始打包? (y/n): ").strip().lower()
    if response != 'y':
        print("取消打包")
        return
    
    # 执行打包流程
    clean_build()
    
    if build_executable():
        copy_additional_files()
        show_result()
    else:
        print("打包过程中出现错误")
        sys.exit(1)


if __name__ == '__main__':
    main()
