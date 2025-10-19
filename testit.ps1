# Run Lyric language interpreter tests
# PowerShell version for Windows

Write-Host "Running Lyric interpreter tests..." -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Run tests from the lyric package
Write-Host "Running lexer tests..." -ForegroundColor Yellow
python -m pytest lyric/tests/test_lexer.py -v

Write-Host ""
Write-Host "Running parser tests..." -ForegroundColor Yellow
python -m pytest lyric/tests/test_parser.py -v

Write-Host ""
Write-Host "Running interpreter tests..." -ForegroundColor Yellow
python -m pytest lyric/tests/test_interpreter.py -v

Write-Host ""
Write-Host "Running all lyric tests..." -ForegroundColor Yellow
python -m pytest lyric/tests/ -v

Write-Host ""
Write-Host "Running root level tests..." -ForegroundColor Yellow
python -m pytest tests/ -v

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "All tests completed!" -ForegroundColor Green
