
# Unit Converter
# Convert between common units of length, weight, and volume.



def print_header():

    print("\n" + "=" * 50)
    print("📏  UNIT CONVERTER  📏")
    print("=" * 50 + "\n")


def length_converter():

    # Convert between length units.

    print("\n--- Length Converter ---")
    print("\nAvailable units:")
    print("1. Meters (m)")
    print("2. Kilometers (km)")
    print("3. Centimeters (cm)")
    print("4. Millimeters (mm)")
    print("5. Miles (mi)")
    print("6. Feet (ft)")
    print("7. Inches (in)")
    
    # Conversion rates to meters (base unit)
    to_meters = {
        '1': 1,           # meters
        '2': 1000,        # kilometers
        '3': 0.01,        # centimeters
        '4': 0.001,       # millimeters
        '5': 1609.34,     # miles
        '6': 0.3048,      # feet
        '7': 0.0254       # inches
    }
    
    unit_names = {
        '1': 'meters', '2': 'kilometers', '3': 'centimeters',
        '4': 'millimeters', '5': 'miles', '6': 'feet', '7': 'inches'
    }
    
    try:
        from_unit = input("\nConvert FROM (enter number): ").strip()
        to_unit = input("Convert TO (enter number): ").strip()
        
        if from_unit not in to_meters or to_unit not in to_meters:
            print("❌ Invalid unit selection!")
            return
        
        value = float(input(f"\nEnter value in {unit_names[from_unit]}: "))
        
        # Convert to meters first- then to target unit
        in_meters = value * to_meters[from_unit]
        result = in_meters / to_meters[to_unit]
        
        print(f"\n✅ {value} {unit_names[from_unit]} = {result:.4f} {unit_names[to_unit]}")
        
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")


def weight_converter():

    """Convert between weight units."""
    
    print("\n--- Weight Converter ---")
    print("\nAvailable units:")
    print("1. Kilograms (kg)")
    print("2. Grams (g)")
    print("3. Milligrams (mg)")
    print("4. Pounds (lb)")
    print("5. Ounces (oz)")
    print("6. Tons (metric)")
    
    # Conversion rates to kilograms (base unit)
    to_kg = {
        '1': 1,           # kilograms
        '2': 0.001,       # grams
        '3': 0.000001,    # milligrams
        '4': 0.453592,    # pounds
        '5': 0.0283495,   # ounces
        '6': 1000         # metric tons
    }
    
    unit_names = {
        '1': 'kilograms', '2': 'grams', '3': 'milligrams',
        '4': 'pounds', '5': 'ounces', '6': 'metric tons'
    }
    
    try:
        from_unit = input("\nConvert FROM (enter number): ").strip()
        to_unit = input("Convert TO (enter number): ").strip()
        
        if from_unit not in to_kg or to_unit not in to_kg:
            print("❌ Invalid unit selection!")
            return
        
        value = float(input(f"\nEnter value in {unit_names[from_unit]}: "))
        
        # Convert to kg first- then to target unit
        in_kg = value * to_kg[from_unit]
        result = in_kg / to_kg[to_unit]
        
        print(f"\n✅ {value} {unit_names[from_unit]} = {result:.4f} {unit_names[to_unit]}")
        
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")


def volume_converter():

    # Convert between volume units.

    print("\n--- Volume Converter ---")
    print("\nAvailable units:")
    print("1. Liters (L)")
    print("2. Milliliters (mL)")
    print("3. Cubic meters (m³)")
    print("4. Gallons (US)")
    print("5. Cups (US)")
    print("6. Fluid ounces (fl oz)")
    
    # Conversion rates to liters (base unit)
    to_liters = {
        '1': 1,           # liters
        '2': 0.001,       # milliliters
        '3': 1000,        # cubic meters
        '4': 3.78541,     # US gallons
        '5': 0.236588,    # US cups
        '6': 0.0295735    # US fluid ounces
    }
    
    unit_names = {
        '1': 'liters', '2': 'milliliters', '3': 'cubic meters',
        '4': 'gallons', '5': 'cups', '6': 'fluid ounces'
    }
    
    try:
        from_unit = input("\nConvert FROM (enter number): ").strip()
        to_unit = input("Convert TO (enter number): ").strip()
        
        if from_unit not in to_liters or to_unit not in to_liters:
            print("❌ Invalid unit selection!")
            return
        
        value = float(input(f"\nEnter value in {unit_names[from_unit]}: "))
        
        # Convert to liters first- then to target unit
        in_liters = value * to_liters[from_unit]
        result = in_liters / to_liters[to_unit]
        
        print(f"\n✅ {value} {unit_names[from_unit]} = {result:.4f} {unit_names[to_unit]}")
        
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")


def time_converter():

      # Convert between time units.

    print("\n--- Time Converter ---")
    print("\nAvailable units:")
    print("1. Second (s)")
    print("2. Minutes (min)")
    print("3. Hours (hr)")
    print("4. Days (day)")
    print("5. Weeks (wk)")
    print("6. Months (months)")
    print("7. Years (yr)")

      # Conversion rates to seconds (base unit)
    to_sec = {
        '1': 1,           # Seconds
        '2': 60,          # Minutes
        '3': 3600,        # Hours
        '4': 86400,       # Days
        '5': 604800,      # Weeks
        '6': 2592000,      # Months
        '7': 31536000     # Years

    }

    unit_names = {
        '1': 'second', '2': 'minutes', '3': 'hours',
        '4': 'days', '5': 'weeks', '6': 'months', '7': 'years'
    }
    
    try:
        from_unit = input("\nConvert FROM (enter number): ").strip()
        to_unit = input("Convert TO (enter number): ").strip()
        
        if from_unit not in to_sec or to_unit not in to_sec:
            print("❌ Invalid unit selection!")
            return
        
        value = float(input(f"\nEnter value in {unit_names[from_unit]}: "))
        
        # Convert to liters first- then to target unit
        in_sec = value * to_sec[from_unit]
        result = in_sec / to_sec[to_unit]
        
        print(f"\n✅ {value} {unit_names[from_unit]} = {result:.4f} {unit_names[to_unit]}")
        
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")
  

def main():

    while True:
        print_header()
        print("Select conversion type:")
        print("\n1. 📏 Length")
        print("2. ⚖️  Weight")
        print("3. 🧪 Volume")
        print("4. ⏰ Time")
        print("5. ❌ Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            length_converter()
        elif choice == '2':
            weight_converter()
        elif choice == '3':
            volume_converter()
        elif choice == '4':
            time_converter()    
        elif choice == '5':
            print("\n👋 Thanks for using Unit Converter! Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice! Please select 1-4.")
        
        if choice in ['1', '2', '3','4']:
            continue_choice = input("\nConvert another unit? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("\n👋 Thanks for using Unit Converter! Goodbye!\n")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!\n")