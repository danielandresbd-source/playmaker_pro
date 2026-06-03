# 🏈 PlayMaker Pro — Football Playbook Creator & Analyzer

> AB Final Project · Programming & Coding · MSMK University College 2025–2026

PlayMaker Pro is a CLI app that lets coaches and analysts create,
manage, and analyze American football playbooks and plays.
Think of it like a simpler, terminal-based version of tools like
Cloob or Tackle Football Playmarker — but built in Python!

---

## ✅ Features

| Feature | Status | Requirement |
|---------|--------|-------------|
| Import plays from CSV | ✅ Done | RF1 |
| Create/Edit/Delete playbooks & plays | ✅ Done | RF2 |
| Stats & analytics | ✅ Done | RF3 |
| Anomaly detection | ✅ Done | RF4 |
| Export reports to CSV | ✅ Done | RF5 |
| Automatic alerts | ✅ Done | RF6 |
| Trend prediction (moving average) | ✅ Done | RF7 |
| Interactive CLI menu | ✅ Done | RF8 |
| ASCII bar charts in console | ✅ Done | RF9 |
| Synthetic data simulator | ✅ Done | RF10 |

---

## 🚀 Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/playmaker_pro.git
cd playmaker_pro
```

### 2. Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify everything works
```bash
pytest tests/ -v
```

---

## 🎮 How to Use

```bash
# Start the interactive menu
python cli.py

# See all commands
python cli.py --help

# Quick examples
python cli.py playbooks list
python cli.py plays add --playbook pb_001 --name "HB Dive" --type run
python cli.py analyze stats
python cli.py simulator generate --plays 50
```

---

## 📁 Project Structure

```
playmaker_pro/
├── cli.py              # Main entry point, interactive menu (RF8)
├── data_importer.py    # CSV import & validation (RF1)
├── data_manager.py     # CRUD operations with JSON (RF2)
├── analyzer.py         # Stats, anomalies, predictions (RF3, RF4, RF7)
├── reporter.py         # CSV export + ASCII charts (RF5, RF9)
├── alerts.py           # Automatic alert engine (RF6)
├── simulator.py        # Synthetic data generator (RF10)
├── exceptions.py       # Custom exceptions
├── tests/              # All tests (pytest)
├── data/               # CSV files and JSON storage
│   └── exports/        # Generated reports go here
├── requirements.txt
└── .gitignore
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=term-missing

# Run only a specific module's tests
pytest tests/test_analyzer.py -v

# Run performance test
pytest tests/test_performance.py -v
```

---

## 🏗️ Built With

- Python 3.10+
- pandas + numpy (data analysis)
- pytest + pytest-cov (testing)
- argparse (CLI interface)
- flake8 / black (code quality)

---

## 📝 Notes

> This project was built for the Programming & Coding course at MSMK University.
> The fictional client is **Madrid Bulldogs** (American football team) and
> the consultancy is **TechPlay Solutions**.
