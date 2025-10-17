PIVOT — Rename Core Package to lyric_lang

Context:
To align the internal package structure with the PyPI package name "lyric-lang" and future packaging requirements,
we will rename the main source directory from 'lyric' to 'lyric_lang'.
This change ensures consistent naming between the internal module, CLI entry point, and distribution name,
and will simplify packaging, imports, and future pip installation behavior.

Objective:
Safely rename the internal source directory and update all related references while preserving CLI functionality
so that the user can continue running Lyric programs using the 'lyric' command.

Implementation Details:
1. Directory Rename:
   - Rename the top-level source directory:
     From: /lyric
     To:   /lyric_lang

2. Update Import Paths:
   - Update all internal imports referencing "lyric" to use "lyric_lang".
     Example:
       from lyric_lang.cli import main
     becomes:
       from lyric_lang.cli import main

3. Update pyproject.toml:
   - Under [project], ensure the following:
     name = "lyric-lang"
   - Under [project.scripts], change the entry point to:
     lyric = "lyric_lang.cli:main"

4. Verify CLI Functionality:
   - Run the CLI using the module path to confirm the rename:
       python -m lyric_lang.cli run examples/hello.ly
   - After installing in editable mode, confirm the direct command still works:
       pip install -e .
       lyric run examples/hello.ly
   - Both invocations must execute successfully without import errors.

5. Update Documentation:
   - Update any references in README.md or docs/ referencing 'lyric.' imports to 'lyric_lang.'.
   - Confirm the usage examples still show 'lyric run program.ly' as the external CLI command.

6. Testing:
   - Run pytest to confirm all tests pass after the rename.
   - Ensure no
