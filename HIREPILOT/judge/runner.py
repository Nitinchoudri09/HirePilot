import subprocess
import tempfile
import os
import sys
import time
from pathlib import Path

# Demo config - modify for testing
RUN_TIMEOUT = 3  # seconds per test

def run_python_code(code: str, input_data: str, timeout=RUN_TIMEOUT):
    """
    Run user code in a subprocess. Returns (exit_code, stdout, stderr, time_taken).
    WARNING: This runs untrusted code without sandboxing. Use Docker/containers for production.
    """
    # create a temp dir per run
    with tempfile.TemporaryDirectory() as tmpdir:
        code_file = Path(tmpdir) / "solution.py"
        # Optionally, wrap code to prevent certain imports (basic)
        code_file.write_text(code, encoding='utf-8')

        start = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, str(code_file)],  # use current Python interpreter
                input=input_data.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout
            )
            end = time.time()
            return proc.returncode, proc.stdout.decode('utf-8'), proc.stderr.decode('utf-8'), end - start
        except subprocess.TimeoutExpired as e:
            return None, "", f"TimeLimitExceeded after {timeout}s", timeout
