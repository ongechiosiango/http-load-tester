"""Format and display load test results in the terminal."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from .metrics import Metrics

console = Console()


def print_report(metrics: Metrics, url: str, method: str) -> None:
    """Print a pretty report of the metrics to the terminal."""
    console.print()
    console.rule("[bold cyan]HTTP Load Test Report[/bold cyan]")
    console.print(f"[bold]Target:[/bold] {method} {url}\n")

    summary = Table(title="Summary", show_header=True, header_style="bold magenta")
    summary.add_column("Metric", style="cyan", no_wrap=True)
    summary.add_column("Value", style="green")
    summary.add_row("Total Requests", str(metrics.total_requests))
    summary.add_row("Successful (2xx/3xx)", str(metrics.successful))
    summary.add_row("Failed", str(metrics.failed))
    summary.add_row("Requests/sec (RPS)", f"{metrics.requests_per_second:.2f}")
    console.print(summary)

    latency = Table(title="Latency (ms)", show_header=True, header_style="bold magenta")
    latency.add_column("Metric", style="cyan", no_wrap=True)
    latency.add_column("Value", style="green")
    latency.add_row("Average", f"{metrics.avg_latency_ms:.2f}")
    latency.add_row("Min", f"{metrics.min_latency_ms:.2f}")
    latency.add_row("p50", f"{metrics.p50_latency_ms:.2f}")
    latency.add_row("p95", f"{metrics.p95_latency_ms:.2f}")
    latency.add_row("p99", f"{metrics.p99_latency_ms:.2f}")
    latency.add_row("Max", f"{metrics.max_latency_ms:.2f}")
    console.print(latency)

    if metrics.status_codes:
        codes = Table(title="Status Codes", show_header=True, header_style="bold magenta")
        codes.add_column("Code", style="cyan")
        codes.add_column("Count", style="green")
        for code, count in sorted(metrics.status_codes.items()):
            codes.add_row(str(code), str(count))
        console.print(codes)
