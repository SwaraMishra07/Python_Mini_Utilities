import json
import urllib.request
from typing import Dict, Optional

class CurrencyConverter:
    def __init__(self):
        # Predefined exchange rates (as a fallback)
        self.rates = {
            'USD': 1.0,
            'INR': 90.0,    # Indian Rupee
            'EUR': 0.92,    # Euro
            'GBP': 0.79,    # British Pound
            'JPY': 147.8,   # Japanese Yen
            'AUD': 1.52,    # Australian Dollar
            'CAD': 1.35,    # Canadian Dollar
            'CNY': 7.18,    # Chinese Yuan
            'RUB': 88.5,    # Russian Ruble
            'SGD': 1.34,    # Singapore Dollar
        }
        self.update_rates()


    def update_rates(self) -> bool:
        """Try to fetch latest exchange rates from API."""
        try:
            with urllib.request.urlopen("https://api.exchangerate-api.com/v4/latest/USD") as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    self.rates = data.get('rates', self.rates)
                    return True
        except Exception as e:
            print(f"⚠️  Could not fetch latest rates: {e}. Using predefined rates.")
            return False
        return False


    def get_available_currencies(self) -> list:
        """Return sorted list of available currency codes."""
        return sorted(self.rates.keys())


    def convert(self, amount: float, from_curr: str, to_curr: str) -> Optional[float]:
        """Convert amount from one currency to another."""
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        
        if from_curr not in self.rates or to_curr not in self.rates:
            return None
            
        # Convert to USD first, then to target currency
        amount_in_usd = amount / self.rates[from_curr]
        return amount_in_usd * self.rates[to_curr]


def display_predefined_options(converter):
    """Display predefined conversion options."""
    print("\nPredefined Conversion Options:")
    options = [
        ("USD to INR", "USD", "INR"),
        ("EUR to USD", "EUR", "USD"),
        ("GBP to USD", "GBP", "USD"),
        ("USD to JPY", "USD", "JPY"),
        ("RUB to USD", "RUB", "USD"),
        ("Other (custom conversion)", "CUSTOM", "CUSTOM"),
    ]
    
    for i, (label, _, _) in enumerate(options, 1):
        print(f"{i}. {label}")
    
    return options


def get_user_amount() -> float:
    """Get and validate amount from user."""
    while True:
        try:
            amount = float(input("\nEnter amount to convert: ").strip())
            if amount <= 0:
                print("❌ Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("❌ Please enter a valid number.")


def get_currency(prompt: str, available_currencies: list) -> str:
    """Get and validate currency code from user."""
    while True:
        curr = input(prompt).strip().upper()
        if curr in available_currencies:
            return curr
        print(f"❌ Invalid currency. Available: {', '.join(available_currencies)}")


def main():
    print("💱 Currency Converter")
    converter = CurrencyConverter()
    
    while True:
        print("\n" + "="*50)
        print("💱 CURRENCY CONVERTER")
        print("="*50)
        
        options = display_predefined_options(converter)
        available_currencies = converter.get_available_currencies()
        
        try:
            choice = int(input("\nSelect an option (1-6): ").strip())
            if not 1 <= choice <= len(options):
                print("❌ Invalid choice. Please try again.")
                continue
                
            _, from_curr, to_curr = options[choice - 1]
            
            if from_curr == "CUSTOM":
                print(f"\nAvailable currencies: {', '.join(available_currencies)}")
                from_curr = get_currency("From currency (3-letter code): ", available_currencies)
                amount = get_user_amount()
                to_curr = get_currency("To currency (3-letter code): ", available_currencies)
            else:
                amount = get_user_amount()
                print(f"Converting {from_curr} to {to_curr}")
            
            result = converter.convert(amount, from_curr, to_curr)
            
            if result is not None:
                print(f"\n📊 {amount:.2f} {from_curr} = {result:.2f} {to_curr}")
                print(f"💱 1 {from_curr} = {1 / converter.rates[from_curr] * converter.rates[to_curr]:.4f} {to_curr}")
                print(f"💱 1 {to_curr} = {1 / (1 / converter.rates[from_curr] * converter.rates[to_curr]):.4f} {from_curr}")
            else:
                print("❌ Error: Could not perform conversion. Please check currency codes.")
            
        except (ValueError, IndexError):
            print("❌ Invalid input. Please try again.")
        
        if input("\nConvert another? (y/n): ").lower() != 'y':
            print("\nThank you for using the Currency Converter! 💰")
            break

if __name__ == "__main__":
    main()
