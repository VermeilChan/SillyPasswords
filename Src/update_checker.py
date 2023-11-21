import urllib.request
import json

GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'SillyPasswords'
CURRENT_VERSION = 'v1.0.5'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36'

def check_for_updates():
    print("Checking for updates...")
    latest_version, error = get_latest_version()

    if error:
        handle_error(error)
        return

    current_version_tuple = parse_version(CURRENT_VERSION)
    latest_version_tuple = parse_version(latest_version)

    compare_versions(current_version_tuple, latest_version_tuple)

def handle_error(error):
    print(f"Error: {error}")

def parse_version(version_string):
    return tuple(map(int, version_string.lstrip('v').split('.')))

def compare_versions(current_version, latest_version):
    latest_version_str = '.'.join(map(str, latest_version))
    current_version_str = '.'.join(map(str, current_version))

    if latest_version > current_version:
        print(f"A newer version '{latest_version_str}' is available.")
    else:
        print(f"You are currently running version '{current_version_str}', which is up to date.")

def get_latest_version():
    headers = {'User-Agent': USER_AGENT}

    try:
        response = make_github_api_request(headers)
        release_data = json.loads(response)
        latest_version = release_data['tag_name']
        return latest_version, None
    except urllib.error.URLError as url_error:
        return None, f"URL error: {url_error}"
    except ValueError as json_error:
        return None, f"JSON decoding error: {json_error}"

def make_github_api_request(headers):
    try:
        url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest'
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as url_error:
        raise url_error

check_for_updates()
