#!/usr/bin/env python3
"""
Port Watcher - A CLI tool to quickly identify occupied network ports
Version: 1.0.0
"""

import socket
import sys
import argparse
from typing import List, Tuple
import time


# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PortWatcher:
    """Main class for port scanning functionality"""
    
    DEFAULT_START_PORT = 8000
    DEFAULT_END_PORT = 9000
    DEFAULT_TIMEOUT = 0.5
    
    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.localhost = '127.0.0.1'
    
    def check_port(self, port: int) -> bool:
        """
        Check if a specific port is occupied.
        
        Args:
            port: Port number to check
            
        Returns:
            True if port is busy, False if free
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        
        try:
            result = sock.connect_ex((self.localhost, port))
            sock.close()
            return result == 0
        except socket.error:
            return False
        finally:
            sock.close()
    
    def print_header(self, start_port: int, end_port: int):
        """Print a nice header for the scan"""
        print("\n" + "=" * 70)
        print(f"{Colors.BOLD}{Colors.OKCYAN}{'PORT WATCHER':^70}{Colors.ENDC}")
        print("=" * 70)
        print(f"{Colors.BOLD}Target:{Colors.ENDC} {self.localhost}")
        print(f"{Colors.BOLD}Port Range:{Colors.ENDC} {start_port} - {end_port}")
        print(f"{Colors.BOLD}Timeout:{Colors.ENDC} {self.timeout}s per port")
        print("=" * 70 + "\n")
    
    def print_progress_bar(self, current: int, total: int, width: int = 50):
        """Print a progress bar"""
        progress = current / total
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        percent = progress * 100
        print(f"\r{Colors.OKCYAN}Progress: [{bar}] {percent:.1f}% ({current}/{total}){Colors.ENDC}", end='', flush=True)
    
    def scan_ports(self, start_port: int, end_port: int, 
                   show_free: bool = False, show_busy: bool = True,
                   verbose: bool = False) -> Tuple[List[int], List[int]]:
        """
        Scan a range of ports and return busy/free ports.
        
        Args:
            start_port: Starting port number
            end_port: Ending port number
            show_free: Whether to display free ports
            show_busy: Whether to display busy ports
            verbose: Show scanning progress
            
        Returns:
            Tuple of (busy_ports, free_ports)
        """
        busy_ports = []
        free_ports = []
        total_ports = end_port - start_port + 1
        
        # Print header
        self.print_header(start_port, end_port)
        
        # Show what we're displaying
        display_mode = []
        if show_busy:
            display_mode.append(f"{Colors.FAIL}BUSY{Colors.ENDC}")
        if show_free:
            display_mode.append(f"{Colors.OKGREEN}FREE{Colors.ENDC}")
        print(f"{Colors.BOLD}Displaying:{Colors.ENDC} {' and '.join(display_mode)} ports\n")
        
        if verbose:
            print(f"{Colors.BOLD}Scanning in progress...{Colors.ENDC}\n")
        
        start_time = time.time()
        
        # Column headers
        if show_busy or show_free:
            print(f"{Colors.BOLD}{'PORT':<10} {'STATUS':<15} {'INFO':<30}{Colors.ENDC}")
            print("-" * 70)
        
        for i, port in enumerate(range(start_port, end_port + 1), 1):
            # Update progress bar if verbose
            if verbose:
                self.print_progress_bar(i, total_ports)
            
            is_busy = self.check_port(port)
            
            if is_busy:
                busy_ports.append(port)
                if show_busy:
                    if not verbose:
                        status = f"{Colors.FAIL}● BUSY{Colors.ENDC}"
                        info = "Service is running on this port"
                        print(f"{port:<10} {status:<24} {info:<30}")
            else:
                free_ports.append(port)
                if show_free:
                    if not verbose:
                        status = f"{Colors.OKGREEN}○ FREE{Colors.ENDC}"
                        info = "Port is available"
                        print(f"{port:<10} {status:<24} {info:<30}")
        
        if verbose:
            print("\n")  # Clear progress bar line
        
        scan_time = time.time() - start_time
        
        return busy_ports, free_ports, scan_time
    
    def print_summary(self, busy_ports: List[int], free_ports: List[int], scan_time: float):
        """Print a detailed summary of the scan"""
        total_scanned = len(busy_ports) + len(free_ports)
        
        print("\n" + "=" * 70)
        print(f"{Colors.BOLD}{Colors.OKCYAN}{'SCAN SUMMARY':^70}{Colors.ENDC}")
        print("=" * 70)
        
        # Statistics
        print(f"\n{Colors.BOLD}Statistics:{Colors.ENDC}")
        print(f"  Total Scanned:  {total_scanned}")
        print(f"  {Colors.FAIL}Busy Ports:{Colors.ENDC}     {len(busy_ports)}")
        print(f"  {Colors.OKGREEN}Free Ports:{Colors.ENDC}     {len(free_ports)}")
        print(f"  Scan Time:      {scan_time:.2f} seconds")
        print(f"  Speed:          {total_scanned/scan_time:.0f} ports/sec")
        
        # Show busy ports if any
        if busy_ports:
            print(f"\n{Colors.BOLD}{Colors.FAIL}Busy Ports:{Colors.ENDC}")
            # Group ports for better display
            if len(busy_ports) <= 20:
                for i in range(0, len(busy_ports), 5):
                    ports_line = ", ".join(str(p) for p in busy_ports[i:i+5])
                    print(f"  {ports_line}")
            else:
                print(f"  {busy_ports[0]}, {busy_ports[1]}, {busy_ports[2]}, ... (showing first 3 of {len(busy_ports)})")
                print(f"  Use -v flag to see all busy ports")
        else:
            print(f"\n{Colors.OKGREEN}✓ No busy ports found - all ports are free!{Colors.ENDC}")
        
        # Recommendations
        if busy_ports and len(busy_ports) < total_scanned:
            print(f"\n{Colors.BOLD}Recommendations:{Colors.ENDC}")
            print(f"  • Use -f flag to find available ports")
            print(f"  • Check --manual to see all services")
        
        print("=" * 70 + "\n")


def print_manual():
    """Print the complete user manual"""
    manual = """
