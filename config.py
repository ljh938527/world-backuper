from typing import Any
import toml

def create_config() -> dict:
    """创建配置文件"""
    config_data = {
        "backup": {
            "7z_path": "",
            "source_dir": "./server/worlds",
            "output_dir": "./server/backup",
            "archive_name": "world"
        },
        "auto": {
            "keep_days": 7,  # 保留天数
            "backup_interval_minutes": 60,
            "log_dir": "logs"
        }
    }
    with open('config.toml', 'w', encoding='utf-8') as f:
        toml.dump(config_data, f)
    return config_data

def read_config() -> dict:
    """读取配置文件"""
    with open('config.toml', 'r', encoding='utf-8') as f:
        return toml.load(f)

def validate_config(config: dict[str, Any], start: int = 0, stop: int = 9) -> bool:
    """验证配置文件的完整性"""
    errors = []
    required = [
        "backup",
        "backup.7z_path",
        "backup.source_dir",
        "backup.output_dir",
        "backup.archive_name",
        "auto",
        "auto.keep_days",
        "auto.backup_interval_minutes",
        "auto.log_dir"
    ]
    for i in required[slice(start, stop)]:
        keys = i.split(".")
        current = config
        if len(keys) == 1 and keys[0] not in current:
            errors.append(i)
        elif len(keys) == 2 and keys[1] not in current[keys[0]]:
            errors.append(i)
    if errors:
        return False
    return True

if __name__ == "__main__":
    create_config()
    conf = read_config()
    print(conf)
    print(validate_config(conf))
