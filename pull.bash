#!/bin/bash

WORKSPACE_ROOT="$(pwd)"

update_repo() {
    local REPO="$1"
    local REPO_NAME

    REPO_NAME=$(basename "$REPO")

    echo ""
    echo "========================================"
    echo "Updating: $REPO_NAME"
    echo "========================================"

    cd "$REPO" || {
        echo "ERROR: Could not enter $REPO"
        exit 1
    }

    git fetch origin

    git switch main || {
        echo "ERROR: Could not switch to main"
        exit 1
    }

    git pull --ff-only origin main || {
        echo "ERROR: Pull failed in $REPO_NAME"
        exit 1
    }

    cd "$WORKSPACE_ROOT"
}

echo "========================================"
echo "Starting update process..."
echo "Workspace: $WORKSPACE_ROOT"
echo "Started: $(date)"
echo "========================================"

# Update workspace first
update_repo "$WORKSPACE_ROOT"

# Update submodules
update_repo "$WORKSPACE_ROOT/implementations/minecraft/AlienCraft"
update_repo "$WORKSPACE_ROOT/implementations/python/python-package"

echo ""
echo "========================================"
echo "All repositories updated!"
echo "Finished: $(date)"
echo "========================================"