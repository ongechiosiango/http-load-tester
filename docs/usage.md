# Usage Guide

## Basic Example

    http-load-tester --url https://example.com --requests 200 --concurrency 20

## All Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| --url | -u | required | Target URL |
| --requests | -n | 100 | Total number of requests |
| --concurrency | -c | 10 | Concurrent requests |
| --method | -m | GET | HTTP method |
| --timeout | -t | 10.0 | Timeout in seconds |

## Examples

### POST endpoint

    http-load-tester -u https://api.example.com/submit -m POST -n 500 -c 50

### Slow, cautious test

    http-load-tester -u https://example.com -n 10 -c 1 -t 30
