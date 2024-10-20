USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 8.1; SM-G960U Build/OPM1.171019.026)",
    "DVR-H264/1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "IPCam-Viewer/1.1",
    # Add more IoT-specific user agents
]
MAX_RETRIES = 3
TIMEOUT = 10  # seconds
ERROR_PATTERNS = ["login failed", "invalid user", "incorrect password"]