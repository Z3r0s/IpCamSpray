import subprocess
import random
import asyncio
from colorama import Fore

def is_camera_reachable(ip_address):
    try:
        response = subprocess.run(['ping', '-c', '1', ip_address], stdout=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Failed to reach {ip_address}: {e}")
        return False

async def adaptive_rate_limit(response_time):
    if response_time > 3.0:
        await asyncio.sleep(random.uniform(3, 5))
    else:
        await asyncio.sleep(random.uniform(1, 2))