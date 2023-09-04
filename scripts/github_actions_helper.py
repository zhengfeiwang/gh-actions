import os
from typing import Dict, List, Optional, Tuple

import requests


class GitHubActionsHelper:
    def __init__(self, owner: str, repo: str) -> None:
        self.owner = owner
        self.repo = repo
        self.host = f"https://api.github.com/repos/{owner}/{repo}"

    def _get_token(self) -> str:
        return os.getenv("GITHUB_TOKEN")

    def _create_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._get_token()}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def list_workflows(self):
        url = self.host + "/actions/workflows"
        response = requests.get(url, headers=self._create_headers())
        print(response.json)

    def list_workflow_runs(
            self, workflow_id: int, head_sha: Optional[str]
    ) -> Tuple[int, Dict]:
        url = self.host + f"/actions/workflows/{workflow_id}/runs"
        params = {"head_sha": head_sha} if head_sha is not None else None
        response = requests.get(
            url, headers=self._create_headers(), params=params
        )
        response_dict = response.json()
        return response_dict["total_count"], response_dict["workflow_runs"]

    def trigger_workflow_run(
            self, workflow_id: int, ref: str, inputs: Dict
    ) -> None:
        url = self.host + f"/actions/workflows/{workflow_id}/dispatches"
        headers = self._create_headers()
        data = {"ref": ref, "inputs": inputs}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

    def list_workflow_run_jobs(self, run_id: int) -> Tuple[int, List[Dict]]:
        url = self.host + f"/actions/runs/{run_id}/jobs"
        response = requests.get(url, headers=self._create_headers())
        response_dict = response.json()
        return response_dict["total_count"], response_dict["jobs"]
