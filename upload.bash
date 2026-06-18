#!/bin/bash

WORKSPACE_ROOT="$(pwd)"

push_repo() {
local REPO="$1"
local REPO_NAME
local COMMIT_MESSAGE

REPO_NAME=$(basename "$REPO")
COMMIT_MESSAGE="Auto-update $(date '+%Y-%m-%d %H:%M:%S')"

echo ""
echo "========================================"
echo "Processing: $REPO_NAME"
echo "========================================"

cd "$REPO" || {
    echo "ERROR: Could not enter $REPO"
    exit 1
}

git add .

if git diff --cached --quiet; then
    echo "No changes detected."
else
    echo "Changes detected."
    echo "Committing with message: $COMMIT_MESSAGE"

    git commit -m "$COMMIT_MESSAGE" || {
        echo "ERROR: Commit failed in $REPO_NAME"
        exit 1
    }

    echo "Pushing..."

    git push || {
        echo "ERROR: Push failed in $REPO_NAME"
        exit 1
    }

    echo "Push complete."
fi

cd "$WORKSPACE_ROOT" || {
    echo "ERROR: Could not return to workspace root."
    exit 1
}

}

echo "========================================"
echo "Starting upload process..."
echo "Workspace: $WORKSPACE_ROOT"
echo "Started: $(date)"
echo "========================================"

push_repo "$WORKSPACE_ROOT/implementations/minecraft/AlienCraft"
push_repo "$WORKSPACE_ROOT/implementations/python/python-package"

Push workspace last so updated submodule SHAs are captured

push_repo "$WORKSPACE_ROOT"

echo ""
echo "========================================"
echo "All uploads complete!"
echo "Finished: $(date)"
echo "========================================"