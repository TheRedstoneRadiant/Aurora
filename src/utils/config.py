def load_config(config_path: str) -> dict:
    # Load config
    try:
        with open(config_path) as file:
            config = json.load(file)

    # Create config file
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(f"[!] Config Reset ({config_path})")

        config = {"prefix": ",", "status": "idle"}

        with open(config_path, "w") as file:
            json.dump(config, file)

    return config
