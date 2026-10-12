import csv
import json
import re
from pathlib import Path
from statistics import median

data = Path(__file__).resolve().parents[1] / "data"
runs = [line.split("=", 1)[1] for line in (data / "environment.txt").read_text().splitlines() if line.startswith("run_")]
if len(runs) != 6 or len(set(runs)) != 6:
    raise ValueError("Expected six different runs")
results = {"on": [], "off": []}
units = {"B": 1 / 1048576, "KiB": 1 / 1024, "MiB": 1, "GiB": 1024}

print("Run, P95 (ms), Requests/s, Peak memory (MiB)")
for name in runs:
    folder = data / name
    with (folder / "locust_stats.csv").open() as file:
        stats = next(row for row in csv.DictReader(file) if row["Name"] == "Aggregated")
    if int(stats["Request Count"]) == 0 or int(stats["Failure Count"]) != 0:
        raise ValueError(f"Invalid requests in {name}")

    memory = []
    log = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", (folder / "memory.log").read_text())
    for line in log.splitlines():
        if line.strip():
            value = json.loads(line)["MemUsage"].split("/")[0].strip()
            amount, unit = re.fullmatch(r"([\d.]+)\s*([A-Za-z]+)", value).groups()
            memory.append(float(amount) * units[unit])

    values = (float(stats["95%"]), float(stats["Requests/s"]), max(memory))
    results[name.rsplit("-", 1)[1]].append(values)
    print(f"{name}, {values[0]:.0f}, {values[1]:.1f}, {values[2]:.2f}")
    if "WARNING" in (folder / "load.log").read_text():
        print(f"Warning recorded in {name}/load.log")

for cache, trials in results.items():
    if len(trials) != 3:
        raise ValueError(f"Expected three runs for cache {cache}")
    p95, rate, memory = [median(column) for column in zip(*trials)]
    print(f"Median {cache}, {p95:.0f}, {rate:.1f}, {memory:.2f}")
