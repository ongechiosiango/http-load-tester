# HTTP Load Tester

[![CI](https://github.com/ongechiosiango/http-load-tester/actions/workflows/ci.yml/badge.svg)](https://github.com/ongechiosiango/http-load-tester/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A blazing-fast, asynchronous HTTP load testing tool written in pure Python.

## Features

- Async engine powered by httpx + asyncio for high concurrency.
- Rich metrics: RPS, avg/min/max, p50/p95/p99 latency.
- Status code distribution.
- Beautiful terminal output using rich.
- Modern packaging with pyproject.toml and a src/ layout.

## Installation

From source:

    git clone git@github.com:ongechiosiango/http-load-tester.git
    cd http-load-tester
    python3 -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"

## Usage

    http-load-tester --url https://example.com --requests 500 --concurrency 20

### All options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| --url | -u | required | Target URL |
| --requests | -n | 100 | Total requests |
| --concurrency | -c | 10 | Concurrent requests |
| --method | -m | GET | HTTP method |
| --timeout | -t | 10.0 | Timeout (seconds) |

See docs/usage.md for more examples.

## Development

    pip install -e ".[dev]"
    pytest -v

## Contributing

See CONTRIBUTING.md.

## License

MIT - see LICENSE.