╔════════════════════════════════════════════════════════════════════════╗
║                      PORT WATCHER - USER MANUAL                        ║
║                           Version 1.0.0                                ║
╚════════════════════════════════════════════════════════════════════════╝

DESCRIPTION:
    Port Watcher is a lightweight CLI tool that quickly identifies which 
    local network ports are currently occupied on your system.

USAGE:
    python port_watcher.py [OPTIONS]

OPTIONS:
    -s, --start PORT        Starting port number (default: 8000)
    -e, --end PORT          Ending port number (default: 9000)
    -p, --port PORT         Check a single specific port
    -f, --show-free         Show free ports (default: only busy ports)
    -a, --show-all          Show both busy and free ports
    -t, --timeout SECONDS   Connection timeout in seconds (default: 0.5)
    -v, --verbose           Show scanning progress
    --help                  Show this help message
    --manual                Show complete user manual (this page)
    --examples              Show usage examples

EXAMPLES:
    # Scan default range (8000-9000) for busy ports
    python port_watcher.py

    # Scan custom range
    python port_watcher.py -s 3000 -e 5000

    # Check a single port
    python port_watcher.py -p 8080

    # Show all ports (busy and free)
    python port_watcher.py -a

    # Show only free ports
    python port_watcher.py -f

    # Verbose mode with progress
    python port_watcher.py -v -s 1000 -e 2000

    # Quick scan with shorter timeout
    python port_watcher.py -t 0.2 -s 8000 -e 8100

HOW IT WORKS:
    Port Watcher uses TCP socket connections to test port availability:
    
    1. For each port in the specified range, it attempts to establish
       a TCP connection to localhost (127.0.0.1).
    
    2. If the connection succeeds, the port is marked as "BUSY" (occupied
       by a running service).
    
    3. If the connection fails, the port is marked as "FREE" (available
       for use).
    
    4. A timeout mechanism ensures the scan completes quickly even for
       unresponsive ports.

