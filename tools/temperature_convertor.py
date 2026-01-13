def celsius_to_fahrenheit(celsius):
    return round((celsius * 9 / 5) + 32, 2)


def fahrenheit_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 2)


def main():
    while True:
        print("\nTemperature Converter")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ")

        try:
            if choice == "1":
                celsius = float(input("Enter temperature in Celsius: "))
                print("Temperature in Fahrenheit:", celsius_to_fahrenheit(celsius))

            elif choice == "2":
                fahrenheit = float(input("Enter temperature in Fahrenheit: "))
                print("Temperature in Celsius:", fahrenheit_to_celsius(fahrenheit))

            elif choice == "3":
                print("Exiting Temperature Converter. Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1, 2, or 3.")

        except ValueError:
            print("Invalid input! Please enter numeric values only.")


if __name__ == "__main__":
    main()
