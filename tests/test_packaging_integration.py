"""
Test suite for pip/packaging integration - SPRINT5 Task 6
Tests that lyric command is globally available after pip install
"""

import pytest
import sys
import os
import subprocess
import tempfile

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPackagingIntegration:
    """Test pip packaging integration and global lyric command availability."""

    def create_test_file(self, content: str) -> str:
        """Create a temporary .ly file with the given content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name

    def run_global_lyric_command(self, args: list) -> tuple[int, str, str]:
        """Run the global lyric command and return exit code, stdout, stderr."""
        cmd = ['lyric'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return result.returncode, result.stdout, result.stderr

    def test_global_lyric_command_exists(self):
        """Test that the global lyric command is available."""
        exit_code, stdout, stderr = self.run_global_lyric_command(['--version'])
        assert exit_code == 0
        assert "Lyric 0.1.6" in stdout

    def test_global_lyric_help_flag(self):
        """Test that --help flag works with global lyric command."""
        exit_code, stdout, stderr = self.run_global_lyric_command(['--help'])
        assert exit_code == 0
        assert "Lyric Language Interpreter" in stdout
        assert "command_or_file" in stdout
        assert "options:" in stdout

    def test_global_lyric_version_flag(self):
        """Test that --version flag works with global lyric command."""
        exit_code, stdout, stderr = self.run_global_lyric_command(['--version'])
        assert exit_code == 0
        assert "Lyric 0.1.6" in stdout

    def test_global_lyric_run_subcommand(self):
        """Test that 'lyric run file.ly' works with global command."""
        test_content = '''
def main() {
    print("Hello from global lyric run")
}
'''
        test_file = self.create_test_file(test_content)
        try:
            exit_code, stdout, stderr = self.run_global_lyric_command(['run', test_file])
            assert exit_code == 0
            assert "Hello from global lyric run" in stdout
        finally:
            os.unlink(test_file)

    def test_global_lyric_direct_file(self):
        """Test that 'lyric file.ly' works with global command."""
        test_content = '''
def main() {
    print("Hello from global lyric direct")
}
'''
        test_file = self.create_test_file(test_content)
        try:
            exit_code, stdout, stderr = self.run_global_lyric_command([test_file])
            assert exit_code == 0
            assert "Hello from global lyric direct" in stdout
        finally:
            os.unlink(test_file)

    def test_global_lyric_both_forms_identical(self):
        """Test that both forms produce identical output with global command."""
        test_content = '''
def main() {
    var x = 42
    print("Global lyric test:", x)
}
'''
        test_file = self.create_test_file(test_content)
        try:
            # Test run subcommand form
            exit_code1, stdout1, stderr1 = self.run_global_lyric_command(['run', test_file])
            
            # Test direct file form
            exit_code2, stdout2, stderr2 = self.run_global_lyric_command([test_file])
            
            # Both should succeed and produce identical output
            assert exit_code1 == 0
            assert exit_code2 == 0
            assert stdout1 == stdout2
            assert "Global lyric test: 42" in stdout1
        finally:
            os.unlink(test_file)

    def test_global_lyric_error_handling(self):
        """Test error handling with global lyric command."""
        # Test nonexistent file
        exit_code, stdout, stderr = self.run_global_lyric_command(['nonexistent.ly'])
        assert exit_code == 1
        assert "Error: File 'nonexistent.ly' not found" in stdout

        # Test missing file for run command
        exit_code, stdout, stderr = self.run_global_lyric_command(['run'])
        assert exit_code == 1
        assert "Error: 'run' command requires a file argument" in stdout

        # Test non-.ly file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Not a .ly file")
            test_file = f.name
        
        try:
            exit_code, stdout, stderr = self.run_global_lyric_command([test_file])
            assert exit_code == 1
            assert "Error: Expected .ly file, got" in stdout
        finally:
            os.unlink(test_file)

    def test_global_lyric_debug_flag(self):
        """Test that --debug flag works with global lyric command."""
        test_content = '''
def main() {
    var x = 5
    var y = x / 0  # This will cause a runtime error
}
'''
        test_file = self.create_test_file(test_content)
        try:
            # Test run subcommand with debug
            exit_code1, stdout1, stderr1 = self.run_global_lyric_command(['run', '--debug', test_file])
            
            # Test direct file form with debug
            exit_code2, stdout2, stderr2 = self.run_global_lyric_command(['--debug', test_file])
            
            # Both should fail with debug info
            assert exit_code1 == 1
            assert exit_code2 == 1
            assert "Runtime Error" in stdout1
            assert "Runtime Error" in stdout2
        finally:
            os.unlink(test_file)

    def test_global_lyric_no_arguments(self):
        """Test that no arguments shows help with global lyric command."""
        exit_code, stdout, stderr = self.run_global_lyric_command([])
        assert exit_code == 1
        assert "usage:" in stdout
        assert "Lyric Language Interpreter" in stdout

    def test_pyproject_toml_entry_points_configuration(self):
        """Test that pyproject.toml has correct entry_points configuration."""
        import tomllib
        
        with open('pyproject.toml', 'rb') as f:
            config = tomllib.load(f)
        
        # Check that [project.scripts] section exists
        assert 'project' in config
        assert 'scripts' in config['project']
        
        # Check that lyric script is configured
        scripts = config['project']['scripts']
        assert 'lyric' in scripts
        assert scripts['lyric'] == 'lyric.cli:main'

    def test_global_lyric_command_path(self):
        """Test that lyric command is in the expected location."""
        # Find where lyric command is installed
        result = subprocess.run(['where', 'lyric'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            # Command found, verify it's in a Scripts directory
            lyric_path = result.stdout.strip()
            assert 'Scripts' in lyric_path or 'bin' in lyric_path
        else:
            # On some systems, 'where' might not work, try 'which'
            result = subprocess.run(['which', 'lyric'], capture_output=True, text=True)
            if result.returncode == 0:
                lyric_path = result.stdout.strip()
                assert lyric_path  # Should have a path
