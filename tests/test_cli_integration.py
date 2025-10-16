"""
Integration tests for CLI error handling and functionality.
"""

import pytest
import subprocess
import sys
import os


class TestCLIIntegration:
    """Test CLI integration and error handling."""
    
    def run_cli_command(self, args):
        """Run a CLI command and return the result."""
        cmd = [sys.executable, "-m", "lyric.cli"] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode, result.stdout, result.stderr
    
    def test_cli_run_success(self):
        """Test successful CLI run."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/hello.ly"])
        
        assert exit_code == 0
        assert "Hello, Lyric!" in stdout
        assert stderr == ""
    
    def test_cli_run_class_test(self):
        """Test CLI run of class_test.ly produces correct greeting."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/class_test.ly"])
        
        assert exit_code == 0
        assert "Creating player instance..." in stdout
        assert "Hello, Guest" in stdout
        assert "Hello, Alice" in stdout
        assert stderr == ""
    
    def test_cli_run_error_demo(self):
        """Test CLI run of error_demo.ly produces expected error messages."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/error_demo.ly"])
        
        assert exit_code == 1  # Should fail with error
        assert "Testing error reporting..." in stdout
        assert "Runtime Error: Undefined variable: undefined_variable" in stdout
        assert stderr == ""  # No Python traceback
    
    def test_cli_lex_error(self):
        """Test CLI handles lex errors gracefully."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/lex_error_demo.ly"])
        
        assert exit_code == 1
        assert "Lex Error in 'tests/examples/lex_error_demo.ly' [line 7, col 5]: Unexpected character '@'" in stdout
        assert stderr == ""  # No Python traceback
    
    def test_cli_parse_error(self):
        """Test CLI handles parse errors gracefully."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/parse_error_demo.ly"])
        
        assert exit_code == 1
        assert "Parse Error in 'tests/examples/parse_error_demo.ly' [line 10, col 1]: Expected 'end'" in stdout
        assert stderr == ""  # No Python traceback
    
    def test_cli_runtime_error(self):
        """Test CLI handles runtime errors gracefully."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/runtime_error_demo.ly"])
        
        assert exit_code == 1
        assert "Testing various runtime errors..." in stdout
        assert "Runtime Error: Undefined variable: undefined_variable" in stdout
        assert stderr == ""  # No Python traceback
    
    def test_cli_nonexistent_file(self):
        """Test CLI handles nonexistent files gracefully."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "nonexistent.ly"])
        
        assert exit_code == 1
        assert "Error:" in stdout
        assert stderr == ""
    
    def test_cli_wrong_extension(self):
        """Test CLI handles wrong file extensions."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/hello.txt"])
        
        assert exit_code == 1
        assert "Error:" in stdout
        assert stderr == ""
    
    def test_cli_integration_comprehensive(self):
        """Test CLI with comprehensive integration test."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/sprint2_integration_test.ly"])
        
        assert exit_code == 0
        assert "=== SPRINT 2 INTEGRATION TEST ===" in stdout
        assert "=== ALL SPRINT 2 FEATURES WORKING ===" in stdout
        assert stderr == ""
    
    def test_cli_nested_flow(self):
        """Test CLI with nested control flow example."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/nested_flow.ly"])
        
        assert exit_code == 0
        assert "Testing nested control flow..." in stdout
        assert "i is greater than 1: 2" in stdout
        assert "outer: 0 inner: 0" in stdout
        assert stderr == ""
    
    def test_cli_boolean_test(self):
        """Test CLI with boolean operations example."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/boolean_test.ly"])
        
        assert exit_code == 0
        assert "Testing boolean and comparison operations..." in stdout
        assert "a == b: False" in stdout
        assert "true and false: False" in stdout
        assert stderr == ""
    
    def test_cli_runtime_test(self):
        """Test CLI with runtime enhancements example."""
        exit_code, stdout, stderr = self.run_cli_command(["run", "tests/examples/runtime_test.ly"])
        
        assert exit_code == 0
        assert "=== Testing isinstance function ===" in stdout
        assert "isinstance(42, 'int'): True" in stdout
        assert "type(42): int" in stdout
        assert "range(2, 5): [2, 3, 4]" in stdout
        assert stderr == ""
