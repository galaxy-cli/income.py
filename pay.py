#!/usr/bin/env python3
import argparse
import sys
import re

# --- Utilities ---

def title(name: str) -> None:
    """Print a clean section header."""
    print(f"\n=== Calculate {name} ===")

def fmt(num: float, force_int: bool = False) -> str:
    """Format numbers with commas, stripping unnecessary decimal zeros."""
    if force_int:
        return f"{round(num):,}"
    return f"{num:,.2f}".rstrip('0').rstrip('.') if num % 1 != 0 else f"{num:,.0f}"

def parse_smart_value(user_input: str) -> tuple[float | None, str | None]:
    """Extract numeric value and time unit (mo/yr) from input string."""
    if not user_input: 
        return None, None
    
    user_input = str(user_input).strip().lower()
    unit = 'mo' if 'mo' in user_input else 'yr' if 'yr' in user_input else None
    multiplier = 1000 if 'k' in user_input else 1
    
    # Extract numbers and decimals
    clean_num_str = re.sub(r'[^\d.]', '', user_input.replace(',', ''))
    try:
        val = float(clean_num_str) * multiplier
        return val, unit
    except ValueError:
        return None, unit

def get_input(prompt: str, unit_label: str, allow_zero: bool = False, is_pct: bool = False, provided_val: str = None) -> float:
    """Safely get numeric input from CLI args or interactive prompt."""
    if provided_val is not None:
        val, _ = parse_smart_value(str(provided_val))
        if val is not None: 
            return val

    while True:
        user_input = input(f"{prompt} ({unit_label}) [? for help]: ").strip().lower()
        if user_input == '?':
            print("\n" + "="*45)
            print(f"  HELP: {prompt}")
            print("="*45)
            print(f"  Expected Unit : {unit_label}")
            print("  Format Rules  : Plain numbers or shorthand with 'k'")
            print("  Examples      : 4500, 4.5k, 250k")
            if is_pct:
                print("  Range Allowed : 0 to 100 percent")
            elif not allow_zero:
                print("  Range Allowed : Must be greater than 0")
            print("="*45 + "\n")
            continue
            
        val, _ = parse_smart_value(user_input)
        if val is None:
            print("[!] Invalid input. Please enter a valid number.")
            continue
        if not allow_zero and val <= 0:
            print("[!] Must be greater than zero.")
            continue
        if is_pct and not (0 <= val <= 100):
            print("[!] Percentage must be between 0 and 100.")
            continue
        return val

def get_any_pay(prompt: str, provided_val: str = None) -> tuple[float, float]:
    """Safely get pay and return both monthly and annual amounts."""
    if provided_val is not None:
        val, unit = parse_smart_value(str(provided_val))
        if val is not None and unit:
            return (val, val * 12) if unit == 'mo' else (val / 12, val)

    while True:
        user_input = input(f"{prompt} [? for help]: ").strip()
        if user_input == '?':
            print("\n" + "="*45)
            print(f"  HELP: {prompt}")
            print("="*45)
            print("  Format Rules  : Require an amount AND a time framework")
            print("  Valid Units   : Use '/mo' for month or '/yr' for year")
            print("  Shorthand     : 'k' multiplies by 1,000")
            print("  Examples      : 5k/mo, 4500/mo, 120k/yr, 95000/yr")
            print("="*45 + "\n")
            continue
            
        val, unit = parse_smart_value(user_input)
        if val is None:
            print("[!] Enter a valid numerical amount.")
            continue
            
        while not unit:
            choice = input(f"[!] You entered ${fmt(val)}. Is this for (1) /mo or (2) /yr? ").strip().lower()
            if choice in ['1', 'mo', '/mo']: 
                unit = 'mo'
            elif choice in ['2', 'yr', '/yr']: 
                unit = 'yr'
            else:
                print("[!] Invalid choice. Enter 1 or 2.")
                
        return (val, val * 12) if unit == 'mo' else (val / 12, val)

def print_result_table(rows: list, header: tuple = ("Item", "Amount", "% of Total"), hour_mode: bool = False) -> None:
    """Print results in a perfectly aligned, scannable table."""
    h1, h2, h3 = header
    print(f"\n{h1:<20} {h2:<12} {h3}")
    print("-" * 55)
    for label, val, pct in rows:
        if isinstance(pct, (int, float)):
            pct_str = f"{pct:>9.1f}%"
        elif pct is not None:
            pct_str = f"{pct:>10}"
        else:
            pct_str = ""
            
        is_hour = hour_mode and label == "Hour"
        val_str = f"${fmt(val, force_int=not is_hour):>10}" if isinstance(val, (int, float)) else f"{val:>11}"
        print(f"{label:<20} {val_str}  {pct_str}")

def get_pay_type() -> str:
    """Prompt user to identify if they are paid via wage or salary."""
    while True:
        choice = input("Are you paid by (1) Wage [Hourly] or (2) Salary? ").strip()
        if choice in ['1', 'wage', 'hourly']:
            return 'wage'
        if choice in ['2', 'salary']:
            return 'salary'
        print("[!] Invalid choice. Please enter 1 or 2.")

# --- Logic Modules ---

