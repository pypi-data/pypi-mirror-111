def convert(str_headers: str):
    headers = {}
    for browser_header in str_headers.split('\n'):
        key, value = browser_header.rsplit(': ', 1)
        headers[str(key)] = str(value)
    return headers
