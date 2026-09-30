"""Compute metrics from raw load test results."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from .engine import LoadTestResult


@dataclass
class Metrics:
    """Aggregated performance metrics."""

    total_requests: int
    successful: int
    failed: int
    requests_per_second: float
    avg_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    status_codes: dict


def _percentile(sorted_values, pct):
    """Return the given percentile from a sorted list of values."""
    if not sorted_values:
        return 0.0
    k = (len(sorted_values) - 1) * pct
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return sorted_values[f]
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)


def compute_metrics(result: LoadTestResult) -> Metrics:
    """Compute aggregated metrics from a LoadTestResult."""
    latencies = sorted(r.latency_ms for r in result.results)
    successful = sum(1 for r in result.results if r.status_code and 200 <= r.status_code < 400)
    failed = len(result.results) - successful

    status_codes = {}
    for r in result.results:
        if r.status_code is not None:
            status_codes[r.status_code] = status_codes.get(r.status_code, 0) + 1

    rps = len(result.results) / result.total_time_s if result.total_time_s > 0 else 0.0

    return Metrics(
        total_requests=len(result.results),
        successful=successful,
        failed=failed,
        requests_per_second=round(rps, 2),
        avg_latency_ms=round(mean(latencies), 2) if latencies else 0.0,
        min_latency_ms=round(latencies[0], 2) if latencies else 0.0,
        max_latency_ms=round(latencies[-1], 2) if latencies else 0.0,
        p50_latency_ms=round(_percentile(latencies, 0.50), 2),
        p95_latency_ms=round(_percentile(latencies, 0.95), 2),
        p99_latency_ms=round(_percentile(latencies, 0.99), 2),
        status_codes=status_codes,
    )
