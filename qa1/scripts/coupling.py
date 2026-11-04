#!/usr/bin/env python3
import subprocess
from collections import defaultdict

modules = {
    'base': [
        'src/flask/__init__.py', 'src/flask/__main__.py', 'src/flask/app.py',
        'src/flask/blueprints.py', 'src/flask/config.py', 'src/flask/views.py',
        'src/flask/sansio/app.py', 'src/flask/sansio/blueprints.py', 'src/flask/sansio/scaffold.py',
    ],
    'request': ['src/flask/wrappers.py', 'src/flask/ctx.py', 'src/flask/helpers.py'],
    'req_helpers': [
        'src/flask/globals.py', 'src/flask/sessions.py', 'src/flask/signals.py',
        'src/flask/templating.py', 'src/flask/json/__init__.py',
        'src/flask/json/provider.py', 'src/flask/json/tag.py',
    ],
    'dev_helpers': [
        'src/flask/debughelpers.py', 'src/flask/typing.py', 'src/flask/logging.py',
        'src/flask/testing.py', 'src/flask/cli.py',
    ],
}

file_to_module = {f: mod for mod, files in modules.items() for f in files}

cmd = ['git', 'log', '--pretty=format:COMMIT %H', '--name-only', '--', 'src/flask/']
result = subprocess.run(cmd, capture_output=True, text=True)
lines = result.stdout.splitlines()

commits = []
current_commit = None
current_files = set()

for line in lines:
    if line.startswith('COMMIT '):
        if current_commit and current_files:
            commits.append((current_commit, current_files))
        current_commit = line.split()[1]
        current_files = set()
    elif line.strip() in file_to_module:
        current_files.add(line.strip())

if current_commit and current_files:
    commits.append((current_commit, current_files))

print(f"Total commits touching relevant files: {len(commits)}")

coupled = 0
pairs = defaultdict(int)
single = 0
multi_dist = defaultdict(int)

for commit, files in commits:
    mods = {file_to_module[f] for f in files}
    if len(mods) > 1:
        coupled += 1
        multi_dist[len(mods)] += 1
        mod_list = sorted(mods)
        for i in range(len(mod_list)):
            for j in range(i + 1, len(mod_list)):
                pairs[(mod_list[i], mod_list[j])] += 1
    else:
        single += 1

print(f"Single-module commits: {single}")
print(f"Multi-module commits:  {coupled} ({coupled/len(commits)*100:.1f}%)")
print("\nCross-module pairs:")
for pair, count in sorted(pairs.items(), key=lambda x: -x[1]):
    print(f"  {pair[0]} ↔ {pair[1]}: {count}")
print("\nModules per multi-commit:")
for n, c in sorted(multi_dist.items()):
    print(f"  {n} modules: {c}")
