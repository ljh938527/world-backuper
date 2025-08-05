import os
import subprocess
from datetime import datetime
from config import create_config, read_config

try:
    conf = read_config()
except FileNotFoundError:
    conf = create_config()

def find_7z() -> str | None:
    """寻找 7z 位置"""
    for path in [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]:
        if os.path.exists(path):
            return path
    else:
        print("提示：未找到7z.exe，请在 www.7-zip.org 中安装 7-zip 到 C盘 或 从配置文件中添加您的 7zip 位置。")
        return None


def backup_world(quiet: bool = False) -> bool:
    """备份世界函数"""
    source_dir = conf["backup"]["source_dir"]
    output_dir = conf["backup"]["output_dir"]
    archive_name = conf["backup"]["archive_name"]

    seven_zip = conf["backup"]["7z_path"]  # 设置 7z 位置
    if not seven_zip:
        seven_zip = find_7z()
    if not seven_zip:
        return False

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{archive_name}_{timestamp}.7z")

    # 执行压缩
    try:
        if quiet:
            subprocess.run([
                seven_zip,
                "a", "-t7z", "-mx9", "-ssw", "-bso0", "-bsp0",
                output_file,
                os.path.join(source_dir, "*")
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run([
                seven_zip,
                "a", "-t7z", "-mx9", "-ssw",
                output_file,
                os.path.join(source_dir, "*")
            ], check=True)
            print(f"备份成功: {output_file}")
        return True
    except Exception as e:
        print(f"备份失败! 错误信息: {e}")
        return False

if __name__ == "__main__":
    # 手动执行备份
    backup_world()