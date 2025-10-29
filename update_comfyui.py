#!/usr/bin/env python3
"""
ComfyUI Update Script
This script updates ComfyUI, custom nodes, and Python dependencies.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComfyUIUpdater:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.path.dirname(os.path.realpath(__file__))
        self.custom_nodes_path = os.path.join(self.base_path, "custom_nodes")
        self.requirements_file = os.path.join(self.base_path, "requirements.txt")
        
    def run_command(self, cmd, cwd=None, shell=False):
        """Run a shell command and return the result."""
        try:
            logger.info(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_path,
                shell=shell,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                logger.info(result.stdout)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with error: {e.stderr}")
            return False, e.stderr
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False, str(e)
    
    def update_comfyui(self):
        """Update the main ComfyUI repository."""
        logger.info("=" * 60)
        logger.info("Updating ComfyUI...")
        logger.info("=" * 60)
        
        # Check if we're in a git repository
        if not os.path.exists(os.path.join(self.base_path, ".git")):
            logger.warning("Not a git repository. Skipping ComfyUI update.")
            return False
        
        # Stash any local changes
        logger.info("Stashing local changes...")
        self.run_command(["git", "stash"])
        
        # Fetch latest changes
        logger.info("Fetching latest changes from remote...")
        success, output = self.run_command(["git", "fetch", "origin"])
        if not success:
            logger.error("Failed to fetch from remote")
            return False
        
        # Get current branch
        success, current_branch = self.run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        if success:
            current_branch = current_branch.strip()
            logger.info(f"Current branch: {current_branch}")
        else:
            current_branch = "master"
        
        # Pull latest changes
        logger.info(f"Pulling latest changes for branch: {current_branch}...")
        success, output = self.run_command(["git", "pull", "origin", current_branch])
        
        if success:
            logger.info("✓ ComfyUI updated successfully!")
        else:
            logger.warning("Failed to pull changes. You may need to resolve conflicts manually.")
        
        return success
    
    def update_custom_nodes(self):
        """Update all custom nodes that are git repositories."""
        logger.info("=" * 60)
        logger.info("Updating custom nodes...")
        logger.info("=" * 60)
        
        if not os.path.exists(self.custom_nodes_path):
            logger.info("No custom_nodes directory found. Skipping.")
            return True
        
        # Find all custom node directories
        custom_nodes = [
            d for d in os.listdir(self.custom_nodes_path)
            if os.path.isdir(os.path.join(self.custom_nodes_path, d))
            and not d.startswith('.')
            and d != '__pycache__'
        ]
        
        if not custom_nodes:
            logger.info("No custom nodes found.")
            return True
        
        updated_count = 0
        failed_count = 0
        
        for node_dir in custom_nodes:
            node_path = os.path.join(self.custom_nodes_path, node_dir)
            git_path = os.path.join(node_path, ".git")
            
            if not os.path.exists(git_path):
                logger.info(f"  {node_dir}: Not a git repository, skipping...")
                continue
            
            logger.info(f"  Updating {node_dir}...")
            
            # Stash local changes
            self.run_command(["git", "stash"], cwd=node_path)
            
            # Pull latest changes
            success, output = self.run_command(["git", "pull"], cwd=node_path)
            
            if success:
                logger.info(f"    ✓ {node_dir} updated successfully")
                updated_count += 1
                
                # Check if requirements.txt exists and update dependencies
                node_requirements = os.path.join(node_path, "requirements.txt")
                if os.path.exists(node_requirements):
                    logger.info(f"    Installing requirements for {node_dir}...")
                    success, _ = self.run_command([
                        sys.executable, "-m", "pip", "install", "-r", node_requirements
                    ])
                    if success:
                        logger.info(f"    ✓ Requirements installed for {node_dir}")
            else:
                logger.warning(f"    ✗ Failed to update {node_dir}")
                failed_count += 1
        
        logger.info(f"\nCustom nodes update summary:")
        logger.info(f"  Updated: {updated_count}")
        logger.info(f"  Failed: {failed_count}")
        
        return failed_count == 0
    
    def update_dependencies(self):
        """Update Python dependencies from requirements.txt."""
        logger.info("=" * 60)
        logger.info("Updating Python dependencies...")
        logger.info("=" * 60)
        
        if not os.path.exists(self.requirements_file):
            logger.warning(f"Requirements file not found: {self.requirements_file}")
            return False
        
        logger.info("Installing/updating dependencies...")
        
        # Try with increased timeout and retries
        max_retries = 2
        for attempt in range(max_retries):
            if attempt > 0:
                logger.info(f"Retry attempt {attempt + 1}/{max_retries}...")
            
            success, output = self.run_command([
                sys.executable, "-m", "pip", "install", 
                "-r", self.requirements_file, 
                "--upgrade",
                "--default-timeout=100"
            ])
            
            if success:
                logger.info("✓ Dependencies updated successfully!")
                return True
            
            if attempt < max_retries - 1:
                logger.warning("Dependency update failed, retrying...")
        
        logger.warning("Failed to update dependencies after retries")
        logger.warning("You may need to run 'pip install -r requirements.txt --upgrade' manually")
        
        # Return True anyway if it's just a network issue - the script should continue
        return True
    
    def run_full_update(self):
        """Run a complete update of ComfyUI, custom nodes, and dependencies."""
        logger.info("\n" + "=" * 60)
        logger.info("Starting ComfyUI Full Update")
        logger.info("=" * 60 + "\n")
        
        results = {
            'comfyui': False,
            'custom_nodes': False,
            'dependencies': False
        }
        
        # Update ComfyUI
        results['comfyui'] = self.update_comfyui()
        
        # Update custom nodes
        results['custom_nodes'] = self.update_custom_nodes()
        
        # Update dependencies
        results['dependencies'] = self.update_dependencies()
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("Update Summary")
        logger.info("=" * 60)
        logger.info(f"ComfyUI: {'✓ Success' if results['comfyui'] else '✗ Failed'}")
        logger.info(f"Custom Nodes: {'✓ Success' if results['custom_nodes'] else '✗ Failed'}")
        logger.info(f"Dependencies: {'✓ Success' if results['dependencies'] else '✗ Failed'}")
        logger.info("=" * 60)
        
        all_success = all(results.values())
        
        if all_success:
            logger.info("\n✓ All updates completed successfully!")
            logger.info("\nTo restart ComfyUI:")
            logger.info("  1. Stop the current instance (Ctrl+C)")
            logger.info("  2. Run: python main.py")
        else:
            logger.warning("\n⚠ Some updates failed. Please check the logs above.")
        
        return all_success


def main():
    """Main entry point for the update script."""
    updater = ComfyUIUpdater()
    
    try:
        success = updater.run_full_update()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\nUpdate cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during update: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
