# Minesweeper AI Solver

An AI agent that automatically solves Minesweeper boards using
logical inference and probability-based decision making.

---

## Overview
This project implements an autonomous Minesweeper solver that combines
deterministic logical rules with probabilistic reasoning to select
safe moves and identify mine locations.

The project was originally developed as part of a university AI course.
All logic and decision-making components were implemented by me and
the code has been reorganized and refined for portfolio presentation.

---

## Key Ideas
- Identifies guaranteed mines and safe cells using deterministic rules
- Estimates mine probabilities for uncertain cells
- Selects actions based on minimum-risk heuristics
- Balances logical inference with probabilistic decision making

---

## Tech Stack
- **Language**: Python
- **Topics**: AI reasoning, constraint satisfaction, probability heuristics

---


## Project Structure
```text
.
├── Main.py           # Entry point
├── World.py          # Game environment and board state
├── AI.py             # Base AI interface
├── MainAI.py         # Primary AI implementation
├── MainAI_variant.py # Second Algorithm of Primary AI implementation
├── RandomAI.py       # Baseline random agent
├── ManualAI.py       # Human-controlled agent
└── Action.py         # Action definitions

  
