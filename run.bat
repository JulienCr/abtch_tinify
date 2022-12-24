@echo off
git pull
if not "%VIRTUAL_ENV%" == "" (
    python main.py %*
) else (
    pip install -e .
    python main.py %*
)
