import json
from colorama import Fore

def get_model_specific_data(model_name):
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
        model_data = config["models"].get(model_name, {})
        return model_data.get("login_url", "/login"), model_data.get("username_field", "username"), model_data.get("password_field", "password")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] Config file not found.")
        return "/login", "username", "password"