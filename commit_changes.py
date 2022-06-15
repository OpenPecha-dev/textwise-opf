from pathlib import Path
from git import Repo
import os





def commit(repo, message, not_includes=[], branch="master"):
    has_changed = False

    for fn in repo.untracked_files:
        ignored = False
        for not_include_fn in not_includes:
            if not_include_fn in fn:
                ignored = True
        if ignored:
            continue
        if fn:
            repo.git.add(fn)
        if has_changed is False:
            has_changed = True

    if repo.is_dirty() is True:
        for fn in repo.git.diff(None, name_only=True).split("\n"):
            if fn:
                repo.git.add(fn)
            if has_changed is False:
                has_changed = True
        if has_changed is True:
            if not message:
                message = "Initial commit"
            repo.git.commit("-m", message)
            repo.git.push("origin", branch)

def setup_auth(repo, org, token):
    remote_url = repo.remote().url
    old_url = remote_url.split("//")
    authed_remote_url = f"{old_url[0]}//{org}:{token}@{old_url[1]}"
    repo.remote().set_url(authed_remote_url)


if __name__ == "__main__":
    token = "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"
    commit_msg = "updated opf"
    pedurma_types = ["namsel_pedurma", "derge_google_pedurma"]
    for pedurma_type in pedurma_types:
        pecha_paths = list(Path(f'./original/{pedurma_type}/').iterdir())
        pecha_paths.sort()
        for pecha_path in pecha_paths:
            pecha_path = Path(f"{pecha_path}")
            repo = Repo(pecha_path)
            setup_auth(repo, "Openpecha", token)
            commit(repo,commit_msg, branch="master")
            print(f"{pecha_path.stem} of {pedurma_type} has updated")