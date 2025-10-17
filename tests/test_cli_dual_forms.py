"""
Test suite for CLI dual form functionality - SPRINT5 Task 5
Tests both 'lyric run file.ly' and 'lyric file.ly' command forms
"""

import pytest
import sys
import os
import subprocess
import tempfile

# Add the parent directory to the path so we can import lyric
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLIDualForms:
    """Test both CLI command forms work correctly."""

    def create_test_file(self, content: str) -> str:
        """Create a temporary .ly file with the given content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name

    def run_cli_command(self, args: list) -> tuple[int, str, str]:
        """Run a CLI command and return exit code, stdout, stderr."""
        cmd = [sys.executable, '-m', 'lyric.cli'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return result.returncode, result.stdout, result.stderr

    def test_run_subcommand_form(self):
        """Test 'lyric run file.ly' form works correctly."""
        test_content = '''
def main() {
    print("Hello from run subcommand")
}
'''
        test_file = self.create_test_file(test_content)
        try:
            exit_code, stdout, stderr = self.run_cli_command(['run', test_file])
            assert exit_code == 0
            assert "Hello from run subcommand" in stdout
        finally:
            os.unlink(test_file)

    def test_direct_file_form(self):
        """Test 'lyric file.ly' form works correctly."""
        test_content = '''
def main() {
    print("Hello from direct file")
}
'''
        test_file = self.create_test_file(test_content)
        try:
            exit_code, stdout, stderr = self.run_cli_command([test_file])
            assert exit_code == 0
            assert "Hello from direct file" in stdout
        finally:
            os.unlink(test_file)

    def test_both_forms_produce_same_output(self):
        """Test that both forms produce identical output."""
        test_content = '''
def main() {
    var x = 42
    print("Value:", x)
}
'''
        test_file = self.create_test_file(test_content)
        try:
            # Test run subcommand form
            exit_code1, stdout1, stderr1 = self.run_cli_command(['run', test_file])
            
            # Test direct file form
            exit_code2, stdout2, stderr2 = self.run_cli_command([test_file])
            
            # Both should succeed and produce identical output
            assert exit_code1 == 0
            assert exit_code2 == 0
            assert stdout1 == stdout2
            assert "Value: 42" in stdout1
        finally:
            os.unlink(test_file)

    def test_run_command_missing_file_error(self):
        """Test error when 'run' command is missing file argument."""
        exit_code, stdout, stderr = self.run_cli_command(['run'])
        assert exit_code == 1
        assert "Error: 'run' command requires a file argument" in stdout
        assert "Usage: lyric run <file_name.ly>" in stdout

    def test_nonexistent_file_error(self):
        """Test error when file doesn't exist."""
        exit_code, stdout, stderr = self.run_cli_command(['nonexistent.ly'])
        assert exit_code == 1
        assert "Error: File 'nonexistent.ly' not found" in stdout

    def test_non_ly_file_error(self):
        """Test error when file is not a .ly file."""
        # Create a temporary non-.ly file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is not a .ly file")
            test_file = f.name
        
        try:
            exit_code, stdout, stderr = self.run_cli_command([test_file])
            assert exit_code == 1
            assert f"Error: Expected .ly file, got '{test_file}'" in stdout
        finally:
            os.unlink(test_file)

    def test_no_arguments_shows_help(self):
        """Test that no arguments shows help message."""
        exit_code, stdout, stderr = self.run_cli_command([])
        assert exit_code == 1
        assert "usage:" in stdout
        assert "Lyric Language Interpreter" in stdout
        assert "command_or_file" in stdout

    def test_debug_flag_works_both_forms(self):
        """Test that --debug flag works with both command forms."""
        test_content = '''
def main() {
    var x = 5
    var y = x / 0  # This will cause a runtime error
}
'''
        test_file = self.create_test_file(test_content)
        try:
            # Test run subcommand with debug
            exit_code1, stdout1, stderr1 = self.run_cli_command(['run', '--debug', test_file])
            
            # Test direct file form with debug
            exit_code2, stdout2, stderr2 = self.run_cli_command(['--debug', test_file])
            
            # Both should fail with debug info
            assert exit_code1 == 1
            assert exit_code2 == 1
            assert "Runtime Error" in stdout1
            assert "Runtime Error" in stdout2
            # Debug mode should show stack traces (if implemented)
        finally:
            os.unlink(test_file)

    def test_version_flag_works(self):
        """Test that --version flag works."""
        exit_code, stdout, stderr = self.run_cli_command(['--version'])
        assert exit_code == 0
        assert "Lyric 0.1.9" in stdout

    def test_help_flag_works(self):
        """Test that --help flag works."""
        exit_code, stdout, stderr = self.run_cli_command(['--help'])
        assert exit_code == 0
        assert "Lyric Language Interpreter" in stdout
        assert "command_or_file" in stdout

    def test_run_nonexistent_file_error(self):
        """Test error when 'run' command is used with nonexistent file."""
        exit_code, stdout, stderr = self.run_cli_command(['run', 'nonexistent.ly'])
        assert exit_code == 1
        assert "Error: File 'nonexistent.ly' not found" in stdout

    def test_run_non_ly_file_error(self):
        """Test error when 'run' command is used with non-.ly file."""
        # Create a temporary non-.ly file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is not a .ly file")
            test_file = f.name
        
        try:
            exit_code, stdout, stderr = self.run_cli_command(['run', test_file])
            assert exit_code == 1
            assert f"Error: Expected .ly file, got '{test_file}'" in stdout
        finally:
            os.unlink(test_file)
