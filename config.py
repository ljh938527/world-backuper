import toml

def create_config() -> dict:
    config_data = {
        "backup": {
            "7z_path": "",
            "source_dir": "server/worlds",
            "output_dir": "server/backup",
            "archive_name": "world"
        }
    }
    with open('config.toml', 'w', encoding='utf-8') as f:
        toml.dump(config_data, f)
    return config_data

def read_config() -> dict:
    with open('config.toml', 'r', encoding='utf-8') as f:
        return toml.load(f)

if __name__ == "__main__":
    create_config()
    conf = read_config()
    print(conf)