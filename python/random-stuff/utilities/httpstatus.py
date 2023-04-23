import json


def http_status(post_url, response):
    status_str: str
    if response.status_code > 499:
        status_str = "[!] [{0}] Server Error".format(response.status_code)
        return status_str
    elif response.status_code == 404:
        status_str = "[!] [{0}] URL not found: [{1}]".format(response.status_code, post_url)
        return status_str
    elif response.status_code == 401:
        status_str = "[!] [{0}] Authentication Failed".format(response.status_code)
        return status_str
    elif response.status_code > 399:
        status_str = "[!] [{0}] Bad Request".format(response.status_code)
        print(response.content)
        return status_str
    elif response.status_code > 299:
        status_str = "[!] [{0}] Unexpected redirect.".format(response.status_code)
        return status_str
    elif response.status_code == 201 or response.status_code == 200:
        status_str = json.loads(response.content)
        return status_str
    else:
        status_str = "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(response.status_code, response.content)
        return status_str
