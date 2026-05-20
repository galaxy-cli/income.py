# Pay and Budgeting Tool

A robust, highly interactive command-line application written in Python to help individuals convert, split, and allocate their pay dynamically. Built to replace vague financial assumptions with precise metrics, the tool routes configurations based entirely on your exact employment structure (Wage vs. Salary).

## Features

- **Adaptive Employment Routing**: Intelligently alters its logical flow depending on whether you earn an hourly wage or a rigid annual salary.
- **Context-Aware Dynamic Help**: Typing `?` inside any prompt generates an immediate visual box displaying formatting patterns, real-world baseline examples, and allowed percent/integer boundary rules.
- **Pew Research Methodology**: Calibrates economic class tiering matrices against strict Pew parameters (<66% for Lower Class, 67%+ for Middle, and 200%+ for Upper Class entry benchmarks).
- **Flexible Work Week Conversions**: Offers a dedicated `--hourly-days` flag to redefine custom working schedules instead of locking calculators to standard 5-day baselines.
- **No Silently Mutated Data**: Stripped of hidden truncation rules, putting clean, precise financial metrics directly back in your control.

---

## Usage & Flags

You can run individual specialized evaluation blocks using dedicated CLI arguments, or launch the interactive master program suite using the global `--all` runner.

### Global Module Execution
```bash
python3 pay_tool.py --all
```

### Targeted Command Flags
```bash
# Evaluate wage structures and salary breakdown mechanics
python3 pay_tool.py --pay-metrics

# Evaluate roommate housing split percentages and balance reserves 
python3 pay_tool.py --monthly-rent

# Evaluate economic baseline class tier thresholds via Pew metrics
python3 pay_tool.py --pay-bracket

# Run investment allocation waterfalls against gross-to-net pay
python3 pay_tool.py --investment
```

### Custom Work Schedules
Redefine structural salary breakdowns to hours by setting exact days worked in a standard week (Default baseline is `5.0`):
```bash
python3 pay_tool.py --pay-metrics --hourly-days 4.5
```

---

## Input Syntax Examples

When prompted for values inside the utility framework, you can type plain integers or use clean shorthand formatting tricks:

- **Shorthand Scale**: Entering `5k/mo` automatically processes as `$5,000.00` per month.
- **Time Frameworks**: Entering `120k/yr` scales calculations across annual parameters automatically.
- **Percentages**: Entering `80` dynamically evaluates calculations relative to an exact `80%` net footprint.

---

## Requirements

- Python 3.10 or newer (uses explicit type hinting syntax like `float | None`).
- Zero external package dependencies. Runs natively out of the box using built-in system modules (`argparse`, `sys`, `re`).
