# 🛡️ Port Watcher - User Manual

**Port Watcher** (`port_watch.py`) is a professional-grade network analysis CLI tool. It helps developers identifying open ports, detect which processes are using them, and manage system resources—all without leaving the terminal.

It is built entirely with the **Python Standard Library**, requiring zero external dependencies (no `pip install` needed).

---

## 🚀 Prerequisites

* **Python 3.6+** installed.
* **Operating System:** Windows, macOS, or Linux.
* **Permissions:** * **Basic Scan:** Works with standard user permissions.
    * **Advanced Features (PID/Kill):** Requires **Admin/Root** privileges to see Process IDs and terminate tasks.
        * *Windows:* Run Command Prompt/PowerShell as Administrator.
        * *Linux/Mac:* Run with `sudo`.

---

## ⚡ Quick Start

1.  Navigate to the tool's directory:
    ```bash
    cd tools
    ```
2.  Run the script:
    ```bash
    python port_watch.py
    ```
    *(Or `sudo python3 port_watch.py` on Linux/Mac for full features)*

---

## 🎮 Main Menu Options

When you launch the tool, you will see the interactive dashboard with the following options:

### **1. ⚡ Quick Scan (Top 20 Ports)**
Scans the most critical networking ports used by common services. Use this for a rapid health check.
* **Includes:** FTP (21), SSH (22), DNS (53), HTTP (80), HTTPS (443), MySQL (3306), Redis (6379), Local Dev (8000, 8080), and more.

### **2. 🌐 Standard Scan (1-1000)**
Performs a multi-threaded scan of the first 1000 ports (System Ports). 
* **Best for:** Finding hidden services or unexpected open ports on your system.

### **3. 🎯 Custom Range Scan**
Allows you to define a specific start and end port.
* **Best for:** Debugging specific applications (e.g., checking ports 3000-4000 for React apps).

### **4. ⚙️ Change Target IP**
* **Default:** `127.0.0.1` (Localhost).
* **Remote Scan:** You can enter a LAN IP (e.g., `192.168.1.5`) to scan other devices on your network. 
    * *Note:* Process ID (PID) detection and "Kill" features are disabled for remote targets.

---

## 🛠️ Interactive Features (Post-Scan)

After a scan completes, you are presented with a results table and an Action Menu.

### **Viewing Results**
The table provides detailed insights:
* **PORT:** The port number (Color-coded: Blue=Web, Yellow=Admin).
* **PID:** The **Process ID** of the application using the port.
* **PROCESS NAME:** The actual executable name (e.g., `python.exe`, `nginx`).
* **SERVICE BANNER:** The "Welcome Message" sent by the service (e.g., `Server: Apache/2.4`).

### **Taking Action**
You can type the **ID Number** of any result row to enter the **Inspection Mode**:

* **🔍 Inspect:** View full details about the port and process.
* **💀 Kill Process:** If a port is stuck (e.g., "Address already in use"), press **`K`** inside the inspection menu to force-kill the process. The tool handles the OS-specific commands (`taskkill` or `kill -9`) for you.

### **💾 Save Reports**
* Type **`S`** in the results menu to export the current scan data to a timestamped JSON file (e.g., `scan_20231027_1230.json`) for documentation.

---

## ❓ Troubleshooting

**Q: Why do I see "Unknown/Hidden" under Process Name?**
**A:** This usually happens if you lack permissions. Try running the terminal as **Administrator** or using `sudo`.

**Q: The scan is slow on remote targets.**
**A:** This is normal. Network latency impacts remote scanning speed. Localhost scans are near-instant.

**Q: Can I use this on a server?**
**A:** Yes! Since it uses only standard libraries, you can upload just the `port_watch.py` file to any server and run it immediately without installing packages.