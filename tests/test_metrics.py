"""Tests for the metrics computation."""

from http_load_tester.engine import LoadTestResult, RequestResult
from http_load_tester.metrics import compute_metrics


def test_compute_metrics_basic():
    result = LoadTestResult(
        results=[
            RequestResult(status_code=200, latency_ms=100.0),
            RequestResult(status_code=200, latency_ms=200.0),
            RequestResult(status_code=500, latency_ms=300.0),
            RequestResult(latency_ms=400.0, error="timeout"),
        ],
        total_time_s=2.0,
    )
    metrics = compute_metrics(result)

    assert metrics.total_requests == 4
    assert metrics.successful == 2
    assert metrics.failed == 2
    assert metrics.requests_per_second == 2.0
    assert metrics.min_latency_ms == 100.0
    assert metrics.max_latency_ms == 400.0
    assert metrics.status_codes == {200: 2, 500: 1}


def test_compute_metrics_empty():
    result = LoadTestResult(results=[], total_time_s=0.0)
    metrics = compute_metrics(result)

    assert metrics.total_requests == 0
    assert metrics.avg_latency_ms == 0.0
    assert metrics.requests_per_second == 0.0
