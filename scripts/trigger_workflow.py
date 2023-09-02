import os
from typing import Dict

import requests
from dotenv import load_dotenv


OWNER = "zhengfeiwang"
REPO = "gh-actions"

URL = "https://api.github.com/repos/{owner}/{repo}/dispatches"


def get_token() -> str:
    return os.getenv("GITHUB_TOKEN")


def create_headers() -> Dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {get_token()}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def request_github() -> requests.Response:
    data = {
        "event_type": "create-branch",
        "client_payload": {
            "release_version": "1.0.0",
        }
    }
    response = requests.post(
        URL.format(owner=OWNER, repo=REPO),
        headers=create_headers(),
        json=data,
    )
    return response


def main():
    response = request_github()
    print(response.status_code)


if __name__ == "__main__":
    load_dotenv()
    main()
