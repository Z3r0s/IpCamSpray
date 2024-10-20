from colorama import Fore

def load_creds(fpath):
    try:
        with open(fpath, 'r') as f:
            creds = [tuple(line.strip().split(':')) for line in f]
        return creds
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Could not load credentials: {e}")
        return []