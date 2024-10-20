from colorama import Fore

CONNECTIONS = []

def get_proxy_input():
    num_proxies = int(input(f"{Fore.CYAN}How many proxies would you like to add? "))
    for _ in range(num_proxies):
        proxy_type = input(f"{Fore.CYAN}Enter proxy type (http/https/socks5): ").strip().lower()
        proxy = input(f"{Fore.CYAN}Enter proxy (format: {proxy_type}://proxy:port): ").strip()
        if validate_proxy(proxy_type, proxy):
            CONNECTIONS.append({"address": proxy, "type": proxy_type})
        else:
            print(f"{Fore.RED}Invalid proxy format, please try again.")
            return get_proxy_input()

def validate_proxy(proxy_type, proxy):
    return proxy_type in ['http', 'https', 'socks5'] and proxy.startswith(f"{proxy_type}://")