TECHNICAL DETAILS:
    • Protocol: TCP (SOCK_STREAM)
    • Target: localhost (127.0.0.1)
    • Default Timeout: 0.5 seconds per port
    • Port Range: 1-65535 (default scan: 8000-9000)
    • Socket Mode: Non-blocking with timeout

COMMON USE CASES:
    • Finding which development server ports are in use
    • Checking if a service is running on a specific port
    • Identifying port conflicts before starting applications
    • Quick inventory of active local services
    • Debugging network service issues

TROUBLESHOOTING:
    • Slow scans: Reduce port range or decrease timeout value
    • Permission errors: Some ports (1-1024) may require sudo/admin rights
    • No ports found: Ensure services are running and listening on localhost

EXIT CODES:
    0 - Success
    1 - Error (invalid arguments, scanning error)

NOTES:
    • This tool only scans localhost (127.0.0.1), not external hosts
    • Ports below 1024 typically require administrator privileges
    • A "BUSY" port indicates an active service, not necessarily accessible
    • Some firewalls may interfere with port scanning results

For more information, run: python port_watcher.py --examples
"""
    print(manual)


def print_examples():
    """Print usage examples"""
    examples = """
╔════════════════════════════════════════════════════════════════════════╗
║                     PORT WATCHER - USAGE EXAMPLES                      ║
╚════════════════════════════════════════════════════════════════════════╝

BASIC USAGE:
    # Scan default ports (8000-9000)
    $ python port_watcher.py
    Port 8000: BUSY ✗
    Port 8080: BUSY ✗
    Port 8888: BUSY ✗

CUSTOM PORT RANGE:
    # Scan ports 3000-5000
    $ python port_watcher.py --start 3000 --end 5000
    Port 3000: BUSY ✗
    Port 4200: BUSY ✗

    # Short form
    $ python port_watcher.py -s 3000 -e 5000

SINGLE PORT CHECK:
    # Check if port 8080 is busy
    $ python port_watcher.py --port 8080
    Port 8080: BUSY ✗

    # Short form
    $ python port_watcher.py -p 8080

SHOW ALL PORTS:
    # Display both busy AND free ports
    $ python port_watcher.py --show-all -s 8000 -e 8005
    Port 8000: BUSY ✗
    Port 8001: FREE ✓
    Port 8002: FREE ✓
    Port 8003: BUSY ✗
    Port 8004: FREE ✓
    Port 8005: FREE ✓

SHOW ONLY FREE PORTS:
    # Useful for finding available ports
    $ python port_watcher.py --show-free -s 3000 -e 3010
    Port 3001: FREE ✓
    Port 3002: FREE ✓
    Port 3004: FREE ✓
    Port 3007: FREE ✓

VERBOSE MODE:
    # Show progress while scanning
    $ python port_watcher.py -v -s 1000 -e 2000
    Scanning ports 1000-2000 on 127.0.0.1...
    ------------------------------------------------------------
    Progress: 45.2% (452/1001 ports)
    Port 1080: BUSY ✗
    Port 1433: BUSY ✗
    ------------------------------------------------------------

QUICK SCAN:
    # Reduce timeout for faster scanning
    $ python port_watcher.py -t 0.2 -s 8000 -e 8100

COMMON SCENARIOS:

    1. Find an available port for your web server:
       $ python port_watcher.py -f -s 3000 -e 3100

    2. Check if your database is running:
       $ python port_watcher.py -p 5432  # PostgreSQL
       $ python port_watcher.py -p 3306  # MySQL
       $ python port_watcher.py -p 27017 # MongoDB

    3. Quick check of development ports:
       $ python port_watcher.py -s 3000 -e 9000

    4. Scan well-known service ports:
       $ python port_watcher.py -s 80 -e 443 -a

    5. Find all busy ports in a large range:
       $ python port_watcher.py -s 1 -e 10000 -v

COMBINING OPTIONS:
    $ python port_watcher.py -s 8000 -e 8100 -a -v -t 0.3
    (Custom range, show all, verbose, custom timeout)

