import json
import csv
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Union, Optional

class FinanceTracker:
    def __init__(self):
        """Initialize the Finance Tracker with data file."""
        self.file = "finance_data.json"
        self.max_attempts = 3
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file with validation."""
        if not os.path.exists(self.file):
            return {"transactions": [], "goals": []}
            
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
                
            # Validate data structure
            if not all(key in data for key in ["transactions", "goals"]):
                print("⚠️  Data file is corrupted. Creating a new one.")
                return {"transactions": [], "goals": []}
                
            # Validate transactions
            if not isinstance(data["transactions"], list):
                data["transactions"] = []
                
            # Validate goals
            if not isinstance(data["goals"], list):
                data["goals"] = []
                
            return data
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error loading data: {e}. Starting with empty data.")
            return {"transactions": [], "goals": []}
    
    def save_data(self) -> bool:
        """Save data to JSON file with backup and error handling."""
        if not self.data:
            print("⚠️  No data to save.")
            return False
            
        # Create backup
        backup_file = f"{self.file}.bak"
        if os.path.exists(self.file):
            try:
                import shutil
                shutil.copy2(self.file, backup_file)
            except Exception as e:
                print(f"⚠️  Could not create backup: {e}")
        
        # Save new data
        try:
            temp_file = f"{self.file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(self.data, f, indent=2)
                
            # Atomic write
            if os.path.exists(self.file):
                os.replace(temp_file, self.file)
            else:
                os.rename(temp_file, self.file)
                
            return True
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            # Try to restore from backup
            if os.path.exists(backup_file):
                try:
                    os.replace(backup_file, self.file)
                    print("⚠️  Restored from backup after save error.")
                except Exception as restore_error:
                    print(f"❌ Critical: Could not restore from backup: {restore_error}")
            return False
    
    def _validate_date(self, date_str: str) -> bool:
        """Validate date format and ensure it's not in the future."""
        try:
            input_date = datetime.strptime(date_str, "%Y-%m-%d")
            if input_date.date() > datetime.now().date():
                print("❌ Future dates are not allowed.")
                return False
            return True
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            return False

    def _get_valid_input(self, prompt: str, validation_func, error_msg: str, max_attempts: int = 3):
        """Generic input validation with retry logic."""
        for attempt in range(max_attempts):
            user_input = input(prompt).strip()
            if validation_func(user_input):
                return user_input
            print(f"❌ {error_msg} (Attempt {attempt + 1}/{max_attempts})")
        raise ValueError(f"Maximum attempts reached for input: {prompt}")

    def _validate_category(self, category: str) -> bool:
        """Validate category name (alphanumeric + spaces)."""
        return bool(re.match(r'^[a-zA-Z0-9\s]+$', category))

    def _validate_amount(self, amount_str: str) -> bool:
        """Validate amount is a positive number."""
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False

    def add_transaction(self):
        """Add a new transaction with validated inputs."""
        print("\n=== Add Transaction ===")
        
        # Get and validate transaction type
        t_type = ""
        while t_type not in ["income", "expense"]:
            t_type = input("Type (income/expense): ").lower().strip()
            if t_type not in ["income", "expense"]:
                print("❌ Invalid type. Please enter 'income' or 'expense'.")
        
        # Get and validate amount
        amount = 0.0
        while amount <= 0:
            try:
                amount = float(input("Amount: $").strip())
                if amount <= 0:
                    print("❌ Amount must be greater than 0.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Get and validate description
        desc = ""
        while not desc.strip():
            desc = input("Description: ").strip()
            if not desc:
                print("❌ Description cannot be empty.")
        
        # Get and validate category
        category = ""
        while not self._validate_category(category):
            category = input("Category: ").strip()
            if not self._validate_category(category):
                print("❌ Category can only contain letters, numbers, and spaces.")
        
        # Get and validate date
        date = ""
        while not date:
            date_input = input("Date (YYYY-MM-DD) or Enter for today: ").strip()
            date = date_input if date_input else datetime.now().strftime("%Y-%m-%d")
            if not self._validate_date(date):
                date = ""
        
        self.data["transactions"].append({
            "type": t_type, "amount": amount, "description": desc,
            "category": category, "date": date
        })
        self.save_data()
        print(f"✅ Added {t_type}: ${amount:.2f}")
    
    def view_summary(self):
        if not self.data["transactions"]:
            print("No transactions yet.")
            return
        
        # Current month
        current_month = datetime.now().strftime("%Y-%m")
        month_trans = [t for t in self.data["transactions"] if t["date"].startswith(current_month)]
        
        income = sum(t["amount"] for t in month_trans if t["type"] == "income")
        expenses = sum(t["amount"] for t in month_trans if t["type"] == "expense")
        
        print(f"\n=== {datetime.now().strftime('%B %Y')} Summary ===")
        print(f"Income:  ${income:.2f}")
        print(f"Expenses: ${expenses:.2f}")
        print(f"Net:     ${(income - expenses):.2f}")
        
        # Category breakdown
        print(f"\n--- Expenses by Category ---")
        cat_totals = defaultdict(float)
        for t in month_trans:
            if t["type"] == "expense":
                cat_totals[t["category"]] += t["amount"]
        
        for cat, amount in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
            percent = (amount / expenses * 100) if expenses > 0 else 0
            print(f"{cat}: ${amount:.2f} ({percent:.0f}%)")
        
        # Recent transactions
        print(f"\n--- Recent Transactions ---")
        recent = sorted(self.data["transactions"], key=lambda x: x["date"], reverse=True)[:5]
        for t in recent:
            sign = "+" if t["type"] == "income" else "-"
            print(f"{t['date']} {sign}${t['amount']:.2f} - {t['description']}")
    
    def add_goal(self):
        """Add or update a savings goal with validated inputs."""
        print("\n=== Add/Update Savings Goal ===")
        
        # Get and validate goal name
        name = ""
        while not name.strip():
            name = input("Goal name: ").strip()
            if not name:
                print("❌ Goal name cannot be empty.")
        
        # Get and validate target amount
        target = 0.0
        while target <= 0:
            try:
                target_input = input("Target amount: $").strip()
                if not target_input:
                    print("❌ Target amount is required.")
                    continue
                target = float(target_input)
                if target <= 0:
                    print("❌ Target must be greater than 0.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Get and validate current amount
        current = -1
        while current < 0:
            current_input = input("Current amount (default: 0): $").strip() or "0"
            try:
                current = float(current_input)
                if current < 0:
                    print("❌ Current amount cannot be negative.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Update existing or add new
        for goal in self.data["goals"]:
            if goal["name"] == name:
                goal["target"] = target
                goal["current"] = current
                self.save_data()
                print(f"✅ Updated goal: {name}")
                return
        
        self.data["goals"].append({"name": name, "target": target, "current": current})
        self.save_data()
        print(f"✅ Added goal: {name}")
    
    def view_goals(self):
        if not self.data["goals"]:
            print("No savings goals yet.")
            return
        
        print("\n=== Savings Goals ===")
        for goal in self.data["goals"]:
            progress = (goal["current"] / goal["target"]) * 100
            bar_length = 15
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"\n{goal['name']}")
            print(f"[{bar}] {progress:.0f}% - ${goal['current']:.0f}/${goal['target']:.0f}")
            print(f"Remaining: ${goal['target'] - goal['current']:.0f}")
    
    def export_csv(self):
        filename = f"finance_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Category", "Description", "Amount"])
            for t in self.data["transactions"]:
                writer.writerow([t['date'], t['type'], t['category'], t['description'], t['amount']])
        print(f"✅ Exported to {filename}")
    
    def run(self):
        print("💰 Personal Finance Tracker")
        
        while True:
            print("\n1. Add Transaction")
            print("2. View Summary")
            print("3. Add Goal")
            print("4. View Goals")
            print("5. Export CSV")
            print("6. Exit")
            
            choice = input("Choice (1-6): ").strip()
            
            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_summary()
            elif choice == "3":
                self.add_goal()
            elif choice == "4":
                self.view_goals()
            elif choice == "5":
                self.export_csv()
            elif choice == "6":
                print("Goodbye! 💰")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    FinanceTracker().run()
