"""Command-line interface for HTTP Load Tester."""

from __future__ import annotations

import argparse
import asyncio
import sys

from .engine import run_load_test
from .metrics import compute_metrics
from .reporter import print_report


def build_parser():
    parser = argparse.ArgumentParser(
        prog="http-load-tester",
        description="A blazing-fast asynchronous HTTP load testing tool.",
    )
    parser.add_argument("--url", "-u", required=True, help="Target URL to test.")
    parser.add_argument("--requests", "-n", type=int, default=100,
                        help="Total number of requests to fire (default: 100).")
    parser.add_argument("--concurrency", "-c", type=int, default=10,
                        help="Number of concurrent requests (default: 10).")
    parser.add_argument("--method", "-m", default="GET",
                        help="HTTP method to use (default: GET).")
    parser.add_argument("--timeout", "-t", type=float, default=10.0,
                        help="Request timeout in seconds (default: 10).")
    return parser


def main():
    args = build_parser().parse_args()

    try:
        result = asyncio.run(
            run_load_test(
                url=args.url,
                requests=args.requests,
                concurrency=args.concurrency,
                method=args.method.upper(),
                timeout=args.timeout,
            )
        )
    except KeyboardInterrupt:
        print("\nAborted by user.", file=sys.stderr)
        return 130

    metrics = compute_metrics(result)
    print_report(metrics, args.url, args.method.upper())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
