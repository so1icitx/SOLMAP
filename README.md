# so1map: Port Scanner

## Overview
so1map is a Python-based port scanner for network reconnaissance in pentesting and CTF challenges and just practice for making python scripts. It scans single IPs or subnets to find open ports, with customizable ranges, threading, and output formats (CSV, JSON, text). It’s a work in progress, and i could add more stuff in future.

## Purpose
so1map identifies open ports on target systems, helping you spot services and potential vulnerabilities for security testing.

## Features
- Scans single IPs (e.g., `192.168.1.1`) or subnets (e.g., `192.168.1.0/24`).
- Custom port range (default: 1-1024).
- Multi-threaded for fast scans (default: 100 threads).
- Output formats: CSV, JSON (clean or standard), or text.
- Quiet mode to save results to file without terminal output.
- Validates IPs/subnets with regex and error handling.
- Shows scan duration.



## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/so1icitx/so1map.git
   cd so1map
   ```
2. Ensure Python 3.6+ is installed (no external libraries needed).
3. Run with root if required for raw sockets:
   ```bash
   sudo python3 so1map.v.1.0.3.py
   ```

## Usage
Run so1map with command-line arguments to scan IPs or subnets.

### Command-Line Options
| Option | Description | Example |
|--------|-------------|---------|
| `-ip`, `--ipaddress` | Single IP or subnet (required). | `-ip 192.168.1.1` or `-ip 192.168.1.0/24` |
| `-p`, `--port` | Port range (1 to specified number, default: 1024). | `-p 65535` |
| `-t`, `--threads` | Number of threads (default: 100). | `-t 200` |
| `-f`, `--file_type` | Output format: `csv`, `json`, `json-clean`, `txt` (default: none). | `-f json-clean` |
| `-o`, `--output` | Output file path (required with `-f`). | `-o scan.json` |
| `--quiet` | Suppress terminal output, save to file. | `--quiet` |

### Examples
1. Scan a single IP (ports 1-1024):
   ```bash
   python3 so1map.v.1.0.3.py -ip 192.168.1.1
   ```
   **Output**:
   ```
   Starting so1map (https://so1icitx.cfd) at 12-09-25 13:00:00 beaconing 192.168.1.1
   PORT    STATE
   22      open
   80      open
   scanned in 2.34 seconds
   ```

2. Scan a subnet with CSV output:
   ```bash
   python3 so1map.v.1.0.3.py -ip 192.168.1.0/24 -p 100 -f csv -o results.csv
   ```
   **Output File (results.csv)**:
   ```
   IP,PORT,STATUS
   192.168.1.1,22,open
   192.168.1.1,80,open
   192.168.1.10,443,open
   ```

3. Quiet mode with clean JSON output:
   ```bash
   python3 so1map.v.1.0.3.py -ip. 192.168.10/24 -p 1024 -t 500 -f json-clean -o scan.json --quiet
   ```
   **Output File (scan.json)**:
   ```
   {
     "ip": " 192.168.1.4",
     "port": 22,
     "status": "open"
   }
   {
     "ip": " 192.168.1.4",
     "port": 993,
     "status": "open"
   }
   {
     "ip": " 192.168.1.5",
     "port": 443,
     "status": "open"
   }
   {
     "ip": " 192.168.1.5",
     "port": 80,
     "status": "open"
   }
   ```

## Disclaimer
Use so1map responsibly and only on systems you have permission to scan. Unauthorized use may violate laws or terms of service.
