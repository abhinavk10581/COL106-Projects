
---

## 📌 4. Event Calendar Scheduler — `README.md`

```markdown
# 📅 Event Calendar Scheduler

A command-line event calendar manager supporting conflict detection, scheduling, free slot search, and JSON-based import/export.

## 🚀 Features

- Add/delete events with time and label
- Detect event conflicts using interval trees
- Find free time slots within a range
- Optimize schedules using greedy + dynamic programming
- Analyze event density
- Import/export events via JSON

## 🧠 DSA Concepts

- AVL-based Interval Tree for efficient O(log n) overlap checks
- Dynamic Programming for optimal event fitting
- Greedy algorithms for fast scheduling

## 💡 Example Commands

- Add Event  
  `add -> Enter time, duration, label`
- Show Conflicts  
  `conflicts`
- Find Free Slots  
  `free -> Enter time window and duration`
- Export/Import Events  
  `export`, `import`

## 🔧 Usage

```bash
python main.py
