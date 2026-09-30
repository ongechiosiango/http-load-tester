"""Core async engine that fires concurrent HTTP requests."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class RequestResult:
    """Result of a single HTTP request."""

    status_code: Optional[int] = None
    latency_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class LoadTestResult:
    """Aggregated result of a full load test run."""

    results: list = field(default_factory=list)
    total_time_s: float = 0.0


async def _fire_request(client, url, method="GET", semaphore=None):
    """Fire a single HTTP request and time it."""
    async def _do():
        start = time.perf_counter()
        try:
            response = await client.request(method, url)
            elapsed_ms = (time.perf_counter() - start) * 1000
            return RequestResult(status_code=response.status_code, latency_ms=elapsed_ms)
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return RequestResult(latency_ms=elapsed_ms, error=str(exc))

    if semaphore is not None:
        async with semaphore:
            return await _do()
    return await _do()


async def run_load_test(url, requests=100, concurrency=10, method="GET", timeout=10.0):
    """Run a full load test and return the aggregated result."""
    semaphore = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency)

    async with httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=True) as client:
        start = time.perf_counter()
        tasks = [_fire_request(client, url, method, semaphore) for _ in range(requests)]
        results = await asyncio.gather(*tasks)
        total_time = time.perf_counter() - start

    return LoadTestResult(results=list(results), total_time_s=total_time)
