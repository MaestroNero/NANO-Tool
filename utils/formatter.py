import json
from tabulate import tabulate

def format_result(json_text):
    try:
        data = json.loads(json_text)
        host = data["nmaprun"]["host"]

        ip = host["address"]["@addr"]
        hostname = host.get("hostnames", {}).get("hostname", {}).get("@name", "N/A")

        # OS guesses
        os_guesses = []
        os_data = host.get("os", {}).get("osmatch", [])
        if isinstance(os_data, dict):
            os_guesses = [os_data.get("@name", "Unknown")]
        elif isinstance(os_data, list):
            os_guesses = [os.get("@name", "Unknown") for os in os_data]

        # Uptime
        uptime = "N/A"
        if "uptime" in host:
            seconds = int(host["uptime"].get("@seconds", 0))
            days = seconds // 86400
            uptime = f"~{days} days"

        # Open ports
        ports = host.get("ports", {}).get("port", [])
        if isinstance(ports, dict):
            ports = [ports]

        port_table = []
        for port in ports:
            state = port.get("state", {}).get("@state", "")
            if state != "open":
                continue
            port_id = port.get("@portid", "")
            protocol = port.get("@protocol", "")
            service = port.get("service", {})
            name = service.get("@name", "unknown")
            product = service.get("@product", "")
            version = service.get("@version", "")
            description = f"{product} {version}".strip() if product or version else "unknown"
            port_table.append([port_id, protocol, name, description])

        # Output
        output = []
        output.append(f"\n[+] Target IP   : {ip}")
        output.append(f"[+] Hostname    : {hostname}")
        output.append(f"[+] OS Guess    : {', '.join(os_guesses) if os_guesses else 'N/A'}")
        output.append(f"[+] Uptime      : {uptime}")
        output.append(f"\n[+] Open Ports:\n")

        if port_table:
            output.append(tabulate(port_table, headers=["Port", "Protocol", "Service", "Description"], tablefmt="fancy_grid"))
        else:
            output.append("No open ports found.")

        return "\n".join(output)

    except Exception as e:
        return f"[!] Error parsing result: {e}"

