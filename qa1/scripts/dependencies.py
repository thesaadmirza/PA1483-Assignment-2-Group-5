#!/usr/bin/env python3
import ast
import os
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

def resolve_target(node, current_mod):
    if not isinstance(node, ast.ImportFrom):
        return None
    if node.level > 0 and node.module:
        # Relativa importer
        mod_name = node.module.split('.')[0]
        mapping = {
            'app': 'base', 'blueprints': 'base', 'config': 'base', 'views': 'base',
            'sansio': 'base',
            'wrappers': 'request', 'ctx': 'request', 'helpers': 'request',
            'globals': 'req_helpers', 'sessions': 'req_helpers', 'signals': 'req_helpers',
            'templating': 'req_helpers', 'json': 'req_helpers',
            'debughelpers': 'dev_helpers', 'typing': 'dev_helpers', 'logging': 'dev_helpers',
            'testing': 'dev_helpers', 'cli': 'dev_helpers',
        }
        return mapping.get(mod_name)
    elif node.module and node.module.startswith('flask.'):
        sub = node.module[6:].split('.')[0]
        mapping = {
            'app': 'base', 'blueprints': 'base', 'config': 'base', 'views': 'base',
            'sansio': 'base',
            'wrappers': 'request', 'ctx': 'request', 'helpers': 'request',
            'globals': 'req_helpers', 'sessions': 'req_helpers', 'signals': 'req_helpers',
            'templating': 'req_helpers', 'json': 'req_helpers',
            'debughelpers': 'dev_helpers', 'typing': 'dev_helpers', 'logging': 'dev_helpers',
            'testing': 'dev_helpers', 'cli': 'dev_helpers',
        }
        return mapping.get(sub)
    return None

import_counts = defaultdict(int)
deps = defaultdict(set)

for mod, files in modules.items():
    for fpath in files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except Exception:
                continue
        for node in ast.walk(tree):
            target = resolve_target(node, mod)
            if target and target != mod:
                import_counts[(mod, target)] += 1
                deps[mod].add(target)

print("Inter-module import counts:")
for (frm, to), cnt in sorted(import_counts.items(), key=lambda x: -x[1]):
    print(f"  {frm} → {to}: {cnt}")

print("\nCircular dependencies exist:", any(
    to in deps.get(frm, set()) and frm in deps.get(to, set())
    for frm, to in import_counts
))
