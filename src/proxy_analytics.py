proxy_usage = {}

def log_proxy_usage(proxy, success=True):
    if proxy not in proxy_usage:
        proxy_usage[proxy] = {"successes": 0, "failures": 0}
    if success:
        proxy_usage[proxy]["successes"] += 1
    else:
        proxy_usage[proxy]["failures"] += 1

def analyze_proxy_performance():
    for proxy, stats in proxy_usage.items():
        success_rate = stats["successes"] / (stats["successes"] + stats["failures"]) if (stats["successes"] + stats["failures"]) > 0 else 0
        print(f"Proxy: {proxy}, Success Rate: {success_rate:.2%}")
        if success_rate < 0.1:
            print(f"[INFO] Low success rate detected for {proxy}, consider refreshing.")