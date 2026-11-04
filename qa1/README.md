# Flask Modifiability Analysis

This repository contains instructions for script usage to measure **modifiability** metrics for the web framework [Flask](https://github.com/pallets/flask) as part of a software architecture assignment.

The analysis is based on the four modules defined in our report (section 1.3) and was performed on commit `d086db856be187255b8ec61ef409357393020f32` (2026-10-07).

## Scripts

| Script | Metric | Description |
|--------|--------|-------------|
| `coupling.py` | Change coupling | Measures how often files from different modules are changed in the same commit |
| `commit_size.py` | Commit size | Calculates median and other statistics of lines changed per non-merge commit |
| `dependencies.py` | Dependencies | Counts import statements that cross module boundaries and detects circular dependencies |

## Prerequisites

- Python 3.8+
- Git
- A local clone of the Flask repository

## How to Run

### 1. Clone Flask

git clone https://github.com/pallets/flask.git
cd flask

### 2. Add the analysis scripts

Copy the three script files from this repository into the root of the cloned Flask folder.

### 3. Run the scripts

python coupling.py
python commit_size.py
python dependencies.py
