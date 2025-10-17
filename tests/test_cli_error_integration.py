"""
Test suite for SPRINT6 Task 5: CLI Error Integration and Runtime Stability
"""

import subprocess
import sys
import os
import tempfile
from pathlib import Path


def test_cli_traceback_format():
    """Test that CLI prints readable 'Traceback' style messages for unhandled errors."""
    test_code = '''
def test_function() {
    print("In test_function")
    raise TypeError("Error in function")
}

def main() {
    print("Testing traceback format...")
    test_function()
}
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'lyric_lang.cli', 'run', temp_file
        ], capture_output=True, text=True, timeout=10)
        
        # Should exit with non-zero status
        assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
        
        # Should contain traceback format
        assert "Traceback (most recent call last):" in result.stdout, "Missing traceback header"
        assert "RuntimeErrorLyric: TypeError: Error in function" in result.stdout, "Missing error message"
        
        print("PASS: CLI traceback format test passed")
        
    finally:
        os.unlink(temp_file)


def test_cli_exit_codes():
    """Test that exit code ≠ 0 on unhandled error."""
    test_code = '''
def main() {
    raise "Test error"
}
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'lyric_lang.cli', 'run', temp_file
        ], capture_output=True, text=True, timeout=10)
        
        # Should exit with non-zero status
        assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
        
        print("PASS: CLI exit codes test passed")
        
    finally:
        os.unlink(temp_file)


def test_cli_graceful_handling():
    """Test that all exceptions within CLI context are handled gracefully."""
    test_code = '''
def main() {
    raise ValueError("Test value error")
}
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'lyric_lang.cli', 'run', temp_file
        ], capture_output=True, text=True, timeout=10)
        
        # Should exit with non-zero status
        assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
        
        # Should not contain raw Python traceback
        assert "File \"" not in result.stdout or "lyric_lang" not in result.stdout, "Found raw Python traceback in stdout"
        
        # Should contain formatted Lyric error
        assert "RuntimeErrorLyric: ValueError: Test value error" in result.stdout, "Missing formatted error message"
        
        print("PASS: CLI graceful handling test passed")
        
    finally:
        os.unlink(temp_file)


def test_cli_typed_errors():
    """Test that typed errors work correctly in CLI."""
    test_code = '''
def main() {
    raise TypeError("This is a typed error")
}
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'lyric_lang.cli', 'run', temp_file
        ], capture_output=True, text=True, timeout=10)
        
        # Should exit with non-zero status
        assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
        
        # Should contain the typed error message
        assert "RuntimeErrorLyric: TypeError: This is a typed error" in result.stdout, "Missing typed error message"
        
        print("PASS: CLI typed errors test passed")
        
    finally:
        os.unlink(temp_file)


def test_cli_simple_errors():
    """Test that simple string errors work correctly in CLI."""
    test_code = '''
def main() {
    raise "This is a simple error"
}
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'lyric_lang.cli', 'run', temp_file
        ], capture_output=True, text=True, timeout=10)
        
        # Should exit with non-zero status
        assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
        
        # Should contain the simple error message
        assert "RuntimeErrorLyric: This is a simple error" in result.stdout, "Missing simple error message"
        
        print("PASS: CLI simple errors test passed")
        
    finally:
        os.unlink(temp_file)


def test_cli_all_error_types():
    """Test that all error types work correctly in CLI."""
    error_types = ['Error', 'TypeError', 'ValueError', 'NameError', 'RuntimeError']
    
    for error_type in error_types:
        test_code = f'''
def main() {{
    raise {error_type}("This is a {error_type}")
}}
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'lyric_lang.cli', 'run', temp_file
            ], capture_output=True, text=True, timeout=10)
            
            # Should exit with non-zero status
            assert result.returncode != 0, f"Expected non-zero exit code for {error_type}, got {result.returncode}"
            
            # Should contain the error message
            assert f"RuntimeErrorLyric: {error_type}: This is a {error_type}" in result.stdout, f"Missing {error_type} error message"
            
        finally:
            os.unlink(temp_file)
    
    print("PASS: CLI all error types test passed")


if __name__ == "__main__":
    print("Running SPRINT6 Task 5 CLI Error Integration tests...")
    
    test_cli_traceback_format()
    test_cli_exit_codes()
    test_cli_graceful_handling()
    test_cli_typed_errors()
    test_cli_simple_errors()
    test_cli_all_error_types()
    
    print("\nSUCCESS: All SPRINT6 Task 5 tests passed!")