REAL-WORLD WORKFLOW:
    # Step 1: Find what's currently running
    $ python port_watcher.py

    # Step 2: Find an available port
    $ python port_watcher.py -f -s 8000 -e 8010

    # Step 3: Verify your service started
    $ python port_watcher.py -p 8001
"""
    print(examples)


def print_quick_help():
    """Print quick help message"""
    help_text = """
Port Watcher - Quick Help

Usage: python port_watcher.py [OPTIONS]

Common Options:
  -s, --start PORT    Start port (default: 8000)
  -e, --end PORT      End port (default: 9000)
  -p, --port PORT     Check single port
  -a, --show-all      Show busy and free ports
  -v, --verbose       Show progress
  --manual            Full user manual
  --examples          Usage examples

Examples:
  python port_watcher.py                    # Scan 8000-9000
  python port_watcher.py -s 3000 -e 5000    # Custom range
  python port_watcher.py -p 8080            # Single port
  python port_watcher.py --manual           # Full manual
"""
    print(help_text)


def main():
    """Main entry point for the CLI tool"""
    parser = argparse.ArgumentParser(
        description='Port Watcher - Quickly identify occupied network ports',
        add_help=False
    )
    
    # Port range options
    parser.add_argument('-s', '--start', type=int, 
                       default=PortWatcher.DEFAULT_START_PORT,
                       help=f'Starting port number (default: {PortWatcher.DEFAULT_START_PORT})')
    parser.add_argument('-e', '--end', type=int,
                       default=PortWatcher.DEFAULT_END_PORT,
                       help=f'Ending port number (default: {PortWatcher.DEFAULT_END_PORT})')
    parser.add_argument('-p', '--port', type=int,
                       help='Check a single specific port')
    
    # Display options
    parser.add_argument('-f', '--show-free', action='store_true',
                       help='Show free ports instead of busy ports')
    parser.add_argument('-a', '--show-all', action='store_true',
                       help='Show both busy and free ports')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show scanning progress')
    
    # Configuration options
    parser.add_argument('-t', '--timeout', type=float,
                       default=PortWatcher.DEFAULT_TIMEOUT,
                       help=f'Connection timeout in seconds (default: {PortWatcher.DEFAULT_TIMEOUT})')
    
    # Help and documentation
    parser.add_argument('--help', action='store_true',
                       help='Show this help message')
    parser.add_argument('--manual', action='store_true',
                       help='Show complete user manual')
    parser.add_argument('--examples', action='store_true',
                       help='Show usage examples')
    
    args = parser.parse_args()
    
    # Handle documentation requests
    if args.manual:
        print_manual()
        return 0
    
    if args.examples:
        print_examples()
        return 0
    
    if args.help:
        print_quick_help()
        return 0
    
    # Validate arguments
    if args.port:
        if not (1 <= args.port <= 65535):
            print(f"{Colors.FAIL}Error: Port must be between 1 and 65535{Colors.ENDC}", file=sys.stderr)
            return 1
        start_port = end_port = args.port
    else:
        if not (1 <= args.start <= 65535) or not (1 <= args.end <= 65535):
            print(f"{Colors.FAIL}Error: Ports must be between 1 and 65535{Colors.ENDC}", file=sys.stderr)
            return 1
        if args.start > args.end:
            print(f"{Colors.FAIL}Error: Start port must be <= end port{Colors.ENDC}", file=sys.stderr)
            return 1
        start_port = args.start
        end_port = args.end
    
    # Determine display mode
    show_busy = True
    show_free = False
    
    if args.show_all:
        show_busy = True
        show_free = True
    elif args.show_free:
        show_busy = False
        show_free = True
    
    # Run the scan
    try:
        watcher = PortWatcher(timeout=args.timeout)
        busy_ports, free_ports, scan_time = watcher.scan_ports(
            start_port, end_port, show_free, show_busy, args.verbose
        )
        
        # Print summary
        watcher.print_summary(busy_ports, free_ports, scan_time)
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Scan interrupted by user.{Colors.ENDC}")
        return 1
    except Exception as e:
        print(f"{Colors.FAIL}Error: {str(e)}{Colors.ENDC}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())