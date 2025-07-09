# ScriptCraft Release Workflow Automation
# This script automates the process of updating both the python-package submodule
# and the main workspace repository after a PyPI release.

Write-Host "ðŸš€ ScriptCraft Release Workflow Automation" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Prompt for commit messages
$SubmoduleCommitMessage = Read-Host "`nEnter commit message for python-package submodule"
$WorkspaceCommitMessage = Read-Host "Enter commit message for main workspace"

# Get current version
$VersionFile = "implementations/python-package/scriptcraft/_version.py"
$CurrentVersion = ""
if (Test-Path $VersionFile) {
    $VersionContent = Get-Content $VersionFile
    $VersionMatch = $VersionContent | Select-String '__version__ = "([^"]+)"'
    if ($VersionMatch) {
        $CurrentVersion = $VersionMatch.Matches[0].Groups[1].Value
        Write-Host "`nCurrent version: $CurrentVersion" -ForegroundColor Cyan
    }
}

# Ask if user wants to update version
$UpdateVersion = Read-Host "Update version number? (y/n)"
$NewVersion = ""

if ($UpdateVersion -eq "y" -or $UpdateVersion -eq "Y") {
    $NewVersion = Read-Host "Enter new version number (e.g., 1.3.4)"
    
    # Validate version format
    if ($NewVersion -match '^\d+\.\d+\.\d+$') {
        Write-Host "âœ… Version format is valid" -ForegroundColor Green
    } else {
        Write-Host "âŒ Invalid version format. Please use format: X.Y.Z (e.g., 1.3.4)" -ForegroundColor Red
        exit 1
    }
}

# Ask if user wants to create a version tag
$CreateTag = Read-Host "Create version tag? (y/n)"
$Version = $NewVersion  # Use the new version for tagging

Write-Host "`nStarting release workflow..." -ForegroundColor Yellow

# Store the original directory
$OriginalDir = Get-Location

# Step 1: Update submodule repository
Write-Host "`nðŸ“¦ Step 1: Updating python-package submodule..." -ForegroundColor Yellow

Set-Location "implementations/python-package"

# Step 1a: Update version if requested
if ($NewVersion) {
    Write-Host "`nðŸ“ Updating version from $CurrentVersion to $NewVersion..." -ForegroundColor Yellow
    
    # Update the version file
    $VersionContent = Get-Content "scriptcraft/_version.py"
    $UpdatedContent = $VersionContent -replace '__version__ = "[^"]+"', "__version__ = `"$NewVersion`""
    Set-Content "scriptcraft/_version.py" $UpdatedContent
    
    Write-Host "âœ… Version updated in scriptcraft/_version.py" -ForegroundColor Green
}

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "Found changes to commit in submodule:" -ForegroundColor Cyan
    git status --short
    
    # Add all changes
    Write-Host "`nAdding changes..." -ForegroundColor Cyan
    git add .
    
    # Commit with provided message
    Write-Host "Committing with message: '$SubmoduleCommitMessage'" -ForegroundColor Cyan
    git commit -m $SubmoduleCommitMessage
    
    # Push to remote
    Write-Host "Pushing to remote..." -ForegroundColor Cyan
    git push
    
    Write-Host "âœ… Submodule updated successfully!" -ForegroundColor Green
} else {
    Write-Host "â„¹ï¸  No changes detected in submodule" -ForegroundColor Yellow
}

# Step 2: Update main workspace repository
Write-Host "`nðŸ  Step 2: Updating main workspace..." -ForegroundColor Yellow

Set-Location $OriginalDir

# Update submodule reference
Write-Host "Updating submodule reference..." -ForegroundColor Cyan
git submodule update --remote implementations/python-package

# Check if submodule was updated
$status = git status --porcelain
if ($status -match "implementations/python-package") {
    Write-Host "Submodule reference updated, committing..." -ForegroundColor Cyan
    git add implementations/python-package
    git commit -m $WorkspaceCommitMessage
    
    Write-Host "Pushing workspace changes..." -ForegroundColor Cyan
    git push
    
    Write-Host "âœ… Workspace updated successfully!" -ForegroundColor Green
} else {
    Write-Host "â„¹ï¸  No submodule updates detected" -ForegroundColor Yellow
}

# Step 3: Optional version tagging
if ($Version) {
    Write-Host "`nðŸ·ï¸  Step 3: Creating version tag..." -ForegroundColor Yellow
    Set-Location "implementations/python-package"
    
    Write-Host "Creating tag v$Version..." -ForegroundColor Cyan
    git tag "v$Version"
    git push origin "v$Version"
    
    Write-Host "âœ… Version tag v$Version created and pushed!" -ForegroundColor Green
}

Write-Host "`nðŸŽ‰ Release workflow completed successfully!" -ForegroundColor Green
Write-Host "Both repositories are now synchronized." -ForegroundColor Green

# Always return to original directory
Set-Location $OriginalDir
