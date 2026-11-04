#!/usr/bin/env python3
import subprocess
import statistics

# Hämta icke-merge commits som rör src/flask
cmd = ['git', 'log', '--no-merges', '--pretty=format:%H', '--', 'src/flask/']
result = subprocess.run(cmd, capture_output=True, text=True)
commits = result.stdout.strip().splitlines()
print(f"Non-merge commits touching src/flask: {len(commits)}")

sizes = []
for i, commit in enumerate(commits):
    if i % 100 == 0:
        print(f"Processing {i}/{len(commits)}...")
    cmd = ['git', 'show', '--numstat', '--format=', commit, '--', 'src/flask/']
    res = subprocess.run(cmd, capture_output=True, text=True)
    total = 0
    for line in res.stdout.splitlines():
        parts = line.split('\t')
        if len(parts) >= 2 and parts[0] != '-' and parts[1] != '-':
            try:
                total += int(parts[0]) + int(parts[1])
            except ValueError:
                pass
    if total > 0:
        sizes.append(total)

print(f"\nCommits with actual changes: {len(sizes)}")
print(f"Median lines changed: {statistics.median(sizes)}")
print(f"Mean:   {statistics.mean(sizes):.1f}")
print(f"Min:    {min(sizes)}")
print(f"Max:    {max(sizes)}")
sizes_sorted = sorted(sizes)
print(f"P25:    {sizes_sorted[len(sizes_sorted)//4]}")
print(f"P75:    {sizes_sorted[3*len(sizes_sorted)//4]}")
