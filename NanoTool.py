import os
import subprocess
import sys
import shutil
import xmltodict
import json
import time
import threading
import itertools

try:
    from tabulate import tabulate
except ImportError:
    print("[!] 'tabulate' not found. Installing...")
    os.system("pip install tabulate")
    from tabulate import tabulate

try:
    from utils.formatter import format_result
except ImportError:
    print("[!] 'formatter.py' not found.")
    sys.exit(1)

class Colors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

BANNER = f'''
{Colors.OKCYAN}
███╗   ██╗ █████╗ ███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗
████╗  ██║██╔══██╗████╗  ██║██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
██╔██╗ ██║███████║██╔██╗ ██║██║   ██║       ██║   ██║   ██║██║   ██║██║
██║╚██╗██║██╔══██║██║╚██╗██║██║   ██║       ██║   ██║   ██║██║   ██║██║
██║ ╚████║██║  ██║██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝██║
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚═╝
{Colors.ENDC}
{Colors.OKGREEN}{Colors.BOLD}
                          NANO TOOL
         Smart & Modular Nmap-based Scanning Utility

     Made by Maestro Nero with Love 💖 | Telegram: @CYBER_Nero
{Colors.ENDC}
'''

class Spinner:
    def __init__(self, message="Processing..."):
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])
        self.stop_running = False
        self.message = message
        self.thread = threading.Thread(target=self.spin)

    def spin(self):
        while not self.stop_running:
            sys.stdout.write(f"\r{self.message} {next(self.spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_running = True
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

def check_dependencies():
    if not shutil.which("nmap"):
        print("[!] Nmap is not installed. Installing...")
        os.system("sudo apt update && sudo apt install nmap -y")

    try:
        import xmltodict
    except ImportError:
        print("[!] Installing 'xmltodict'...")
        os.system("pip install xmltodict")

def run_scan(target, level):
    scan_types = {
        "1": (
            "🔹 Light Scan",
            ["nmap", "-T4", "-sV", "-O", "--version-light", "-oX", "result.xml", target]
        ),
        "2": (
            "⚙️ Medium Scan",
            ["nmap", "-sS", "-sV", "-p-", "-T4", "-O", "-oX", "result.xml", target]
        ),
        "3": (
            "🔍 Deep Scan",
            ["nmap", "-A", "-T4", "-p-", "-oX", "result.xml", target]
        )
    }

    if level not in scan_types:
        print("[✘] Invalid scan type.")
        return

    scan_name, command = scan_types[level]
    print(f"\n[+] Executing {scan_name} on target: {target}\n")

    spinner = Spinner("Scanning in progress")
    spinner.start()

    def scan_task():
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    thread = threading.Thread(target=scan_task)
    thread.start()
    thread.join()

    spinner.stop()

    try:
        with open("result.xml", "r") as f:
            data = xmltodict.parse(f.read())
            json_output = json.dumps(data, indent=2)

        with open("result.json", "w") as jf:
            jf.write(json_output)

        print("\n[✓] Scan result saved to result.json")
        print("\n📊 Scan Summary:\n")
        print(format_result(json_output))

    except Exception as e:
        print(f"[!] Failed to parse result: {e}")

def main():
    os.system("clear")
    print(BANNER)
    check_dependencies()

    while True:
        target = input("\n[?] Enter target IP or domain (or 'exit' to quit): ").strip()
        if target.lower() in ["exit", "quit"]:
            print("\n[👋] Goodbye.\n")
            break

        print("\n[Scan Type]")
        print("1. Light Scan 🔹")
        print("2. Medium Scan ⚙️")
        print("3. Deep Scan 🔍")
        scan_type = input("\n>> ")

        run_scan(target, scan_type)

        input("\n[↩️] Press Enter to return to main menu...")

if __name__ == "__main__":
    main()

