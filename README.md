# world-backuper

一个用于备份 Minecraft 存档 或其他文件夹的 python 程序。

![python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![apache](https://img.shields.io/badge/license-Apache-green?logo=apache)

### 如何使用它？

- 1.克隆仓库： `git clone https://github.com/ljh938527/world-backuper.git`
- 2.安装库： `pip install -r requirements.txt`
- 3.编辑配置文件： 先运行 `config.py`，再编辑 `config.toml`
- 4.启动自动备份： `python main.py`
- 5.手动执行备份： `python backup.py`

### 配置文件
```toml
[backup]
7z_path = ""                     # 自定义7z.exe的位置，若留空则从c盘搜索
source_dir = "./server/worlds"   # 需要备份的文件夹
output_dir = "./server/backup"   # 备份文件导出的目录
archive_name = "world"           # 压缩包文件名

[auto]
keep_days = 7                    # 自动备份时保留备份文件天数
backup_interval_minutes = 60     # 备份间隔分钟
log_dir = "logs"                 # 日志目录名
```
