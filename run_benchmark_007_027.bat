@echo off
REM Run the benchmark for problems 007..027 (inclusive).
REM Does NOT wipe the output dir, because arguments are passed (partial run).
REM Run this from the project root (the folder containing run_benchmark.py).

cd /d "%~dp0"

python run_benchmark.py ^
  problem_007 problem_008 problem_009 problem_010 problem_011 ^
  problem_012 problem_013 problem_014 problem_015 problem_016 ^
  problem_017 problem_018 problem_019 problem_020 problem_021 ^
  problem_022 problem_023 problem_024 problem_025 problem_026 ^
  problem_027

if errorlevel 1 (
  echo.
  echo [ERROR] run_benchmark.py exited with an error.
  pause
  exit /b 1
)

echo.
echo [OK] Problems 007-027 finished. Generating plots...
python -m src.metrics.plots

echo.
echo [DONE] Results in output\, metrics and plots in output\metrics\.
pause
