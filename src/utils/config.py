def load_config(filename: str) -> dict:
    # Load config
    try:
        with open("config.json") as file:
            config = json.load(file)

    # Create config file
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(f"[!] Config Reset ({filename})")

        config = {"prefix": ",", "status": "idle"}

        with open("config.json", "w") as file:
            json.dump(config, file)

    return config
