# ARC_GYM - Real Kaggle ARC Dataset

This directory contains JSON files for real Abstraction and Reasoning Corpus (ARC) tasks.

## Format

Each JSON file follows the official Kaggle ARC format:

```json
{
  "train": [
    {
      "input": [[grid_row_1], [grid_row_2], ...],
      "output": [[grid_row_1], [grid_row_2], ...]
    }
  ],
  "test": [
    {
      "input": [...],
      "output": [...]
    }
  ]
}
```

## Usage

Place ARC task JSON files in this directory with the task ID as filename (e.g., `25d8a9c8.json`).

The engine will automatically discover and include them in the curriculum via `get_arc_tasks()`.

## Current Tasks

- `25d8a9c8.json`: Color inversion task (mock data for verification)

## References

- Official ARC Repository: https://github.com/fchollet/ARC
- Kaggle Competition: https://www.kaggle.com/c/abstraction-and-reasoning-challenge
