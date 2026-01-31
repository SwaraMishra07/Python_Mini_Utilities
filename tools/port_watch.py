import socket
import concurrent.futures
import sys
import time
import os
import subprocess
import platform
import json
import signal
from datetime import datetime

# --- CONFIGURATION ---
TIMEOUT = 1.0  # Seconds
MAX_THREADS = 100

# --- UI COLORS ---
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

# --- CORE ENGINE ---
class PortInspector:
    def __init__(self, target="127.0.0.1"):
        self.target = target
        self.is_local = target in ["127.0.0.1", "localhost", "0.0.0.0", "::1"]
        self.os_type = platform.system()

    def kill_process(self, pid):
        """Terminates a process by PID Cross-Platform"""
        try:
            pid = int(pid)
            if self.os_type == "Windows":
                subprocess.run(f"taskkill /PID {pid} /F", shell=True, check=True, stdout=subprocess.DEVNULL)
            else:
                os.kill(pid, signal.SIGKILL)
            return True, "Success"
        except Exception as e:
            return False, str(e)

    def get_process_info(self, port):
        """Finds PID and Name for a local port."""
        if not self.is_local: return None, "Remote Host"
        
        try:
            if self.os_type == "Windows":
                # Windows: Netstat -> PID -> Tasklist
                cmd = f'netstat -ano | findstr :{port}'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
                for line in res.splitlines():
                    parts = line.split()
                    if f":{port}" in parts[1] or f":{port}" in parts[2]: 
                        pid = parts[-1]
                        task_cmd = f'tasklist /fi "pid eq {pid}" /fo csv /nh'
                        task_res = subprocess.run(task_cmd, shell=True, capture_output=True, text=True).stdout
                        name = task_res.split(',')[0].strip('"')
                        return pid, name
            else:
                # Linux/Mac: lsof
                cmd = ["lsof", "-i", f":{port}", "-t"]
                pid = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
                if pid:
                    pid = pid.split('\n')[0] 
                    name_cmd = ["ps", "-p", pid, "-o", "comm="]
                    name = subprocess.run(name_cmd, capture_output=True, text=True).stdout.strip()
                    return pid, name
        except:
            pass
        return None, "Unknown/Hidden"

    def grab_banner(self, port):
        """Attempts to identify the service version."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((self.target, port))
            
            probe = b'HEAD / HTTP/1.0\r\n\r\n'
            if port not in [21, 22, 23, 25]: 
                s.send(probe)
                
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            s.close()
            
            if "Server:" in banner:
                return banner.split("Server:")[1].split('\n')[0].strip()
            if "SSH" in banner:
                return banner.split('\n')[0]
            return banner[:40] 
        except:
            return None

    def scan_port(self, port):
        """Worker function for threads."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(TIMEOUT)
                if s.connect_ex((self.target, port)) == 0:
                    pid, name = self.get_process_info(port)
                    banner = self.grab_banner(port)
                    return {"port": port, "state": "OPEN", "pid": pid, "name": name, "banner": banner}
        except:
            pass
        return None

