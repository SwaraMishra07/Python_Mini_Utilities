#!/usr/bin/env python3
"""
Barcode Generator Tool
Generates various types of barcodes and saves them as images.
"""

import argparse
import sys
from datetime import datetime


class BarcodeGenerator:
    """Generate various types of barcodes."""

    def __init__(self):
        """Initialize the barcode generator."""
        self.supported_formats = {
            'EAN8': 'EAN-8 (8-digit European Article Number)',
            'EAN13': 'EAN-13 (13-digit European Article Number)',
            'UPCA': 'UPC-A (12-digit Universal Product Code)',
            'CODE39': 'Code 39 (alphanumeric barcode)',
            'CODE128': 'Code 128 (high-density alphanumeric)',
            'ISBN': 'ISBN (International Standard Book Number)',
            'ISSN': 'ISSN (International Standard Serial Number)',
        }

    def generate_barcode(self, data, barcode_type='CODE128', output_file=None, show_text=True):
        """
        Generate a barcode.

        Args:
            data (str): The data to encode in the barcode
            barcode_type (str): Type of barcode (EAN8, EAN13, CODE128, etc.)
            output_file (str): Path to save the barcode image
            show_text (bool): Whether to show the encoded text below the barcode

        Returns:
            str: Path to the generated barcode file
        """
        try:
            import barcode
            from barcode.writer import ImageWriter
        except ImportError:
            print("Error: python-barcode library not found.")
            print("Install it with: pip install python-barcode[pillow]")
            sys.exit(1)

        # Validate barcode type
        barcode_type_upper = barcode_type.upper().replace('-', '')
        if barcode_type_upper not in self.supported_formats:
            print(f"Error: Unsupported barcode type '{barcode_type}'")
            print(f"Supported types: {', '.join(self.supported_formats.keys())}")
            sys.exit(1)

        # Get the barcode class
        barcode_class = barcode.get_barcode_class(barcode_type_upper)

        # Validate data for the barcode type
        if not self._validate_data(data, barcode_type_upper):
            print(f"Error: Invalid data for {barcode_type} barcode")
            print(f"Requirements: {self._get_requirements(barcode_type_upper)}")
            sys.exit(1)

        # Generate the barcode
        generated_barcode = barcode_class(
            data,
            writer=ImageWriter() if output_file else None
        )

        # Default output filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"barcode_{barcode_type_upper}_{timestamp}.png"

        # Save the barcode
        if output_file:
            generated_barcode.save(
                output_file,
                options={
                    'module_width': 2,
                    'module_height': 30,
                    'font_size': 12,
                    'text_distance': 5,
                    'quiet_zone': 6.5,
                }
            )
            print(f"Barcode saved to: {output_file}")
            return output_file
        else:
            print("Error: Output file path required")
            sys.exit(1)

    def _validate_data(self, data, barcode_type):
        """
        Validate data for the barcode type.

        Args:
            data (str): The data to validate
            barcode_type (str): The type of barcode

        Returns:
            bool: True if valid, False otherwise
        """
        if barcode_type == 'EAN8':
            return data.isdigit() and len(data) == 8
        elif barcode_type == 'EAN13':
            return data.isdigit() and len(data) == 13
        elif barcode_type == 'UPCA':
            return data.isdigit() and len(data) == 12
        elif barcode_type in ['CODE39', 'CODE128', 'ISBN', 'ISSN']:
            return len(data) > 0 and data.isprintable()
        return True

    def _get_requirements(self, barcode_type):
        """Get requirements for a barcode type."""
        requirements = {
            'EAN8': '8 digits (numbers only)',
            'EAN13': '13 digits (numbers only)',
            'UPCA': '12 digits (numbers only)',
            'CODE39': 'Uppercase letters, numbers, and special chars (- . $ / + %)',
            'CODE128': 'Any ASCII character (128 characters supported)',
            'ISBN': '10 or 13 digit ISBN (with or without hyphens)',
            'ISSN': '8 digits (format: XXXX-XXXX)',
        }
        return requirements.get(barcode_type, 'N/A')

    def list_formats(self):
        """List all supported barcode formats."""
        print("\nSupported Barcode Formats:")
        print("=" * 50)
        for fmt, description in self.supported_formats.items():
            print(f"{fmt:15} - {description}")
        print("=" * 50)


def print_banner():
    """Print the application banner."""
    print("=" * 60)
    print("          BARCODE GENERATOR")
    print("=" * 60)
    print()


def interactive_mode():
    """Run the barcode generator in interactive mode."""
    gen = BarcodeGenerator()

    print_banner()
    print("Welcome to the Barcode Generator!")
    print("This tool helps you generate various types of barcodes.")
    print()

    gen.list_formats()

    while True:
        print("\n--- Generate Barcode ---")
        barcode_type = input("Enter barcode type (e.g., CODE128): ").strip().upper()
        if barcode_type.upper() == 'EXIT':
            print("\nThank you for using Barcode Generator! Goodbye!")
            sys.exit(0)
        if barcode_type == '?':
            gen.list_formats()
            continue

        data = input("Enter data to encode: ").strip()
        if not data:
            print("Error: Data cannot be empty")
            continue

        output_file = input("Enter output filename (press Enter for auto-name): ").strip()
        if not output_file:
            output_file = None

        try:
            gen.generate_barcode(data, barcode_type, output_file)
        except Exception as e:
            print(f"Error generating barcode: {e}")
            continue

        # Ask if user wants to generate another
        another = input("\nGenerate another barcode? (y/n): ").strip().lower()
        if another != 'y':
            print("\nThank you for using Barcode Generator! Goodbye!")
            sys.exit(0)


def main():
    """Main function for CLI."""
    parser = argparse.ArgumentParser(
        description='Generate various types of barcodes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a Code 128 barcode
  python barcode_generator.py CODE128 "Hello World" -o my_barcode.png

  # Generate an EAN-13 barcode
  python barcode_generator.py EAN13 "5901234123457" -o product_barcode.png

  # List all supported formats
  python barcode_generator.py --list-formats

  # Interactive mode
  python barcode_generator.py
        """
    )

    parser.add_argument(
        'barcode_type',
        nargs='?',
        help='Type of barcode (CODE128, EAN13, CODE39, etc.)'
    )

    parser.add_argument(
        'data',
        nargs='?',
        help='Data to encode in the barcode'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: auto-generated filename)'
    )

    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List all supported barcode formats'
    )

    parser.add_argument(
        '--no-text',
        action='store_true',
        help='Do not show the encoded text below the barcode'
    )

    args = parser.parse_args()

    # Handle list formats
    if args.list_formats:
        gen = BarcodeGenerator()
        gen.list_formats()
        sys.exit(0)

    # Interactive mode if no arguments provided
    if not args.barcode_type or not args.data:
        interactive_mode()
        return

    # Generate barcode from CLI arguments
    gen = BarcodeGenerator()
    gen.generate_barcode(
        args.data,
        args.barcode_type,
        args.output,
        show_text=not args.no_text
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting Barcode Generator. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