def calc_pay_routing(args: list = None, days_per_week: float = 5.0) -> None:
    """Routes pay calculation based on payment structure (Wage vs Salary)."""
    pay_type = get_pay_type()
    
    # Yearly conversion tracking variables
    weeks_per_year = 52
    hours_per_day = 8
    
    if pay_type == 'wage':
        title("Monthly Pay (Wage)")
        h = get_input("Wage", "hr", provided_val=args if (args and len(args) > 0) else None)
        w_hrs = get_input("Hours/wk", "wk", provided_val=args if (args and len(args) > 1) else None)
        
        w = h * w_hrs
        y = w * weeks_per_year
        m = y / 12
        
        rows = [
            ("Hour", h, None), 
            ("Week", w, None), 
            ("Month", m, None), 
            ("Year", y, None)
        ]
        print_result_table(rows, header=("Period", "Amount", ""), hour_mode=True)
        
    else:
        title("Yearly Pay (Salary)")
        _, y = get_any_pay("Annual Pay", args if args else None)
        
        total_hours = days_per_week * hours_per_day * weeks_per_year
        
        rows = [
            ("Hour", y / total_hours, None), 
            ("Week", y / weeks_per_year, None), 
            ("Month", y / 12, None), 
            ("Year", y, None)
        ]
        print_result_table(rows, header=("Period", "Amount", ""), hour_mode=True)

def calc_rent(args: list = None) -> None:
    title("Rent Split")
    rent = get_input("Total Rent", "mo", provided_val=args if (args and len(args) > 0) else None)
    inc = get_input("Monthly Pay", "mo", provided_val=args if (args and len(args) > 1) else None)
    roomies = int(get_input("Roommates", "ppl", True, provided_val=args if (args and len(args) > 2) else None))
    
    split = rent / (roomies + 1)
    rows = [
        ("Monthly Pay", inc, 100.0),
        (f"Rent ({'Solo' if roomies == 0 else 'Split'})", split, (split / inc) * 100),
        ("Remaining Balance", inc - split, (1 - split / inc) * 100)
    ]
    print_result_table(rows)

def calc_brackets(args: list = None) -> None:
    title("Class Bracket (Pew Research Methodology)")
    _, mid = get_any_pay("Middle class baseline pay", args if args else None)
    
    # Pew Research metrics: Lower (<67%), Middle (67%-200%), Upper (>200%)
    scales = [
        ("Lower Class", 0.66), 
        ("Middle Class Minimum", 0.67),
        ("Median Baseline", 1.00), 
        ("Upper Class Minimum", 2.00),
        ("High Earners", 3.00)
    ]
    rows = [(label, mid * mult, f"{mult:.2f}x") for label, mult in scales]
    print_result_table(rows, header=("Bracket", "Annual", "Mult"))

def calc_invest(args: list = None) -> None:
    title("Investment")
    mo_inc, _ = get_any_pay("Gross Pay", args if (args and len(args) > 0) else None)
    net_p = get_input("Net Pay", "%", is_pct=True, provided_val=args if (args and len(args) > 1) else None)
    
    net_mo = mo_inc * (net_p / 100)
    inv_p = get_input("Allocation", "%", is_pct=True, provided_val=args if (args and len(args) > 2) else None)
    
    rows = [
        ("Net Pay", net_mo, net_p),
        ("  Allocated", net_mo * (inv_p / 100), inv_p),
        ("  Remaining Balance", net_mo * ((100 - inv_p) / 100), 100.0 - inv_p)
    ]
    print_result_table(rows)

# --- CLI Setup ---

def main() -> None:
    actions = {
        "pay_metrics": calc_pay_routing,
        "monthly_rent": calc_rent,
        "pay_bracket": calc_brackets,
        "investment": calc_invest
    }

    parser = argparse.ArgumentParser(description="Pay and Budgeting Tool")
    
    parser.add_argument("--hourly-days", type=float, default=5.0, help="Set the number of days worked in a week (Default: 5.0)")
    
    for flag in actions.keys():
        parser.add_argument(f"--{flag.replace('_', '-')}", nargs='*', help=f"Calculate {flag.replace('_', ' ')}")
    parser.add_argument("--all", action="store_true", help="Run all calculation modules interactively")

    args = parser.parse_args()
    
    target_flags = [v for k, v in vars(args).items() if k != 'hourly_days' and k != 'all']
    if not args.all and all(v is None for v in target_flags):
        parser.print_help()
        return

    try:
        if args.all:
            for name, func in actions.items():
                prompt_str = f"Run {name.replace('_', ' ')}? [y/N]: "
                user_res = input(prompt_str).strip().split()
                if user_res and user_res[0].lower() == 'y':
                    extra_args = user_res[1:] if len(user_res) > 1 else None
                    if name == "pay_metrics":
                        func(extra_args, days_per_week=args.hourly_days)
                    else:
                        func(extra_args)
        else:
            for flag, func in actions.items():
                val = getattr(args, flag)
                if val is not None:
                    if flag == "pay_metrics":
                        func(val if len(val) > 0 else None, days_per_week=args.hourly_days)
                    else:
                        func(val if len(val) > 0 else None)
    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()