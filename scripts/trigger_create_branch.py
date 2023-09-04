import argparse
import uuid
from typing import Tuple

import git
from dotenv import load_dotenv

from github_actions_helper import GitHubActionsHelper


OWNER = "zhengfeiwang"
REPO = "gh-actions"

CREATE_BRANCH_WORKFLOW_ID = 68023982


def trigger(gh: GitHubActionsHelper, release_version: str) -> Tuple[str, str]:
    # get head_sha
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    # generate uuid
    client_run_id = str(uuid.uuid4())
    # trigger workflow
    branch = "main"
    inputs = {"release_version": release_version, "id": client_run_id}
    gh.trigger_workflow_run(
        workflow_id=CREATE_BRANCH_WORKFLOW_ID, ref=branch, inputs=inputs
    )
    return sha, client_run_id


def get_workflow_run_id(gh: GitHubActionsHelper, sha: str, client_run_id: str) -> str:
    count, runs = gh.list_workflow_runs(
        workflow_id=CREATE_BRANCH_WORKFLOW_ID, head_sha=sha
    )
    if count == 1:
        return runs[0]["id"]
    
    for run in runs:
        run_id = run["id"]
        _, jobs = gh.list_workflow_run_jobs(run_id=run_id)
        for job in jobs:
            steps = [step["name"] for step in job["steps"]]
            if f"workflow run id - {client_run_id}" in steps:
                return run_id


def main(args: argparse.Namespace):
    gh_helper = GitHubActionsHelper(owner=OWNER, repo=REPO)
    sha, client_run_id = trigger(gh_helper, args.release_version)
    print("sha:", sha)
    print("client_run_id:", client_run_id)
    workflow_run_id = get_workflow_run_id(gh_helper, sha, client_run_id)
    print("workflow_run_id:", workflow_run_id)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release-version",
        dest="release_version",
        type=str,
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    main(args=parse_args())
