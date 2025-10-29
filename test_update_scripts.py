#!/usr/bin/env python3
"""
Test suite for ComfyUI Update Scripts
This script validates the update functionality without making actual changes.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

# Import update_comfyui from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import update_comfyui
except ImportError:
    print("Error: update_comfyui module not found")
    sys.exit(1)


class TestComfyUIUpdater(unittest.TestCase):
    """Test cases for ComfyUIUpdater class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use cross-platform temporary directory
        self.test_base_path = os.path.join(tempfile.gettempdir(), "test_comfyui")
        self.updater = update_comfyui.ComfyUIUpdater(base_path=self.test_base_path)
    
    def test_initialization(self):
        """Test that the updater initializes correctly."""
        self.assertEqual(self.updater.base_path, self.test_base_path)
        self.assertEqual(
            self.updater.custom_nodes_path,
            os.path.join(self.test_base_path, "custom_nodes")
        )
        self.assertEqual(
            self.updater.requirements_file,
            os.path.join(self.test_base_path, "requirements.txt")
        )
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Success",
            stderr=""
        )
        
        success, output = self.updater.run_command(["echo", "test"])
        
        self.assertTrue(success)
        self.assertEqual(output, "Success")
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test failed command execution."""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, "cmd", stderr="Error")
        
        success, output = self.updater.run_command(["false"])
        
        self.assertFalse(success)
        self.assertEqual(output, "Error")
    
    @patch('os.path.exists')
    @patch.object(update_comfyui.ComfyUIUpdater, 'run_command')
    def test_update_comfyui_no_git(self, mock_run_command, mock_exists):
        """Test ComfyUI update when not in git repository."""
        mock_exists.return_value = False
        
        result = self.updater.update_comfyui()
        
        self.assertFalse(result)
        # Should not attempt git commands if not a git repo
    
    @patch('os.path.exists')
    @patch.object(update_comfyui.ComfyUIUpdater, 'run_command')
    def test_update_comfyui_success(self, mock_run_command, mock_exists):
        """Test successful ComfyUI update."""
        mock_exists.return_value = True
        mock_run_command.return_value = (True, "Success")
        
        result = self.updater.update_comfyui()
        
        self.assertTrue(result)
        # Verify git commands were called
        self.assertGreater(mock_run_command.call_count, 0)
    
    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_update_custom_nodes_empty(self, mock_isdir, mock_listdir, mock_exists):
        """Test custom nodes update with no nodes installed."""
        mock_exists.return_value = True
        mock_listdir.return_value = []
        
        result = self.updater.update_custom_nodes()
        
        self.assertTrue(result)
    
    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch.object(update_comfyui.ComfyUIUpdater, 'run_command')
    def test_update_custom_nodes_with_git_repos(
        self, mock_run_command, mock_isdir, mock_listdir, mock_exists
    ):
        """Test custom nodes update with git repositories."""
        # Setup mock filesystem
        def exists_side_effect(path):
            if "custom_nodes" in path:
                return True
            if ".git" in path:
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        mock_listdir.return_value = ["node1", "node2"]
        mock_isdir.return_value = True
        mock_run_command.return_value = (True, "Updated")
        
        result = self.updater.update_custom_nodes()
        
        self.assertTrue(result)
        # Should attempt to update both nodes
        self.assertGreater(mock_run_command.call_count, 0)
    
    @patch('os.path.exists')
    @patch.object(update_comfyui.ComfyUIUpdater, 'run_command')
    def test_update_dependencies_no_requirements(self, mock_run_command, mock_exists):
        """Test dependency update when requirements.txt doesn't exist."""
        mock_exists.return_value = False
        
        result = self.updater.update_dependencies()
        
        self.assertFalse(result)
        mock_run_command.assert_not_called()
    
    @patch('os.path.exists')
    @patch.object(update_comfyui.ComfyUIUpdater, 'run_command')
    def test_update_dependencies_success(self, mock_run_command, mock_exists):
        """Test successful dependency update."""
        mock_exists.return_value = True
        mock_run_command.return_value = (True, "Dependencies updated")
        
        result = self.updater.update_dependencies()
        
        self.assertTrue(result)
        mock_run_command.assert_called_once()
    
    @patch('os.path.exists')
    @patch.object(update_comfyui.ComfyUIUpdater, 'run_command')
    def test_update_dependencies_with_retry(self, mock_run_command, mock_exists):
        """Test dependency update with retry on failure."""
        mock_exists.return_value = True
        # First call fails, second succeeds
        mock_run_command.side_effect = [
            (False, "Timeout"),
            (True, "Success on retry")
        ]
        
        result = self.updater.update_dependencies()
        
        self.assertTrue(result)
        self.assertEqual(mock_run_command.call_count, 2)
    
    @patch.object(update_comfyui.ComfyUIUpdater, 'update_comfyui')
    @patch.object(update_comfyui.ComfyUIUpdater, 'update_custom_nodes')
    @patch.object(update_comfyui.ComfyUIUpdater, 'update_dependencies')
    def test_run_full_update_all_success(
        self, mock_deps, mock_nodes, mock_comfyui
    ):
        """Test full update when all components succeed."""
        mock_comfyui.return_value = True
        mock_nodes.return_value = True
        mock_deps.return_value = True
        
        result = self.updater.run_full_update()
        
        self.assertTrue(result)
        mock_comfyui.assert_called_once()
        mock_nodes.assert_called_once()
        mock_deps.assert_called_once()
    
    @patch.object(update_comfyui.ComfyUIUpdater, 'update_comfyui')
    @patch.object(update_comfyui.ComfyUIUpdater, 'update_custom_nodes')
    @patch.object(update_comfyui.ComfyUIUpdater, 'update_dependencies')
    def test_run_full_update_partial_failure(
        self, mock_deps, mock_nodes, mock_comfyui
    ):
        """Test full update when some components fail."""
        mock_comfyui.return_value = True
        mock_nodes.return_value = False
        mock_deps.return_value = True
        
        result = self.updater.run_full_update()
        
        self.assertFalse(result)


