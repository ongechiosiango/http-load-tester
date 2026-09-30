"""Tests for the async load engine."""

import pytest

from http_load_tester.engine import run_load_test


@pytest.mark.anyio
async def test_run_load_test_basic():
    result = await run_load_test(
        url="https://httpbin.org/get",
        requests=5,
        concurrency=2,
    )
    assert len(result.results) == 5
    assert result.total_time_s > 0


@pytest.mark.anyio
async def test_invalid_url_records_error():
    result = await run_load_test(
        url="https://this-domain-does-not-exist-xyz.invalid",
        requests=2,
        concurrency=1,
        timeout=3.0,
    )
    assert all(r.error is not None for r in result.results)
