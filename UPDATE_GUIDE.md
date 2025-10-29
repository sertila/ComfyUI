# ComfyUI Update Guide

This guide provides instructions for updating ComfyUI, custom nodes, and dependencies.

## Update Scripts

Three update scripts are provided:

1. **update_comfyui.py** - Core Python script that handles all updates
2. **update_and_restart.sh** - Linux/Mac wrapper script with restart functionality
3. **update_and_restart.bat** - Windows wrapper script with restart functionality

## Quick Start

### Linux/Mac

```bash
# Make the script executable (first time only)
chmod +x update_and_restart.sh

# Run the update script
./update_and_restart.sh
```

### Windows

```batch
# Double-click update_and_restart.bat
# Or run from command prompt:
update_and_restart.bat
```

### Python Direct

```bash
# Run the update script directly
python update_comfyui.py
```

## What Gets Updated

The update script performs the following operations:

### 1. ComfyUI Core Update
- Stashes any local changes
- Fetches latest changes from the remote repository
- Pulls and merges updates for the current branch
- Preserves your local modifications in git stash

### 2. Custom Nodes Update
- Scans the `custom_nodes` directory
- Updates all custom nodes that are git repositories
- Automatically installs/updates requirements.txt for each node
- Skips non-git directories

### 3. Python Dependencies Update
- Updates all dependencies from requirements.txt
- Upgrades packages to their latest compatible versions
- Ensures all ComfyUI features continue to work

## Manual Update Process

If you prefer to update manually:

### Update ComfyUI

```bash
cd /path/to/ComfyUI
git stash
git pull
pip install -r requirements.txt --upgrade
```

### Update Custom Nodes

```bash
cd custom_nodes/your_custom_node
git pull
pip install -r requirements.txt  # if it exists
```

## Restart ComfyUI

After updating, you need to restart ComfyUI for changes to take effect:

### Method 1: Using the Script
The wrapper scripts (`.sh` and `.bat`) will offer to restart automatically.

### Method 2: Manual Restart

1. Stop the current ComfyUI instance:
   - Press `Ctrl+C` in the terminal where ComfyUI is running
   - Or kill the process manually

2. Start ComfyUI again:
   ```bash
   python main.py
   ```

## Troubleshooting

### Update Conflicts

If you see git merge conflicts:

```bash
# View conflicting files
git status

# Option 1: Keep your changes
git stash
git pull
git stash pop

# Option 2: Discard local changes
git reset --hard HEAD
git pull
```

### Custom Node Issues

If a custom node fails to update:

1. Navigate to the custom node directory
2. Check for uncommitted changes: `git status`
3. Either commit changes or stash them: `git stash`
4. Try updating again: `git pull`

### Dependency Conflicts

If dependency updates fail:

```bash
# Try updating pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt --upgrade
```

### Permission Errors

If you encounter permission errors:

```bash
# Linux/Mac
sudo chown -R $USER:$USER /path/to/ComfyUI

# Or run with sudo (not recommended)
sudo python update_comfyui.py
```

## Update Frequency

### Recommended Update Schedule

- **ComfyUI Core**: Weekly or when major features are released
- **Custom Nodes**: As needed or when experiencing issues
- **Dependencies**: Monthly or when prompted by security updates

### Before Updating

✅ **Best Practices:**
- Backup your workflows and custom settings
- Check the ComfyUI release notes for breaking changes
- Test updates in a development environment first
- Keep a record of your custom nodes and their versions

## Rollback

If an update causes issues:

### Rollback ComfyUI

```bash
cd /path/to/ComfyUI
git log --oneline  # Find the commit hash you want to revert to
git checkout <commit-hash>
```

### Rollback Custom Nodes

```bash
cd custom_nodes/problematic_node
git log --oneline
git checkout <commit-hash>
```

## Advanced Options

### Update to a Specific Branch

```bash
git checkout branch-name
git pull origin branch-name
```

### Update to Stable Release

```bash
git checkout master
git pull origin master
# Or use tagged release
git checkout tags/v1.0.0
```

### Selective Custom Node Updates

Edit the `update_comfyui.py` script to skip specific nodes:

```python
# Add to the update_custom_nodes method
skip_nodes = ['node_to_skip', 'another_node_to_skip']
if node_dir in skip_nodes:
    logger.info(f"  {node_dir}: Skipping (in skip list)")
    continue
```

## Support

If you encounter issues:

1. Check the ComfyUI GitHub issues: https://github.com/comfyanonymous/ComfyUI/issues
2. Join the ComfyUI Discord: https://discord.gg/comfyui
3. Review custom node repositories for specific node issues

## Script Customization

The `update_comfyui.py` script can be customized:

- Modify update behavior
- Add pre/post-update hooks
- Implement automatic backups
- Add notification systems

See the script source code for implementation details.
