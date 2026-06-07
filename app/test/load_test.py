"""
Bore Connect 接口压测工具
用法:
    python -m app.test.load_test                    # 默认: 10并发, 30秒
    python -m app.test.load_test --url http://127.0.0.1:8000 --concurrency 20 --duration 60
    python -m app.test.load_test --quick             # 快速测试: 5并发, 10秒
"""
import argparse
import json
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed  # noqa
from datetime import datetime

import requests

# ── 配置 ──
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_CONCURRENCY = 10
DEFAULT_DURATION = 30  # 秒


class LatencyStats:
    """线程安全的延迟统计"""
    def __init__(self):
        self._lock = threading.Lock()
        self._samples: list[float] = []

    def record(self, elapsed: float):
        with self._lock:
            self._samples.append(elapsed)

    @property
    def samples(self) -> list[float]:
        with self._lock:
            return list(self._samples)


class BenchmarkResult:
    def __init__(self, name: str):
        self.name = name
        self.stats = LatencyStats()
        self.success = 0
        self.fail = 0
        self.bytes_received = 0
        self._lock = threading.Lock()

    def record_success(self, elapsed: float, size: int):
        self.stats.record(elapsed)
        with self._lock:
            self.success += 1
            self.bytes_received += size

    def record_fail(self):
        with self._lock:
            self.fail += 1

    def summary(self) -> dict:
        samples = sorted(self.stats.samples)
        total = self.success + self.fail
        if not samples:
            return {"name": self.name, "total": 0, "qps": 0, "error_rate": 0}

        n = len(samples)
        return {
            "name": self.name,
            "total": total,
            "success": self.success,
            "fail": self.fail,
            "qps": round(self.success / max(samples[-1] if len(samples) > 1 else 1, 1), 1),
            "error_rate": round(self.fail / total * 100, 1) if total else 0,
            "avg_ms": round(sum(samples) / n * 1000, 1),
            "p50_ms": round(samples[int(n * 0.50)] * 1000, 1),
            "p90_ms": round(samples[int(n * 0.90)] * 1000, 1),
            "p95_ms": round(samples[int(n * 0.95)] * 1000, 1),
            "p99_ms": round(samples[int(n * 0.99)] * 1000, 1),
            "min_ms": round(samples[0] * 1000, 1),
            "max_ms": round(samples[-1] * 1000, 1),
            "bytes_mb": round(self.bytes_received / 1024 / 1024, 2),
        }


# ── 测试用例定义 ──
ENDPOINTS = [
    {"name": "Health Check", "method": "GET", "path": "/api/health"},
    {"name": "Device Status", "method": "GET", "path": "/api/overview/device-status"},
    {"name": "Subsystems", "method": "GET", "path": "/api/overview/subsystems"},
    {"name": "Trend (24h)", "method": "GET", "path": "/api/overview/trend-data?range=24h"},
    {"name": "Trend (7d)", "method": "GET", "path": "/api/overview/trend-data?range=7d"},
    {"name": "Alarms", "method": "GET", "path": "/api/overview/alarms"},
    {"name": "Diagnosis", "method": "GET", "path": "/api/diagnosis/status"},
    {"name": "Motor Currents", "method": "GET", "path": "/api/analysis/motor-currents"},
]


def _hit_endpoint(base_url: str, ep: dict, timeout: int = 30) -> tuple[bool, float, int]:
    """返回 (是否成功, 耗时秒, 响应体大小)"""
    url = base_url + ep["path"]
    try:
        resp = requests.request(
            method=ep["method"],
            url=url,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )
        elapsed = resp.elapsed.total_seconds()
        size = len(resp.content)
        return resp.status_code < 500, elapsed, size
    except Exception:
        return False, 0, 0


def warmup(base_url: str):
    """预热：每个接口先请求一次"""
    print("Warming up...", end=" ", flush=True)
    for ep in ENDPOINTS:
        try:
            _hit_endpoint(base_url, ep, timeout=10)
            print(".", end="", flush=True)
        except Exception:
            print("x", end="", flush=True)
    print(" 完成\n")


