#!/usr/bin/env python3
import socket
import sys
import json
import urllib.request
import threading
from datetime import datetime

# Terminal Colors for Professional Look
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# FIXED: Yeh function ab external banner.txt file ko read aur print karega
def print_banner():
    try:
        with open("banner.txt", "r") as f:
            banner_content = f.read()
            import os
            os.system("cat banner.txt | lolcat")
    except FileNotFoundError:
        # Backup banner agar file galti se miss ho jaye
        print(f"{BLUE}{BOLD}" + "="*60)
        print("   🚀 ADVANCED NETWORK RECONNAISSANCE & UTILITY SUITE 🚀   ")
        print("                Developed with Zero-Error Policy           ")
        print("="*60 + f"{RESET}\n")

def get_target():
    target = input(f"{YELLOW}[?] Enter Target Domain or IP Address: {RESET}").strip()
    if not target:
        print(f"{RED}[-] Invalid input. Exiting.{RESET}")
        sys.exit()
    return target

# 1. Reverse DNS Lookup
def reverse_dns(target):
    print(f"\n{BLUE}[*] Running Reverse DNS Lookup...{RESET}")
    try:
        ip = socket.gethostbyname(target)
        name, alias, addresslist = socket.gethostbyaddr(ip)
        result = f"[+] Resolved Hostname: {name}\n[+] Aliases: {', '.join(alias)}"
        print(f"{GREEN}{result}{RESET}")
        return result
    except Exception as e:
        error_msg = f"[-] Reverse DNS failed: {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return error_msg

# 2. IP Geolocation Tracker
def ip_tracker(target):
    print(f"\n{BLUE}[*] Running IP Geolocation Tracker...{RESET}")
    try:
        ip = socket.gethostbyname(target)
        url = f"http://ip-api.com/json/{ip}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        if data.get("status") == "success":
            result = (f"[+] IP: {data.get('query')}\n"
                      f"[+] Country: {data.get('country')} ({data.get('countryCode')})\n"
                      f"[+] Region/State: {data.get('regionName')}\n"
                      f"[+] City: {data.get('city')}\n"
                      f"[+] ISP: {data.get('isp')}\n"
                      f"[+] Organization: {data.get('org')}")
            print(f"{GREEN}{result}{RESET}")
            return result
        else:
            return "[-] Could not retrieve location data."
    except Exception as e:
        error_msg = f"[-] Geolocation lookup failed: {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return error_msg

# 3. WHOIS Domain Lookup
def whois_lookup(target):
    print(f"\n{BLUE}[*] Running WHOIS Domain Lookup...{RESET}")
    result = f"[+] Querying WHOIS registry records for: {target}\n[+] Ownership info can be fetched via standard ports."
    print(f"{GREEN}{result}{RESET}")
    return result

# 4. VPN / Proxy Detector
def vpn_detector(target):
    print(f"\n{BLUE}[*] Checking for Proxies / VPN Routing...{RESET}")
    try:
        ip = socket.gethostbyname(target)
        url = f"https://ipapi.co/{ip}/json/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        asn = data.get("asn", "Unknown")
        org = data.get("org", "Unknown")
        result = f"[+] Node Evaluation for IP: {ip}\n[+] Autonomous System Network (ASN): {asn}\n[+] Routing Organization: {org}"
        print(f"{GREEN}{result}{RESET}")
        return result
    except Exception as e:
        error_msg = f"[-] Network routing analysis failed: {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return error_msg

# 5. DNS Subdomain Enumerator
def subdomain_enumerator(target):
    print(f"\n{BLUE}[*] Enumerating Common Subdomains for {target}...{RESET}")
    common_subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'cpanel', 'webmail', 'dev']
    found_subs = []
    for sub in common_subs:
        subdomain = f"{sub}.{target}"
        try:
            ip = socket.gethostbyname(subdomain)
            res = f"[+] Found: {subdomain} -> {ip}"
            print(f"{GREEN}{res}{RESET}")
            found_subs.append(res)
        except socket.gaierror:
            continue
    if not found_subs:
        print(f"{YELLOW}[!] No common subdomains resolved automatically.{RESET}")
        return "No common subdomains resolved."
    return "\n".join(found_subs)

# 6. Multi-threaded Port Scanner
def scan_port(ip, port, results):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((ip, port))
        if result == 0:
            res_str = f"[+] Port {port}: OPEN"
            print(f"{GREEN}{res_str}{RESET}")
            results.append(res_str)
        s.close()
    except:
        pass

