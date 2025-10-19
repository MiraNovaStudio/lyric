"""
Test suite for Lyric CLI functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch


class TestCLI:
    """Test cases for CLI functionality."""
    
    def test_cli_import(self):
        """Test that CLI module can be imported."""
        import lyric.cli
        assert hasattr(lyric.cli, 'main')
    
    def test_version_command(self):
        """Test --version command."""
        with patch('sys.argv', ['lyric', '--version']):
            with patch('sys.exit') as mock_exit:
                with patch('builtins.print') as mock_print:
                    from lyric.cli import main
                    main()
                    mock_print.assert_called_with("Lyric 0.1")
    
    def test_run_command_placeholder(self):
        """Test run command with valid file."""
        with patch('sys.argv', ['lyric', 'run', 'examples/hello.ly']):
            with patch('os.path.exists', return_value=True):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        from lyric.cli import main
                        main()
                        mock_print.assert_called_with("execution not implemented")
    
    def test_run_command_file_not_found(self):
        """Test run command with non-existent file."""
        with patch('sys.argv', ['lyric', 'run', 'nonexistent.ly']):
            with patch('os.path.exists', return_value=False):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        from lyric.cli import main
                        try:
                            main()
                        except SystemExit:
                            pass  # Expected due to sys.exit(1)
                        mock_print.assert_called_with("Error: File 'nonexistent.ly' not found")
                        mock_exit.assert_called_with(1)
    
    def test_run_command_invalid_extension(self):
        """Test run command with non-.ly file."""
        with patch('sys.argv', ['lyric', 'run', 'test.txt']):
            with patch('os.path.exists', return_value=True):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        from lyric.cli import main
                        try:
                            main()
                        except SystemExit:
                            pass  # Expected due to sys.exit(1)
                        mock_print.assert_called_with("Error: File 'test.txt' is not a .ly file")
                        mock_exit.assert_called_with(1)
