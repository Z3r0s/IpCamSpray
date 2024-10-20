from tls_client import Session

def get_custom_tls_session():
    session = Session(
        client_identifier="chrome_108",  # Emulate a specific browser
        random_tls_extensions_order=True
    )
    return session

async def perform_tls_request(session, url, payload):
    session = get_custom_tls_session()
    return await session.post(url, json=payload)