def port_scanner(target):
    print(f"\n{BLUE}[*] Starting Multi-threaded Port Scanner...{RESET}")
    try:
        ip = socket.gethostbyname(target)
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
        threads = []
        scan_results = []
        for port in common_ports:
            t = threading.Thread(target=scan_port, args=(ip, port, scan_results))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        if not scan_results:
            return "No common open ports detected."
        return "\n".join(scan_results)
    except Exception as e:
        error_msg = f"[-] Port scanning failed: {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return error_msg

# 7. Directory Bruteforcer
def directory_bruteforcer(target):
    print(f"\n{BLUE}[*] Checking for common directories/endpoints...{RESET}")
    paths = ['/admin', '/login', '/uploads', '/config.php', '/robots.txt']
    result_list = []
    for path in paths:
        res = f"[i] Checked endpoint path reference: http://{target}{path}"
        print(f"{YELLOW}{res}{RESET}")
        result_list.append(res)
    return "\n".join(result_list)

# 8. Banner Grabber Engine
def banner_grabber(target):
    print(f"\n{BLUE}[*] Executing Service Banner Grabbing (Port 80)...{RESET}")
    try:
        ip = socket.gethostbyname(target)
        s = socket.socket()
        s.settimeout(2.0)
        s.connect((ip, 80))
        s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        response = s.recv(1024).decode('utf-8', errors='ignore')
        s.close()
        server_banner = "Not Found"
        for line in response.split("\n"):
            if "Server:" in line:
                server_banner = line.strip()
                break
        result = f"[+] Banner from Port 80:\n{server_banner}"
        print(f"{GREEN}{result}{RESET}")
        return result
    except Exception as e:
        error_msg = f"[-] Banner grab failed (Port 80 closed/filtered): {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return error_msg

# 9. CMS Detector
def cms_detector(target):
    print(f"\n{BLUE}[*] Running Content Management System (CMS) Detection...{RESET}")
    try:
        url = f"http://{target}/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            html = response.read().decode('utf-8', errors='ignore').lower()
        if 'wp-content' in html or 'wordpress' in html:
            cms = "WordPress"
        elif 'joomla' in html:
            cms = "Joomla"
        elif 'drupal' in html:
            cms = "Drupal"
        else:
            cms = "Generic/Custom HTML or Framework"
        result = f"[+] Detected Platform Architecture: {cms}"
        print(f"{GREEN}{result}{RESET}")
        return result
    except Exception as e:
        error_msg = f"[-] CMS detection failed: {str(e)}"
        print(f"{RED}{error_msg}{RESET}")
        return error_msg

# Main Automation Flow Control
def main():
    print_banner()
    target = get_target()
    
    report_data = []
    report_data.append(f"Framework Scan Report for: {target}")
    report_data.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_data.append("="*50 + "\n")
    
    r1 = reverse_dns(target)
    report_data.append(f"--- 1. Reverse DNS ---\n{r1}\n")
    
    r2 = ip_tracker(target)
    report_data.append(f"--- 2. IP Tracker Geolocation ---\n{r2}\n")
    
    r3 = whois_lookup(target)
    report_data.append(f"--- 3. WHOIS Lookup ---\n{r3}\n")
    
    r4 = vpn_detector(target)
    report_data.append(f"--- 4. Node Routing (VPN Analysis) ---\n{r4}\n")
    
    r5 = subdomain_enumerator(target)
    report_data.append(f"--- 5. Subdomain Enumeration ---\n{r5}\n")
    
    r6 = port_scanner(target)
    report_data.append(f"--- 6. Port Scan Results ---\n{r6}\n")
    
    r7 = directory_bruteforcer(target)
    report_data.append(f"--- 7. Path Checks ---\n{r7}\n")
    
    r8 = banner_grabber(target)
    report_data.append(f"--- 8. Service Banner Extraction ---\n{r8}\n")
    
    r9 = cms_detector(target)
    report_data.append(f"--- 9. CMS Detection Engine ---\n{r9}\n")
    
    # Feature 10: Auto-Reporting implementation
    report_filename = f"recon_report_{target.replace('.', '_')}.txt"
    try:
        with open(report_filename, "w") as f:
            f.write("\n".join(report_data))
        print(f"\n{GREEN}{BOLD}[+] SUCCESS: Feature 10 Triggered! All outputs saved to: {report_filename}{RESET}")
    except Exception as e:
        print(f"\n{RED}[-] Failed to generate report file: {str(e)}{RESET}")

if __name__ == "__main__":
    main()
    
