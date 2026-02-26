# 📋 Freelance Order Tracker

A simple CLI tool to track freelance orders, manage clients, and calculate income.

## Features

- ✅ Add new orders with client name, amount, and status
- 📋 View all orders in a formatted table
- 💰 Calculate total and completed income
- ✏️ Edit any order (name, amount, status)
- 🔄 Mark orders as completed with one click
- 🗑️ Reset all data with confirmation prompt
- 💾 Persistent storage via JSON (data saved between sessions)

## Usage

```bash
python tracker.py
```

## Menu Options

```
1. Add order
2. Show all orders
3. Show income summary
4. Edit order
5. Mark order as completed
6. Reset all data
7. Exit
```

## Tech Stack

- Python 3.12+
- Built-in modules only: `json`, `os`, `datetime`
- No external dependencies required