class TestScriptFiles(unittest.TestCase):
    """Test cases for script files existence and validity."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
    
    def test_python_script_exists(self):
        """Test that the Python update script exists."""
        script_path = os.path.join(self.base_path, "update_comfyui.py")
        self.assertTrue(os.path.exists(script_path))
    
    def test_shell_script_exists(self):
        """Test that the shell script exists."""
        script_path = os.path.join(self.base_path, "update_and_restart.sh")
        self.assertTrue(os.path.exists(script_path))
    
    def test_batch_script_exists(self):
        """Test that the batch script exists."""
        script_path = os.path.join(self.base_path, "update_and_restart.bat")
        self.assertTrue(os.path.exists(script_path))
    
    def test_readme_exists(self):
        """Test that the update README exists."""
        readme_path = os.path.join(self.base_path, "UPDATE_README.md")
        self.assertTrue(os.path.exists(readme_path))
    
    def test_guide_exists(self):
        """Test that the update guide exists."""
        guide_path = os.path.join(self.base_path, "UPDATE_GUIDE.md")
        self.assertTrue(os.path.exists(guide_path))
    
    def test_shell_script_executable(self):
        """Test that the shell script is executable (Unix only)."""
        if os.name == 'nt':
            self.skipTest("Executable test not applicable on Windows")
        
        script_path = os.path.join(self.base_path, "update_and_restart.sh")
        if not os.path.exists(script_path):
            self.fail(f"Shell script not found: {script_path}")
        
        is_executable = os.access(script_path, os.X_OK)
        self.assertTrue(is_executable, "Shell script is not executable")


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestComfyUIUpdater))
    suite.addTests(loader.loadTestsFromTestCase(TestScriptFiles))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