# --- INTERACTIVE DASHBOARD ---
class Dashboard:
    def __init__(self):
        self.inspector = PortInspector()
        self.history = []
        self.user = "Admin"

    def header(self):
        Colors.cls()
        print(f"{Colors.BLUE}{Colors.BOLD}")
        # Updated ASCII Art to clearly spell "PORT WATCHER"
        print(r"""
  ___  ___  ___ _____   _      __      _       _               
 | _ \/ _ \| _ \_   _| | |    / /_ _ _| |_ ___| |__  ___ _ _   
 |  _/ (_) |   / | |   | |/\|/ / _` |  _/ __| '_ \/ -_) '_|  
 |_|  \___/|_|_\ |_|   |__/\__/\__,_|\__\___|_| _\___|_|     
        """)
        print(f"{Colors.RESET}{Colors.HEADER}     >>> Professional Port Analysis Suite <<<{Colors.RESET}")
        print(f"\n  {Colors.BOLD}User:{Colors.RESET}   {self.user} | {Colors.BOLD}Target:{Colors.RESET} {self.inspector.target}")
        print("  " + "="*70)

    def print_table(self, results):
        print(f"\n  {Colors.CYAN}{'ID':<4} {'PORT':<7} {'PID':<8} {'PROCESS NAME':<25} {'SERVICE BANNER'}{Colors.RESET}")
        print("  " + "-"*70)
        
        for idx, r in enumerate(results):
            pid_disp = r['pid'] if r['pid'] else "-"
            name_disp = r['name'][:24]
            banner_disp = r['banner'] if r['banner'] else ""
            
            color = Colors.GREEN
            if r['port'] in [22, 3389, 23]: color = Colors.WARNING 
            if r['port'] in [80, 443]: color = Colors.BLUE          
            
            print(f"  {idx+1:<4} {color}{r['port']:<7}{Colors.RESET} {pid_disp:<8} {name_disp:<25} {Colors.WARNING}{banner_disp}{Colors.RESET}")
        print("  " + "-"*70)

    def run_scan(self, ports):
        print(f"\n  {Colors.BOLD}🚀 Scanning {len(ports)} ports...{Colors.RESET}")
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(self.inspector.scan_port, p): p for p in ports}
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                if data: results.append(data)
        
        results.sort(key=lambda x: x['port'])
        self.history = results
        return results

    def result_menu(self):
        while True:
            self.header()
            if not self.history:
                print(f"\n  {Colors.FAIL}No open ports found or no scan run yet.{Colors.RESET}")
                input("\n  Press Enter to return...")
                return

            self.print_table(self.history)
            print(f"\n  {Colors.BOLD}ACTIONS:{Colors.RESET}")
            print("  [1-N] Select ID to Inspect/Kill")
            print("  [S]   Save Results (JSON)")
            print("  [B]   Back to Main Menu")
            
            choice = input(f"\n  {Colors.BLUE}>> {Colors.RESET}").strip().upper()
            
            if choice == 'B': return
            elif choice == 'S': self.save_json()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.history):
                    self.inspect_details(self.history[idx])

    def inspect_details(self, data):
        while True:
            Colors.cls()
            print(f"\n  {Colors.HEADER}=== PORT {data['port']} DETAILS ==={Colors.RESET}")
            print(f"  {Colors.BOLD}Status:{Colors.RESET}      OPEN")
            print(f"  {Colors.BOLD}Process:{Colors.RESET}     {data['name']}")
            print(f"  {Colors.BOLD}PID:{Colors.RESET}         {data['pid']}")
            print(f"  {Colors.BOLD}Banner:{Colors.RESET}      {data['banner']}")
            print("\n  -----------------------------")
            
            if data['pid']:
                print(f"  {Colors.FAIL}[K]{Colors.RESET} KILL Process ({data['pid']})")
            print(f"  {Colors.BLUE}[B]{Colors.RESET} Back")
            
            opt = input(f"\n  {Colors.BLUE}>> {Colors.RESET}").strip().upper()
            
            if opt == 'K' and data['pid']:
                confirm = input(f"  {Colors.FAIL}Kill PID {data['pid']}? (Y/N): {Colors.RESET}")
                if confirm.upper() == 'Y':
                    success, msg = self.inspector.kill_process(data['pid'])
                    if success:
                        print(f"\n  {Colors.GREEN}Process Killed.{Colors.RESET}")
                        data['state'] = "KILLED" 
                        time.sleep(1)
                        return
                    else:
                        print(f"\n  {Colors.FAIL}Error: {msg}{Colors.RESET}")
                        input("  Press Enter...")
            elif opt == 'B':
                return

    def save_json(self):
        fname = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(fname, 'w') as f:
            json.dump(self.history, f, indent=4)
        print(f"\n  {Colors.GREEN}Saved to {fname}{Colors.RESET}")
        time.sleep(1)

    def main_loop(self):
        while True:
            self.header()
            print(f"\n  {Colors.BOLD}MAIN MENU:{Colors.RESET}")
            print("  1. ⚡ Quick Scan (Top 20 Ports)")
            print("  2. 🌐 Standard Scan (1-1000)")
            print("  3. 🎯 Custom Range Scan")
            print("  4. ⚙️ Change Target IP")
            print("  0. ❌ Exit")
            
            opt = input(f"\n  {Colors.BLUE}>> {Colors.RESET}").strip()
            
            if opt == '1':
                ports = [21,22,23,25,53,80,110,135,139,143,443,445,3306,3389,5432,6379,8000,8080,8888,27017]
                self.run_scan(ports)
                self.result_menu()
            elif opt == '2':
                self.run_scan(range(1, 1001))
                self.result_menu()
            elif opt == '3':
                try:
                    s = int(input("  Start Port: "))
                    e = int(input("  End Port:   "))
                    self.run_scan(range(s, e+1))
                    self.result_menu()
                except:
                    print(f"  {Colors.FAIL}Invalid numbers.{Colors.RESET}")
                    time.sleep(1)
            elif opt == '4':
                new_t = input("  Enter IP [127.0.0.1]: ").strip()
                if new_t: 
                    self.inspector.target = new_t
                    self.inspector.is_local = new_t in ["127.0.0.1", "localhost", "0.0.0.0"]
            elif opt == '0':
                Colors.cls()
                print("Goodbye.")
                sys.exit()

if __name__ == "__main__":
    try:
        dash = Dashboard()
        dash.main_loop()
    except KeyboardInterrupt:
        print("\nExiting...")