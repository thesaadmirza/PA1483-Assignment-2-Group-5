# Measurement Results

Results from running the scripts on Flask commit `d086db856be187255b8ec61ef409357393020f32` (2026-10-07).

## Change Coupling (`coupling.py`)

Cross-module pairs:
base ↔ request: 58
base ↔ dev_helpers: 51
base ↔ req_helpers: 39
dev_helpers ↔ request: 32
req_helpers ↔ request: 31
dev_helpers ↔ req_helpers: 24Modules per multi-commit:
2 modules: 61
3 modules: 24
4 modules: 17

## Commit Size (`commit_size.py`)

Commits with actual changes: 411
Median lines changed: 10
Mean:   75.6
Min:    1
Max:    8161
P25:    3
P75:    41

## Dependencies (`dependencies.py`)

Inter-module import counts:
base → req_helpers: 40
base → request: 30
base → dev_helpers: 12
request → req_helpers: 11
req_helpers → request: 8
dev_helpers → base: 6
req_helpers → base: 5
dev_helpers → req_helpers: 4
dev_helpers → request: 3
request → dev_helpers: 1
request → base: 1
req_helpers → dev_helpers: 1
