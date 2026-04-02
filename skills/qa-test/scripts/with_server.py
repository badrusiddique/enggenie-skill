#!/usr/bin/env python3
"""
Server lifecycle management for enggenie:qa-test.

Usage:
    python with_server.py --cmd "npm start" --port 3000 --test "pytest tests/e2e"

Starts a server, waits for it to be ready, runs tests, then stops the server.
Exit code matches the test command's exit code.
"""

import argparse
import subprocess
import sys
import time
import signal
import urllib.request
import urllib.error


def wait_for_server(port: int, timeout: int = 30, interval: float = 0.5) -> bool:
    """Poll until server responds on the given port."""
    url = f"http://localhost:{port}"
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except (urllib.error.URLError, ConnectionError, OSError):
            time.sleep(interval)
    return False


def main():
    parser = argparse.ArgumentParser(description="Run tests with a managed server lifecycle")
    parser.add_argument("--cmd", required=True, help="Command to start the server")
    parser.add_argument("--port", type=int, required=True, help="Port the server listens on")
    parser.add_argument("--test", required=True, help="Test command to run")
    parser.add_argument("--timeout", type=int, default=30, help="Seconds to wait for server (default: 30)")
    args = parser.parse_args()

    # Start server
    print(f"Starting server: {args.cmd}")
    server = subprocess.Popen(
        args.cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN),
    )

    try:
        # Wait for server to be ready
        print(f"Waiting for server on port {args.port} (timeout: {args.timeout}s)...")
        if not wait_for_server(args.port, timeout=args.timeout):
            print(f"Server did not start within {args.timeout}s", file=sys.stderr)
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()
            sys.exit(1)

        print(f"Server ready on port {args.port}")

        # Run tests
        print(f"Running tests: {args.test}")
        result = subprocess.run(args.test, shell=True)
        test_exit_code = result.returncode

    finally:
        # Stop server
        print("Stopping server...")
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()
        print("Server stopped.")

    sys.exit(test_exit_code)


if __name__ == "__main__":
    main()