def run_benchmark(
    base_url: str,
    concurrency: int = DEFAULT_CONCURRENCY,
    duration: int = DEFAULT_DURATION,
) -> dict:
    """执行全接口压测"""
    # 按端点分组统计
    results = {ep["name"]: BenchmarkResult(ep["name"]) for ep in ENDPOINTS}
    overall = BenchmarkResult("Overall")

    stop_event = threading.Event()
    endpoint_cycle = ENDPOINTS.copy()

    def worker():
        idx = 0
        while not stop_event.is_set():
            ep = endpoint_cycle[idx % len(endpoint_cycle)]
            idx += 1
            success, elapsed, size = _hit_endpoint(base_url, ep)
            results[ep["name"]].record_success(elapsed, size) if success else results[ep["name"]].record_fail()
            overall.record_success(elapsed, size) if success else overall.record_fail()

    # 启动并发线程
    threads = []
    start = time.time()
    for _ in range(concurrency):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    # 打印进度
    last_report = start
    last_success = 0
    while time.time() - start < duration:
        time.sleep(2)
        now = time.time()
        current_success = overall.success
        instant_qps = (current_success - last_success) / max(now - last_report, 0.1)
        elapsed = now - start
        print(f"\r[{elapsed:.0f}s/{duration}s] Requests: {current_success} | Instant QPS: {instant_qps:.1f} | Concurrency: {concurrency}", end="", flush=True)
        last_report = now
        last_success = current_success

    stop_event.set()
    for t in threads:
        t.join(timeout=3)

    total_elapsed = time.time() - start
    print(f"\r[OK] Load test complete, total time: {total_elapsed:.1f}s\n")

    return {
        "results": [r.summary() for r in results.values()],
        "overall": overall.summary(),
        "config": {
            "base_url": base_url,
            "concurrency": concurrency,
            "duration": duration,
            "total_elapsed": round(total_elapsed, 1),
        },
    }


def print_report(data: dict):
    """打印压测报告"""
    cfg = data["config"]
    overall = data["overall"]

    print("=" * 90)
    print(f"  Bore Connect API Benchmark Report")
    print(f"  Target: {cfg['base_url']}  |  Concurrency: {cfg['concurrency']}  |  Duration: {cfg['duration']}s")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print(f"  Requests: {overall['total']}  |  Success: {overall['success']}  |  Fail: {overall['fail']}  |  Error Rate: {overall['error_rate']}%")
    print(f"  Traffic: {overall['bytes_mb']} MB")
    print(f"  Average QPS: {overall['total'] / cfg['total_elapsed']:.1f}")
    print(f"  Avg Latency: {overall['avg_ms']}ms  |  P50: {overall['p50_ms']}ms  |  P90: {overall['p90_ms']}ms  |  P95: {overall['p95_ms']}ms  |  P99: {overall['p99_ms']}ms")
    print("-" * 90)
    print(f"  {'Endpoint':<20} {'Succ':>6} {'Fail':>6} {'QPS':>8} {'Avg':>8} {'P50':>8} {'P90':>8} {'P95':>8} {'P99':>8}")
    print("-" * 90)

    for r in data["results"]:
        print(
            f"  {r['name']:<20} {r['success']:>6} {r['fail']:>6} "
            f"{r['qps']:>8.1f} {r['avg_ms']:>7}ms {r['p50_ms']:>7}ms "
            f"{r['p90_ms']:>7}ms {r['p95_ms']:>7}ms {r['p99_ms']:>7}ms"
        )

    print("=" * 90)

    # Save JSON report
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"benchmark_{timestamp}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [Report] JSON saved to: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Bore Connect 接口压测")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="目标地址")
    parser.add_argument("-c", "--concurrency", type=int, default=DEFAULT_CONCURRENCY, help="并发数")
    parser.add_argument("-d", "--duration", type=int, default=DEFAULT_DURATION, help="测试时长(秒)")
    parser.add_argument("--quick", action="store_true", help="快速测试 (5并发/10秒)")
    parser.add_argument("--warmup", action="store_true", default=True, help="预热 (默认开启)")
    parser.add_argument("--no-warmup", action="store_false", dest="warmup", help="跳过预热")
    args = parser.parse_args()

    if args.quick:
        args.concurrency = 5
        args.duration = 10

    print(f"\n=== Bore Connect Load Test ===")
    print(f"   Target: {args.url}  Concurrency: {args.concurrency}  Duration: {args.duration}s\n")

    # 健康检查
    try:
        r = requests.get(f"{args.url}/api/health", timeout=5)
        if r.status_code != 200:
            print(f"[FAIL] Service unreachable: {args.url}/api/health returned {r.status_code}")
            sys.exit(1)
        print(f"[OK] Service reachable: {args.url}")
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] Cannot connect to {args.url}, please ensure the server is running")
        sys.exit(1)

    if args.warmup:
        warmup(args.url)

    data = run_benchmark(args.url, args.concurrency, args.duration)
    print_report(data)


if __name__ == "__main__":
    main()
