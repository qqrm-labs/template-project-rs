"""Read-only eligibility check; GitHub performs the actual merge and review gates."""

import json
import os
import re
import subprocess
from pathlib import Path


def compatible(dependencies):
    if not isinstance(dependencies, list) or not dependencies:
        return False
    for dependency in dependencies:
        if not isinstance(dependency, dict) or dependency.get("maintainerChanges"):
            return False
        if dependency.get("updateType") not in (
            "version-update:semver-patch", "version-update:semver-minor"
        ):
            return False
        versions = []
        for key in ("prevVersion", "newVersion"):
            value = dependency.get(key, "")
            if not isinstance(value, str):
                return False
            match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value)
            if not match:
                return False
            versions.append(tuple(map(int, match.groups())))
        old, new = versions
        # Rust 0.x minor bumps and 0.0.x patch bumps can be breaking changes.
        width = 1 if old[0] else (2 if old[1] else 3)
        if new <= old or old[:width] != new[:width]:
            return False
    return True


def verified_bot_commits(commits):
    return bool(commits) and all(
        (commit.get("author") or {}).get("login") == "dependabot[bot]"
        and commit.get("commit", {}).get("verification", {}).get("verified") is True
        for commit in commits
    )


def approval_candidates(reviews, head):
    latest = {}
    for review in sorted(reviews, key=lambda item: item["id"]):
        # A later comment does not revoke an approval; dismissal/changes do.
        if review["state"] in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[review["user"]["login"]] = review
    return [login for login, review in latest.items()
            if review["state"] == "APPROVED" and review["commit_id"] == head]


def api(endpoint, paginated=False):
    args = ["gh", "api", endpoint]
    if paginated:
        args += ["--paginate", "--slurp"]
    result = json.loads(subprocess.check_output(args, text=True))
    return [item for page in result for item in page] if paginated else result


def main():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pr = event["pull_request"]
    repo = event["repository"]["full_name"]
    endpoint = f"repos/{repo}/pulls/{pr['number']}"
    commits = api(endpoint + "/commits?per_page=100", paginated=True)
    metadata = json.loads(os.environ.get("DEPENDENCIES") or "[]")
    if verified_bot_commits(commits) and compatible(metadata):
        print("All dependency updates are compatible and signed by Dependabot.")
        return
    reviews = api(endpoint + "/reviews?per_page=100", paginated=True)
    for login in approval_candidates(reviews, pr["head"]["sha"]):
        if login == pr["user"]["login"]:
            continue
        permission = api(f"repos/{repo}/collaborators/{login}/permission")["permission"]
        if permission in ("admin", "maintain", "write"):
            print("A maintainer approved this exact dependency batch.")
            return
    raise SystemExit("This batch needs maintainer approval of its current commit: "
                     "breaking, unverified, or incomplete dependency metadata.")


if __name__ == "__main__":
    main()
