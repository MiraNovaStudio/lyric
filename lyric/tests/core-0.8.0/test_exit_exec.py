# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for exit() and exec() built-in functions (Sprint 9 Task 10)."""

import pytest
import subprocess
import sys
import tempfile
import os


def test_exit_with_zero():
    """Test exit(0) exits with code 0."""
    code = """
def main() {
    print("Before exit")
    exit(0)
    print("After exit")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Before exit" in result.stdout
        assert "After exit" not in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exit_with_nonzero():
    """Test exit(1) exits with code 1."""
    code = """
def main() {
    print("Exiting with error")
    exit(1)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Exiting with error" in result.stdout
        assert result.returncode == 1
    finally:
        os.unlink(temp_file)


def test_exit_default_zero():
    """Test exit() without argument defaults to 0."""
    code = """
def main() {
    exit()
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exit_with_custom_code():
    """Test exit() with various custom codes."""
    for code_value in [2, 5, 42, 127]:
        code = f"""
def main() {{
    exit({code_value})
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert result.returncode == code_value
        finally:
            os.unlink(temp_file)


def test_exec_simple_command():
    """Test exec() with a simple command."""
    code = """
def main() {
    int rc = exec("echo Hello")
    print("Return code:", rc)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Return code: 0" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exec_returns_return_code():
    """Test that exec() returns the command's return code."""
    # Use a command that will fail on most systems
    code = """
def main() {
    int rc = exec("exit 5")
    print("Command returned:", rc)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Command returned: 5" in result.stdout
        assert result.returncode == 0  # The Lyric program itself exits normally
    finally:
        os.unlink(temp_file)


def test_exec_success_zero():
    """Test that successful commands return 0."""
    # Create a temporary file to test with
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        
        # Normalize path for Windows
        test_file_normalized = test_file.replace('\\', '/')
        
        code = f"""
def main() {{
    int rc = exec("echo test > {test_file_normalized}")
    if rc == 0
        print("Command succeeded")
    else
        print("Command failed")
    end
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Command succeeded" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)


def test_exec_in_conditional():
    """Test using exec() return code in conditionals."""
    code = """
def main() {
    int result = exec("echo test")
    if result == 0
        print("Success")
    else
        print("Failed")
    end
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Success" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exec_multiple_commands():
    """Test executing multiple commands."""
    code = """
def main() {
    int rc1 = exec("echo First")
    int rc2 = exec("echo Second")
    print("RC1:", rc1, "RC2:", rc2)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "RC1: 0 RC2: 0" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exit_in_conditional():
    """Test exit() inside conditional blocks."""
    code = """
def main() {
    int x = 5
    if x > 3
        print("Exiting early")
        exit(10)
    end
    print("This should not print")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Exiting early" in result.stdout
        assert "This should not print" not in result.stdout
        assert result.returncode == 10
    finally:
        os.unlink(temp_file)


def test_exec_output_redirection():
    """Test exec() -> variable (output redirection)."""
    code = """
def main() {
    str output
    exec("echo Hello World") -> output
    print("Output:", output)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Output: Hello World" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exec_input_piping():
    """Test exec() <- variable (input piping)."""
    # Use a simple echo command that we pipe input to
    # Note: This is platform-dependent, so we'll use a simple approach
    code = """
def main() {
    str input_data = "test input data"
    str output
    exec("cat") <- input_data
    print("Input piped successfully")
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        # Just verify it doesn't crash - cat behavior varies by platform
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exec_output_multiple_lines():
    """Test exec() output redirection with multi-line output."""
    code = """
def main() {
    str output
    exec("echo Line1 && echo Line2") -> output
    print("Output:", output)
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
        f.write(code)
        f.flush()
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'lyric.cli', temp_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        assert "Line1" in result.stdout
        assert "Line2" in result.stdout
        assert result.returncode == 0
    finally:
        os.unlink(temp_file)


def test_exec_with_file_output():
    """Test exec() ->> file (append output to file)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "output.txt")
        test_file_normalized = test_file.replace('\\', '/')
        
        code = f"""
def main() {{
    dsk outfile = disk("{test_file_normalized}")
    exec("echo Test output") ->> outfile
    outfile.close()
    
    dsk readfile = disk("{test_file_normalized}")
    str content = readfile.read()
    print("File contains:", content)
    readfile.close()
}}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ly', delete=False) as f:
            f.write(code)
            f.flush()
            temp_ly_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'lyric.cli', temp_ly_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            assert "Test output" in result.stdout
            assert result.returncode == 0
        finally:
            os.unlink(temp_ly_file)


